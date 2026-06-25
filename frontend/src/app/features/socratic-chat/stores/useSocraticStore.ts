import { create } from "zustand";

import { askSocraticChat } from "@/app/features/socratic-chat/api";
import type { SocraticChatResult, SocraticChatPayload } from "@/app/features/socratic-chat/types";
import { getErrorMessage } from "@/app/shared/api/errors";

interface Message {
  id: string;
  type: "query" | "response";
  query?: string;
  result?: SocraticChatResult;
  fileName?: string;
  fileType?: string;
  filePreview?: string;
}

interface SocraticChatState {
  messages: Message[];
  isSubmitting: boolean;
  error: string | null;
  ask: (payload: SocraticChatPayload) => Promise<void>;
  clearChat: () => void;
}

export const useSocraticStore = create<SocraticChatState>((set, get) => ({
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
      const result = await askSocraticChat(payload);
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
