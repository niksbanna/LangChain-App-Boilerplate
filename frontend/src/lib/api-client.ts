import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  use_vector_db?: boolean;
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  sources?: any[];
}

export interface DocumentInput {
  content: string;
  metadata?: any;
}

export interface SearchRequest {
  query: string;
  top_k?: number;
}

export interface SearchResult {
  content: string;
  score: number;
  metadata: any;
}

class ApiClient {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Chat endpoints
  async chat(request: ChatRequest): Promise<ChatResponse> {
    const response = await axios.post(`${this.baseURL}/api/v1/chat`, request);
    return response.data;
  }

  // Document endpoints
  async addDocument(document: DocumentInput): Promise<any> {
    const response = await axios.post(`${this.baseURL}/api/v1/documents`, document);
    return response.data;
  }

  // Search endpoints
  async search(request: SearchRequest): Promise<SearchResult[]> {
    const response = await axios.post(`${this.baseURL}/api/v1/search`, request);
    return response.data;
  }

  // Health check
  async healthCheck(): Promise<any> {
    const response = await axios.get(`${this.baseURL}/api/v1/health`);
    return response.data;
  }

  // Clear conversation
  async clearConversation(conversationId: string): Promise<void> {
    await axios.delete(`${this.baseURL}/api/v1/conversations/${conversationId}`);
  }
}

export const apiClient = new ApiClient();
