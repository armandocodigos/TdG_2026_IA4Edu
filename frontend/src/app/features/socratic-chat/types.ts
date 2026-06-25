export interface SocraticChatPayload {
  query: string;
  topic?: string;
  useRag?: boolean;
  file?: File | null;
  mode?: string;
}

export interface SocraticChatSource {
  id: string;
  source: string;
  topic: string;
  chunkIndex: number;
}

export interface SocraticChatResult {
  answer: string;
  modelUsed: string;
  ragEnabled: boolean;
  sources: SocraticChatSource[];
  latencySeconds: number;
}
