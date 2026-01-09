"""REST API endpoints"""
from fastapi import APIRouter, HTTPException
from typing import List
import uuid

from ...models.schemas import (
    ChatRequest,
    ChatResponse,
    DocumentInput,
    DocumentResponse,
    SearchRequest,
    SearchResult,
    HealthResponse
)
from ...services.llm_service import llm_service
from ...services.vector_service import vector_db_service
from ...core.config import settings


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        llm_provider=settings.LLM_PROVIDER,
        vector_db_provider=settings.VECTOR_DB_PROVIDER
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint - Send a message and get a response
    """
    try:
        # Generate or use existing conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Get context from vector DB if requested
        context = None
        sources = None
        if request.use_vector_db:
            search_results = await vector_db_service.search(
                query=request.message,
                top_k=3
            )
            if search_results:
                context = "\n\n".join([r["content"] for r in search_results])
                sources = search_results
        
        # Generate response
        response_message = await llm_service.chat(
            message=request.message,
            conversation_id=conversation_id,
            context=context
        )
        
        return ChatResponse(
            message=response_message,
            conversation_id=conversation_id,
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/documents", response_model=DocumentResponse)
async def add_document(document: DocumentInput):
    """
    Add a document to the vector database
    """
    try:
        doc_id = await vector_db_service.add_document(
            content=document.content,
            metadata=document.metadata
        )
        
        return DocumentResponse(
            id=doc_id,
            content=document.content,
            metadata=document.metadata
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=List[SearchResult])
async def search_documents(request: SearchRequest):
    """
    Search for similar documents in the vector database
    """
    try:
        results = await vector_db_service.search(
            query=request.query,
            top_k=request.top_k
        )
        
        return [
            SearchResult(
                content=r["content"],
                score=r["score"],
                metadata=r["metadata"]
            )
            for r in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversations/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """
    Clear a conversation history
    """
    try:
        llm_service.clear_conversation(conversation_id)
        return {"message": "Conversation cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
