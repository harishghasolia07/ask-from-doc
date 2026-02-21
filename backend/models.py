from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    """Single message in conversation history"""
    question: str
    answer: str


class ChatRequest(BaseModel):
    """Request body for /api/chat endpoint"""
    question: str
    conversation_history: Optional[List[ChatMessage]] = []


class SourceChunk(BaseModel):
    """Source chunk with metadata"""
    document_name: str
    chunk_text: str
    similarity: float


class ChatResponse(BaseModel):
    """Response from /api/chat endpoint"""
    success: bool
    answer: Optional[str] = None
    sources: Optional[List[SourceChunk]] = []
    error: Optional[str] = None
    timestamp: str
