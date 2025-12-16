"""LangGraph state schema for RAG workflow."""
from typing import TypedDict, List, Optional
from backend.models.document import DocumentChunk

class RAGState(TypedDict):
    """State for RAG workflow."""
    query: str
    video_id: str
    intent: str  # qa | summary | comparison | complex
    retrieved_chunks: List[DocumentChunk]
    final_answer: str
    sources: List[dict]
    conversation_history: List[dict]
    confidence: float
    retry_count: int
