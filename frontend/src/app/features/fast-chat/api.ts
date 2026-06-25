import { apiRequest } from "@/app/shared/api/http";
import type { FastChatPayload, FastChatResult } from "@/app/features/fast-chat/types";

interface FastChatResponse {
  answer: string;
  model_used: string;
  rag_enabled: boolean;
  sources: Array<{
    id: string;
    source: string;
    topic: string;
    chunk_index: number;
  }>;
  latency_ms: number;
}

export function askFastChat(payload: FastChatPayload) {
  const formData = new FormData();
  formData.append("query", payload.query);
  formData.append("use_rag", String(payload.useRag ?? false));
  
  if (payload.topic) {
    formData.append("topic", payload.topic);
  }
  
  if (payload.file) {
    formData.append("file", payload.file);
  }

  console.log("[FastChat API] Sending payload to backend:", Object.fromEntries(formData));

  return apiRequest<FastChatResponse>("/api/fast-chat", {
    method: "POST",
    body: formData,
  }).then(
    (response): FastChatResult => ({
      answer: response.answer,
      modelUsed: response.model_used,
      ragEnabled: response.rag_enabled,
      sources: response.sources.map((source) => ({
        id: source.id,
        source: source.source,
        topic: source.topic,
        chunkIndex: source.chunk_index,
      })),
      latencySeconds: response.latency_ms / 1000,
    }),
  );
}
