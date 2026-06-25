import { apiRequest } from "@/app/shared/api/http";
import type { SocraticChatPayload, SocraticChatResult } from "@/app/features/socratic-chat/types";

interface SocraticChatResponse {
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

export function askSocraticChat(payload: SocraticChatPayload) {
  const formData = new FormData();
  formData.append("query", payload.query);
  formData.append("use_rag", String(payload.useRag ?? false));
  formData.append("mode", "socratic"); // Inject socratic mode
  
  if (payload.topic) {
    formData.append("topic", payload.topic);
  }
  
  if (payload.file) {
    formData.append("file", payload.file);
  }

  console.log("[SocraticChat API] Sending payload to backend:", Object.fromEntries(formData));

  // Temporarily pointing to /api/fast-chat until /api/socratic-chat is ready
  return apiRequest<SocraticChatResponse>("/api/fast-chat", {
    method: "POST",
    body: formData,
  }).then(
    (response): SocraticChatResult => ({
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
