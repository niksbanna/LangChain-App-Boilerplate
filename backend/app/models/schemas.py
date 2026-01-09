"""Models and schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class LLMProvider(str, Enum):
    """LLM Provider types"""
    OLLAMA = "ollama"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"


class VectorDBProvider(str, Enum):
    """Vector Database Provider types"""
    CHROMA = "chroma"
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"


class ChatMessage(BaseModel):
    """Chat message model"""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., description="User message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    use_vector_db: bool = Field(False, description="Whether to use vector DB for context")


class ChatResponse(BaseModel):
    """Chat response model"""
    message: str = Field(..., description="Assistant response")
    conversation_id: str = Field(..., description="Conversation ID")
    sources: Optional[List[Dict[str, Any]]] = Field(None, description="Source documents if vector DB used")


class DocumentInput(BaseModel):
    """Document input for vector DB"""
    content: str = Field(..., description="Document content")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Document metadata")


class DocumentResponse(BaseModel):
    """Document response"""
    id: str = Field(..., description="Document ID")
    content: str = Field(..., description="Document content")
    metadata: Dict[str, Any] = Field(..., description="Document metadata")


class SearchRequest(BaseModel):
    """Vector search request"""
    query: str = Field(..., description="Search query")
    top_k: int = Field(5, description="Number of results to return")


class SearchResult(BaseModel):
    """Search result"""
    content: str = Field(..., description="Document content")
    score: float = Field(..., description="Similarity score")
    metadata: Dict[str, Any] = Field(..., description="Document metadata")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    llm_provider: str
    vector_db_provider: str
