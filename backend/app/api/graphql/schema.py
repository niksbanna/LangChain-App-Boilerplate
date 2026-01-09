"""GraphQL schema and resolvers"""
import strawberry
from typing import List, Optional
import uuid

from ...models.schemas import ChatRequest as ChatRequestModel, SearchRequest as SearchRequestModel
from ...services.llm_service import llm_service
from ...services.vector_service import vector_db_service


# GraphQL Types
@strawberry.type
class ChatMessage:
    message: str
    conversation_id: str
    sources: Optional[List[str]] = None


@strawberry.type
class SearchResult:
    content: str
    score: float
    metadata: str


@strawberry.type
class DocumentResult:
    id: str
    content: str
    success: bool


# GraphQL Input Types
@strawberry.input
class ChatInput:
    message: str
    conversation_id: Optional[str] = None
    use_vector_db: bool = False


@strawberry.input
class DocumentInput:
    content: str
    metadata: Optional[str] = None


@strawberry.input
class SearchInput:
    query: str
    top_k: int = 5


# Queries
@strawberry.type
class Query:
    @strawberry.field
    async def health(self) -> str:
        """Health check query"""
        return "healthy"
    
    @strawberry.field
    async def search(self, input: SearchInput) -> List[SearchResult]:
        """Search for documents in vector database"""
        try:
            results = await vector_db_service.search(
                query=input.query,
                top_k=input.top_k
            )
            
            return [
                SearchResult(
                    content=r["content"],
                    score=r["score"],
                    metadata=str(r["metadata"])
                )
                for r in results
            ]
        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")


# Mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def chat(self, input: ChatInput) -> ChatMessage:
        """Send a chat message and get a response"""
        try:
            conversation_id = input.conversation_id or str(uuid.uuid4())
            
            # Get context from vector DB if requested
            context = None
            sources = None
            if input.use_vector_db:
                search_results = await vector_db_service.search(
                    query=input.message,
                    top_k=3
                )
                if search_results:
                    context = "\n\n".join([r["content"] for r in search_results])
                    sources = [r["content"] for r in search_results]
            
            # Generate response
            response_message = await llm_service.chat(
                message=input.message,
                conversation_id=conversation_id,
                context=context
            )
            
            return ChatMessage(
                message=response_message,
                conversation_id=conversation_id,
                sources=sources
            )
        except Exception as e:
            raise Exception(f"Chat failed: {str(e)}")
    
    @strawberry.mutation
    async def add_document(self, input: DocumentInput) -> DocumentResult:
        """Add a document to the vector database"""
        try:
            doc_id = await vector_db_service.add_document(
                content=input.content,
                metadata={"raw": input.metadata} if input.metadata else {}
            )
            
            return DocumentResult(
                id=doc_id,
                content=input.content,
                success=True
            )
        except Exception as e:
            raise Exception(f"Failed to add document: {str(e)}")
    
    @strawberry.mutation
    async def clear_conversation(self, conversation_id: str) -> bool:
        """Clear a conversation history"""
        try:
            llm_service.clear_conversation(conversation_id)
            return True
        except:
            return False


# Create schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
