import { create } from "zustand";

import { askFastChat } from "@/app/features/fast-chat/api";
import type { FastChatResult, FastChatPayload } from "@/app/features/fast-chat/types";
import { getErrorMessage } from "@/app/shared/api/errors";

interface Message {
  id: string;
  type: "query" | "response";
  query?: string;
  result?: FastChatResult;
  fileName?: string;
  fileType?: string;
  filePreview?: string;
}

interface FastChatState {
  messages: Message[];
  isSubmitting: boolean;
  error: string | null;
  ask: (payload: FastChatPayload) => Promise<void>;
  clearChat: () => void;
}

export const useFastChatStore = create<FastChatState>((set, get) => ({
  messages: [],
  isSubmitting: false,
  error: null,
  ask: async (payload) => {
    let filePreview: string | undefined;
    if (payload.file) {
      filePreview = URL.createObjectURL(payload.file);
    }

    const queryMessage: Message = {
      id: `query-${Date.now()}`,
      type: "query",
      query: payload.query,
      fileName: payload.file?.name,
      fileType: payload.file?.type,
      filePreview,
    };

    set({ isSubmitting: true, error: null, messages: [...get().messages, queryMessage] });

    try {
      const result = await askFastChat(payload);
      const responseMessage: Message = {
        id: `response-${Date.now()}`,
        type: "response",
        result,
      };
      set((state) => ({ messages: [...state.messages, responseMessage] }));
    } catch (submitError) {
      set({ error: getErrorMessage(submitError, "No fue posible responder la consulta.") });
    } finally {
      set({ isSubmitting: false });
    }
  },
  clearChat: () => {
    const { messages } = get();
    messages.forEach((msg) => {
      if (msg.filePreview) {
        URL.revokeObjectURL(msg.filePreview);
      }
    });
    set({ messages: [], error: null });
  },
}));
