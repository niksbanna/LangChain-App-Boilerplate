"""Vector Database Service - Handles vector storage and retrieval"""
from typing import List, Dict, Any, Optional
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from ..core.config import settings


class VectorDBService:
    """Service for managing vector database operations"""
    
    def __init__(self):
        self.provider = settings.VECTOR_DB_PROVIDER
        self.embeddings = self._initialize_embeddings()
        self.vector_store = self._initialize_vector_store()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
    
    def _initialize_embeddings(self):
        """Initialize embeddings model"""
        return HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    def _initialize_vector_store(self):
        """Initialize vector store based on configuration"""
        if self.provider == "chroma":
            return Chroma(
                persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
                embedding_function=self.embeddings
            )
        elif self.provider == "pinecone":
            from langchain_community.vectorstores import Pinecone
            import pinecone
            
            pinecone.init(
                api_key=settings.PINECONE_API_KEY,
                environment=settings.PINECONE_ENVIRONMENT
            )
            return Pinecone.from_existing_index(
                index_name=settings.PINECONE_INDEX_NAME,
                embedding=self.embeddings
            )
        else:
            raise ValueError(f"Unsupported vector DB provider: {self.provider}")
    
    async def add_document(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add a document to the vector database
        
        Args:
            content: Document content
            metadata: Optional metadata
        
        Returns:
            Document ID
        """
        try:
            # Split document into chunks
            chunks = self.text_splitter.split_text(content)
            
            # Create documents with metadata
            documents = [
                Document(
                    page_content=chunk,
                    metadata=metadata or {}
                )
                for chunk in chunks
            ]
            
            # Add to vector store
            ids = self.vector_store.add_documents(documents)
            
            # Persist if using Chroma
            if self.provider == "chroma":
                self.vector_store.persist()
            
            return ids[0] if ids else "unknown"
        except Exception as e:
            raise Exception(f"Error adding document: {str(e)}")
    
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filters
        
        Returns:
            List of search results with content, score, and metadata
        """
        try:
            # Perform similarity search with scores
            results = self.vector_store.similarity_search_with_score(
                query,
                k=top_k,
                filter=filter_metadata
            )
            
            # Format results
            formatted_results = [
                {
                    "content": doc.page_content,
                    "score": float(score),
                    "metadata": doc.metadata
                }
                for doc, score in results
            ]
            
            return formatted_results
        except Exception as e:
            raise Exception(f"Error searching documents: {str(e)}")
    
    async def delete_collection(self) -> None:
        """Delete all documents from the collection"""
        try:
            if self.provider == "chroma":
                self.vector_store.delete_collection()
                self.vector_store = self._initialize_vector_store()
        except Exception as e:
            raise Exception(f"Error deleting collection: {str(e)}")
    
    def health_check(self) -> bool:
        """Check if vector DB service is healthy"""
        try:
            # Try a simple search
            self.vector_store.similarity_search("test", k=1)
            return True
        except:
            return False


# Singleton instance
vector_db_service = VectorDBService()
