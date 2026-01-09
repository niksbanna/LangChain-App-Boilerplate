"""LLM Service - Handles LLM interactions"""
from typing import Optional, List
from langchain_community.llms import Ollama
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

from ..core.config import settings
from ..models.schemas import ChatMessage


class LLMService:
    """Service for managing LLM interactions"""
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.llm = self._initialize_llm()
        self.conversations = {}  # Store conversation memories
    
    def _initialize_llm(self):
        """Initialize the LLM based on configuration"""
        if self.provider == "ollama":
            return Ollama(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.OLLAMA_MODEL
            )
        elif self.provider == "openai":
            from langchain_community.chat_models import ChatOpenAI
            return ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_MODEL
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def get_conversation_memory(self, conversation_id: str) -> ConversationBufferMemory:
        """Get or create conversation memory"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = ConversationBufferMemory(
                return_messages=True,
                memory_key="chat_history"
            )
        return self.conversations[conversation_id]
    
    async def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """
        Generate a response using the LLM
        
        Args:
            message: User message
            conversation_id: Optional conversation ID for context
            context: Optional additional context (e.g., from vector DB)
        
        Returns:
            LLM response
        """
        try:
            # Build the prompt with context if provided
            if context:
                prompt = f"Context information:\n{context}\n\nUser question: {message}\n\nPlease answer the question based on the context provided."
            else:
                prompt = message
            
            # Use conversation memory if provided
            if conversation_id:
                memory = self.get_conversation_memory(conversation_id)
                memory.chat_memory.add_user_message(message)
                
                # Get chat history
                history = memory.load_memory_variables({}).get("chat_history", [])
                
                # Build prompt with history
                full_prompt = ""
                for msg in history:
                    if hasattr(msg, 'content'):
                        full_prompt += f"{msg.content}\n"
                full_prompt += f"\nUser: {prompt}\nAssistant:"
                
                response = self.llm.invoke(full_prompt)
                memory.chat_memory.add_ai_message(response)
            else:
                response = self.llm.invoke(prompt)
            
            return response
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def clear_conversation(self, conversation_id: str) -> None:
        """Clear conversation history"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
    
    def health_check(self) -> bool:
        """Check if LLM service is healthy"""
        try:
            # Try a simple prompt
            self.llm.invoke("Test")
            return True
        except:
            return False


# Singleton instance
llm_service = LLMService()
