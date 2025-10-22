from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi

class HybridRetriever:
    def __init__(self):
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        self.bm25_index = None
        self.all_chunks = []
    
    def build_bm25_index(self, chunks):
        self.all_chunks = chunks
        tokenized = [chunk.split() for chunk in chunks]
        self.bm25_index = BM25Okapi(tokenized)
    
    def hybrid_search(self, query, collection, top_k=10):
        query_embedding = self.embed_model.encode(query).tolist()
        vector_results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        tokenized_query = query.split()
        bm25_scores = self.bm25_index.get_scores(tokenized_query)
        top_bm25_idx = sorted(range(len(bm25_scores)), 
                             key=lambda i: bm25_scores[i], 
                             reverse=True)[:top_k]
        
        combined_docs = []
        combined_metas = []
        seen = set()
        
        for i, doc in enumerate(vector_results['documents'][0]):
            if doc not in seen:
                combined_docs.append(doc)
                combined_metas.append(vector_results['metadatas'][0][i])
                seen.add(doc)
        
        for idx in top_bm25_idx:
            doc = self.all_chunks[idx]
            if doc not in seen:
                combined_docs.append(doc)
                combined_metas.append({'file': 'bm25'})
                seen.add(doc)
        
        return combined_docs, combined_metas
    
    def rerank(self, query, documents, top_k=3):
        if not documents:
            return []
        
        pairs = [[query, doc] for doc in documents]
        scores = self.reranker.predict(pairs)
        ranked_idx = sorted(range(len(scores)), 
                           key=lambda i: scores[i], 
                           reverse=True)[:top_k]
        
        return [documents[i] for i in ranked_idx]
from sentence_transformers import SentenceTransformer, CrossEncoder
from rank_bm25 import BM25Okapi

class HybridRetriever:
    def __init__(self):
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        self.bm25_index = None
        self.all_chunks = []
    
    def build_bm25_index(self, chunks):
        self.all_chunks = chunks
        tokenized = [chunk.split() for chunk in chunks]
        self.bm25_index = BM25Okapi(tokenized)
    
    def hybrid_search(self, query, collection, top_k=10):
        query_embedding = self.embed_model.encode(query).tolist()
        vector_results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        tokenized_query = query.split()
        bm25_scores = self.bm25_index.get_scores(tokenized_query)
        top_bm25_idx = sorted(range(len(bm25_scores)), 
                             key=lambda i: bm25_scores[i], 
                             reverse=True)[:top_k]
        
        combined_docs = []
        combined_metas = []
        seen = set()
        
        for i, doc in enumerate(vector_results['documents'][0]):
            if doc not in seen:
                combined_docs.append(doc)
                combined_metas.append(vector_results['metadatas'][0][i])
                seen.add(doc)
        
        for idx in top_bm25_idx:
            doc = self.all_chunks[idx]
            if doc not in seen:
                combined_docs.append(doc)
                combined_metas.append({'file': 'bm25'})
                seen.add(doc)
        
        return combined_docs, combined_metas
    
    def rerank(self, query, documents, top_k=3):
        if not documents:
            return []
        
        pairs = [[query, doc] for doc in documents]
        scores = self.reranker.predict(pairs)
        ranked_idx = sorted(range(len(scores)), 
                           key=lambda i: scores[i], 
                           reverse=True)[:top_k]
        
        return [documents[i] for i in ranked_idx]
