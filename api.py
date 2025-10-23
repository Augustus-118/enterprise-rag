"""
FastAPI web service for RAG system
"""
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.rag_engine import SecureRAGEngine
from api_models import (
    QueryRequest, 
    QueryResponse, 
    HealthResponse, 
    StatsResponse
)

# Global RAG engine
rag_engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic"""
    global rag_engine
    
    # Startup
    logging.info("Loading RAG engine...")
    rag_engine = SecureRAGEngine()
    rag_engine.ingest_documents("./documents/")
    logging.info("RAG engine ready!")
    
    yield
    
    # Shutdown
    logging.info("Shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Enterprise RAG API",
    description="Secure RAG with hybrid search",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple API keys
API_KEYS = {"dev_key_123", "prod_key_456"}

def verify_api_key(api_key: str = Header(..., alias="X-API-Key")):
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Enterprise RAG API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/stats", response_model=StatsResponse, tags=["System"])
def get_stats(api_key: str = Header(..., alias="X-API-Key")):
    verify_api_key(api_key)
    return {
        "total_chunks": len(rag_engine.retriever.all_chunks),
        "total_documents": len(set([m.get('file', 'unknown') 
                                    for m in rag_engine.collection.get()['metadatas']]))
    }

@app.post("/query", response_model=QueryResponse, tags=["RAG"])
def query_documents(
    request: QueryRequest,
    api_key: str = Header(..., alias="X-API-Key")
):
    """Query the RAG system"""
    verify_api_key(api_key)
    
    result = rag_engine.query(request.question, user_id=request.user_id)
    
    if 'error' in result:
        raise HTTPException(status_code=400, detail=result['error'])
    
    return QueryResponse(
        answer=result['answer'],
        sources=result['sources']
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
