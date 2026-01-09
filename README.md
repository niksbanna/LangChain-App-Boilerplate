# LangChain App Boilerplate

A production-grade boilerplate for creating LangChain applications with a modern tech stack. This template provides a complete setup for building AI-powered applications with local LLM support, vector database integration, REST & GraphQL APIs, and a responsive UI.

## 🚀 Features

### 1. **Modular Architecture**
- Clean separation of concerns between backend, frontend, and infrastructure
- Service-oriented design for easy maintenance and scaling
- Configuration management with environment variables

### 2. **Local LLM Support**
- Integration with Ollama for running local LLMs (Llama2, Mistral, etc.)
- Support for OpenAI and other providers
- Easy model switching through configuration
- Conversation memory management

### 3. **Vector Database Integration**
- Chroma DB for vector storage (default)
- Support for Pinecone and Weaviate
- Document chunking and embedding pipeline
- Similarity search with configurable parameters

### 4. **Dual API Architecture**
- **REST API**: Full CRUD operations with FastAPI
- **GraphQL API**: Flexible querying with Strawberry
- Auto-generated API documentation (Swagger/OpenAPI)
- CORS support for cross-origin requests

### 5. **Modern Frontend**
- Next.js 14 with TypeScript
- Tailwind CSS for styling
- Interactive chat interface
- Document management UI
- Real-time conversation with AI

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- Ollama (for local LLM support)

## 🛠️ Installation

### Option 1: Local Development

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

5. Install and run Ollama:
```bash
# Install Ollama from https://ollama.ai
ollama pull llama2  # Or your preferred model
```

6. Run the backend:
```bash
python main.py
```

The API will be available at:
- REST API: http://localhost:8000/api/v1
- GraphQL: http://localhost:8000/graphql
- API Docs: http://localhost:8000/docs

#### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.local.example .env.local
```

4. Run the development server:
```bash
npm run dev
```

The UI will be available at http://localhost:3000

### Option 2: Docker Deployment

1. Build and run all services:
```bash
docker-compose up --build
```

This will start:
- Backend API at http://localhost:8000
- Frontend UI at http://localhost:3000
- Ollama service at http://localhost:11434

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── rest/          # REST API endpoints
│   │   │   └── graphql/       # GraphQL schema & resolvers
│   │   ├── core/              # Configuration & utilities
│   │   ├── models/            # Data models & schemas
│   │   ├── services/          # Business logic services
│   │   │   ├── llm_service.py       # LLM integration
│   │   │   └── vector_service.py    # Vector DB operations
│   │   └── db/                # Database utilities
│   ├── tests/                 # Test suite
│   ├── main.py               # Application entry point
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile           # Backend Docker config
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Next.js pages
│   │   ├── lib/            # API client & utilities
│   │   ├── types/          # TypeScript types
│   │   └── styles/         # CSS styles
│   ├── package.json        # Node dependencies
│   └── Dockerfile         # Frontend Docker config
└── docker-compose.yml     # Multi-container setup
```

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:

```env
# LLM Provider (ollama, openai, huggingface)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# OpenAI (optional)
# OPENAI_API_KEY=your-key
# OPENAI_MODEL=gpt-3.5-turbo

# Vector Database (chroma, pinecone, weaviate)
VECTOR_DB_PROVIDER=chroma
CHROMA_PERSIST_DIRECTORY=./data/chroma

# Embeddings
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Frontend Configuration

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 API Documentation

### REST API Endpoints

#### Chat
```bash
POST /api/v1/chat
{
  "message": "What is LangChain?",
  "use_vector_db": false,
  "conversation_id": "optional-id"
}
```

#### Add Document
```bash
POST /api/v1/documents
{
  "content": "LangChain is a framework...",
  "metadata": {"source": "docs"}
}
```

#### Search Documents
```bash
POST /api/v1/search
{
  "query": "What is LangChain?",
  "top_k": 5
}
```

### GraphQL API

Access GraphQL Playground at http://localhost:8000/graphql

Example Query:
```graphql
query {
  search(input: {query: "LangChain", topK: 5}) {
    content
    score
    metadata
  }
}
```

Example Mutation:
```graphql
mutation {
  chat(input: {message: "Hello!", useVectorDb: false}) {
    message
    conversationId
  }
}
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 🔐 Security Considerations

- Never commit `.env` files with secrets
- Use environment variables for sensitive data
- Implement rate limiting for production
- Add authentication/authorization as needed
- Sanitize user inputs
- Keep dependencies updated

## 🚢 Production Deployment

### Deployment Checklist

1. Set `DEBUG=false` in production
2. Configure proper CORS origins
3. Use production-grade WSGI server (e.g., Gunicorn)
4. Set up reverse proxy (Nginx)
5. Enable HTTPS
6. Configure monitoring and logging
7. Set up backup for vector database
8. Use managed services for databases if possible

### Environment Variables for Production

```env
DEBUG=false
ALLOWED_ORIGINS=["https://yourdomain.com"]
# Add API keys securely through your hosting provider
```

## 🎯 Use Cases

- **Customer Support Chatbots**: RAG-powered support with document retrieval
- **Documentation Assistant**: Query technical documentation with context
- **Content Generation**: AI-powered content creation with custom models
- **Research Assistant**: Search and summarize large document collections
- **Code Assistant**: Help with coding questions using local models

## 🔄 Extending the Boilerplate

### Adding a New LLM Provider

1. Update `backend/app/services/llm_service.py`
2. Add provider configuration in `config.py`
3. Install required dependencies

### Adding a New Vector Database

1. Update `backend/app/services/vector_service.py`
2. Add provider-specific configuration
3. Install required client library

### Adding Authentication

1. Install `fastapi-users` or similar
2. Add middleware to `main.py`
3. Protect endpoints with dependencies
4. Update frontend API client

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [LangChain](https://github.com/langchain-ai/langchain) - Framework for LLM applications
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Chroma](https://www.trychroma.com/) - Vector database

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review API documentation at `/docs`

## 🗺️ Roadmap

- [ ] Add authentication & authorization
- [ ] Implement streaming responses
- [ ] Add more LLM providers (Anthropic, Cohere)
- [ ] Enhance error handling & logging
- [ ] Add monitoring & observability
- [ ] Create deployment guides for major cloud providers
- [ ] Add more frontend components
- [ ] Implement caching layer
- [ ] Add rate limiting
- [ ] Create CLI tool for management

---

Built with ❤️ for the LangChain community