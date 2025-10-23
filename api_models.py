"""
API request and response models
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    user_id: str = Field(default="anonymous")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is RAG?",
                "user_id": "user_123"
            }
        }

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str

class StatsResponse(BaseModel):
    total_chunks: int
    total_documents: int
