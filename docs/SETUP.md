# Setup Guide

This guide will help you set up the LangChain App Boilerplate for development and production.

## Quick Start

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- Ollama (for local LLM support)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd LangChain-App-Boilerplate
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

### 3. Install and Configure Ollama

```bash
# Install Ollama from https://ollama.ai

# Pull a model (e.g., llama2)
ollama pull llama2

# Verify Ollama is running
curl http://localhost:11434
```

### 4. Run the Backend

```bash
# From the backend directory
python main.py
```

The API will be available at:
- REST: http://localhost:8000/api/v1
- GraphQL: http://localhost:8000/graphql
- Docs: http://localhost:8000/docs

### 5. Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local

# Run development server
npm run dev
```

The UI will be available at http://localhost:3000

## Docker Setup

### Using Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### After Docker Startup

1. Wait for Ollama to start (check logs: `docker-compose logs ollama`)
2. Pull a model into the Ollama container:

```bash
docker-compose exec ollama ollama pull llama2
```

3. Access the services:
   - Backend: http://localhost:8000
   - Frontend: http://localhost:3000
   - Ollama: http://localhost:11434

## Configuration

### Backend Environment Variables

Create `backend/.env`:

```env
# Application
APP_NAME=LangChain App Boilerplate
DEBUG=true

# LLM Configuration
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Vector Database
VECTOR_DB_PROVIDER=chroma
CHROMA_PERSIST_DIRECTORY=./data/chroma

# Embeddings
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Frontend Environment Variables

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Using Different LLM Providers

### OpenAI

1. Get an API key from https://platform.openai.com/
2. Update `backend/.env`:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-3.5-turbo
```

### Other Ollama Models

```bash
# List available models
ollama list

# Pull a different model
ollama pull mistral
ollama pull codellama

# Update .env
OLLAMA_MODEL=mistral
```

## Using Different Vector Databases

### Pinecone

1. Sign up at https://www.pinecone.io/
2. Create an index
3. Update `backend/.env`:

```env
VECTOR_DB_PROVIDER=pinecone
PINECONE_API_KEY=your-api-key
PINECONE_ENVIRONMENT=your-environment
PINECONE_INDEX_NAME=your-index-name
```

4. Install Pinecone client:

```bash
pip install pinecone-client
```

## Testing the Setup

### Backend Tests

```bash
cd backend
pytest tests/
```

### Frontend Build Test

```bash
cd frontend
npm run build
```

### Manual API Test

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

## Troubleshooting

### Ollama Not Connecting

1. Check if Ollama is running:
```bash
curl http://localhost:11434
```

2. Verify model is pulled:
```bash
ollama list
```

3. Check OLLAMA_BASE_URL in .env

### Vector Database Errors

1. Check if the persist directory exists and is writable
2. Try deleting the data directory and restarting
3. Ensure you have enough disk space

### Frontend Not Connecting to Backend

1. Verify backend is running at http://localhost:8000
2. Check NEXT_PUBLIC_API_URL in .env.local
3. Check browser console for CORS errors

### Port Already in Use

Change ports in:
- Backend: `backend/.env` (PORT variable)
- Frontend: Run with `npm run dev -- -p 3001`
- Docker: Edit `docker-compose.yml` port mappings

## Next Steps

1. Read the [API Documentation](API.md)
2. Explore the code structure
3. Try adding documents and chatting
4. Customize for your use case

## Production Deployment

For production deployment:

1. Set `DEBUG=false`
2. Use environment-specific configuration
3. Set up proper secrets management
4. Configure HTTPS
5. Set up monitoring and logging
6. Use production-grade servers (Gunicorn, PM2)
7. Set up CI/CD pipeline
