# API Documentation

## REST API

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
Currently, no authentication is required. Add authentication middleware as needed.

## Endpoints

### Health Check
Check the health status of the application.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "llm_provider": "ollama",
  "vector_db_provider": "chroma"
}
```

### Chat

Send a message and get a response from the LLM.

**Endpoint**: `POST /chat`

**Request Body**:
```json
{
  "message": "What is LangChain?",
  "conversation_id": "optional-conversation-id",
  "use_vector_db": false
}
```

**Response**:
```json
{
  "message": "LangChain is a framework for developing applications powered by language models...",
  "conversation_id": "uuid-here",
  "sources": [
    {
      "content": "Source document content...",
      "score": 0.95,
      "metadata": {}
    }
  ]
}
```

### Add Document

Add a document to the vector database.

**Endpoint**: `POST /documents`

**Request Body**:
```json
{
  "content": "LangChain is a framework for developing applications...",
  "metadata": {
    "source": "documentation",
    "author": "John Doe"
  }
}
```

**Response**:
```json
{
  "id": "document-id",
  "content": "LangChain is a framework...",
  "metadata": {
    "source": "documentation",
    "author": "John Doe"
  }
}
```

### Search Documents

Search for similar documents in the vector database.

**Endpoint**: `POST /search`

**Request Body**:
```json
{
  "query": "What is LangChain?",
  "top_k": 5
}
```

**Response**:
```json
[
  {
    "content": "Document content...",
    "score": 0.95,
    "metadata": {
      "source": "docs"
    }
  }
]
```

### Clear Conversation

Clear a specific conversation history.

**Endpoint**: `DELETE /conversations/{conversation_id}`

**Response**:
```json
{
  "message": "Conversation cleared successfully"
}
```

## GraphQL API

### Endpoint
```
http://localhost:8000/graphql
```

### Schema

#### Queries

```graphql
type Query {
  health: String!
  search(input: SearchInput!): [SearchResult!]!
}
```

#### Mutations

```graphql
type Mutation {
  chat(input: ChatInput!): ChatMessage!
  addDocument(input: DocumentInput!): DocumentResult!
  clearConversation(conversationId: String!): Boolean!
}
```

#### Types

```graphql
type ChatMessage {
  message: String!
  conversationId: String!
  sources: [String!]
}

type SearchResult {
  content: String!
  score: Float!
  metadata: String!
}

type DocumentResult {
  id: String!
  content: String!
  success: Boolean!
}

input ChatInput {
  message: String!
  conversationId: String
  useVectorDb: Boolean = false
}

input DocumentInput {
  content: String!
  metadata: String
}

input SearchInput {
  query: String!
  topK: Int = 5
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request data
- `500 Internal Server Error`: Server error

Error Response Format:
```json
{
  "detail": "Error message here"
}
```

## Interactive Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.
Visit http://localhost:8000/graphql for GraphQL Playground.
