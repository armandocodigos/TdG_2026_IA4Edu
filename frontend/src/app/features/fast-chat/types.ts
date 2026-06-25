export interface FastChatPayload {
  query: string;
  topic?: string;
  useRag?: boolean;
  file?: File | null;
}

export interface FastChatSource {
  id: string;
  source: string;
  topic: string;
  chunkIndex: number;
}

export interface FastChatResult {
  answer: string;
  modelUsed: string;
  ragEnabled: boolean;
  sources: FastChatSource[];
  latencySeconds: number;
}
