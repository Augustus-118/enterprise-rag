"""
Configuration settings for RAG system
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set in environment")
    
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    COLLECTION_NAME = "rag_collection"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50

settings = Settings()

# Export at module level (so it can be imported directly)
GEMINI_API_KEY = settings.GEMINI_API_KEY
EMBEDDING_MODEL = settings.EMBEDDING_MODEL
RERANKER_MODEL = settings.RERANKER_MODEL
COLLECTION_NAME = settings.COLLECTION_NAME
CHUNK_SIZE = settings.CHUNK_SIZE
CHUNK_OVERLAP = settings.CHUNK_OVERLAP
