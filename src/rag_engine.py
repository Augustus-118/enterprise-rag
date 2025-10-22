import chromadb
import google.generativeai as genai
import logging

from config.settings import GEMINI_API_KEY
from src.document_loader import load_documents_from_folder
from src.retrieval import HybridRetriever
from src.security.input_validator import InputValidator
from src.security.pii_detector import PIIDetector
from src.security.rate_limiter import RateLimiter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class SecureRAGEngine:
    def __init__(self):
        self.db = chromadb.Client()
        self.collection = self.db.get_or_create_collection("secure_docs")
        self.retriever = HybridRetriever()
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.llm = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        self.validator = InputValidator()
        self.pii_detector = PIIDetector()
        self.rate_limiter = RateLimiter()
    
    def ingest_documents(self, folder_path: str):
        chunks, metadata = load_documents_from_folder(folder_path)
        
        for i, (chunk, meta) in enumerate(zip(chunks, metadata)):
            embedding = self.retriever.embed_model.encode(chunk).tolist()
            self.collection.add(
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[meta],
                ids=[f"chunk_{i}"]
            )
        
        self.retriever.build_bm25_index(chunks)
        logging.info(f"Ingested {len(chunks)} chunks")
    
    def query(self, question: str, user_id: str = "anonymous"):
        if not self.rate_limiter.allow(user_id):
            return {'error': 'Rate limit exceeded'}
        
        is_valid, msg = self.validator.validate(question)
        if not is_valid:
            return {'error': msg}
        
        question = self.validator.sanitize(question)
        
        candidates, metas = self.retriever.hybrid_search(question, self.collection)
        
        if not candidates:
            return {'answer': 'No information found.', 'sources': []}
        
        top_docs = self.retriever.rerank(question, candidates)
        
        context = "\n\n".join([f"[Doc]\n{doc}" for doc in top_docs])
        
        prompt = f"""Answer based on context:

{context}

Question: {question}

Answer:"""
        
        response = self.llm.generate_content(prompt)
        answer = response.text
        
        pii = self.pii_detector.detect(answer)
        if pii:
            answer = self.pii_detector.redact(answer)
        
        return {'answer': answer, 'sources': [m['file'] for m in metas[:3]]}
