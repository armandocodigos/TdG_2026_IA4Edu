import { FormEvent, useState, useEffect, useRef, ChangeEvent } from "react";
import { Send, Paperclip, X, Music, FileText } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

import { useSocraticStore } from "@/app/features/socratic-chat/stores/useSocraticStore";
import { MathText } from "@/app/components/ui/MathText";

const TypingIndicator = () => (
  <motion.div
    animate={{
      boxShadow: [
        "0px 0px 0px 0px rgba(79, 70, 229, 0)",
        "0px 0px 15px 4px rgba(79, 70, 229, 0.4)",
        "0px 0px 0px 0px rgba(79, 70, 229, 0)",
      ],
    }}
    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
    className="flex w-fit items-center gap-1.5 rounded-lg border border-[#e5e5e5] bg-white px-4 py-3"
  >
    <motion.div className="h-2 w-2 rounded-full bg-indigo-600" animate={{ y: [0, -5, 0] }} transition={{ duration: 0.6, repeat: Infinity, delay: 0 }} />
    <motion.div className="h-2 w-2 rounded-full bg-indigo-600" animate={{ y: [0, -5, 0] }} transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }} />
    <motion.div className="h-2 w-2 rounded-full bg-indigo-600" animate={{ y: [0, -5, 0] }} transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }} />
  </motion.div>
);

const ALLOWED_TYPES = [
  "image/jpeg",
  "image/png",
  "image/jpg",
  "audio/mpeg",
  "audio/wav",
  "audio/m4a",
  "audio/ogg",
  "application/pdf",
];

export function SocraticChatPage() {
  const [query, setQuery] = useState("");
  const [useRag, setUseRag] = useState(true); // Socratic might benefit from RAG by default
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileError, setFileError] = useState<string | null>(null);

  const { messages, isSubmitting, error, ask, clearChat } = useSocraticStore();
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isSubmitting]);

  useEffect(() => {
    clearChat();
    return () => {
      clearChat();
    };
  }, [clearChat]);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!ALLOWED_TYPES.includes(file.type)) {
      setFileError("Formato no soportado. Por favor, sube una imagen, audio o PDF.");
      setSelectedFile(file);
    } else {
      setFileError(null);
      setSelectedFile(file);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    setFileError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (query.trim().length < 3) return;
    if (fileError) return;

    ask({ query, useRag, file: selectedFile });
    setQuery("");
    clearFile();
  }

  return (
    <div className="flex h-full bg-[#fafafa]">
      <div className="flex flex-1 flex-col relative">
        <div className="sticky top-0 z-10 flex items-center justify-between border-b border-[#e5e5e5] bg-[#fafafa]/90 px-8 py-4 backdrop-blur-sm">
          <h1 className="text-[15px] font-medium text-[#171717]">Tutoría Socrática</h1>
          <span className="rounded-full bg-indigo-100 px-3 py-1 text-[12px] font-medium text-indigo-700">Tema Libre</span>
        </div>

        <div className="flex-1 overflow-auto p-8">
          <div className="mx-auto max-w-4xl space-y-6">
            {messages.length > 0 ? (
              <AnimatePresence initial={false}>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    transition={{ duration: 0.3 }}
                  >
                    {message.type === "query" && (
                    <div className="flex justify-end">
                      <div className="max-w-[70%] flex flex-col rounded-lg bg-indigo-600 px-4 py-3 text-white">
                        {message.filePreview && (
                          <motion.div
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            transition={{ type: "spring", stiffness: 400, damping: 25 }}
                            className="mb-2 w-fit max-w-full rounded bg-indigo-800/50 p-2"
                          >
                            {message.fileType?.startsWith("image/") ? (
                              <img src={message.filePreview} alt={message.fileName} className="max-h-24 w-auto rounded object-cover" />
                            ) : (
                              <div className="flex items-center gap-2 px-1 text-[12px] text-indigo-50">
                                {message.fileType?.startsWith("audio/") ? (
                                  <Music className="h-4 w-4 shrink-0" />
                                ) : (
                                  <FileText className="h-4 w-4 shrink-0" />
                                )}
                                <span className="truncate">{message.fileName}</span>
                              </div>
                            )}
                          </motion.div>
                        )}
                        <p className="text-[13px] leading-relaxed">{message.query}</p>
                      </div>
                    </div>
                  )}
                  {message.type === "response" && message.result && (
                    <div className="flex justify-start">
                      <div className="max-w-[85%] rounded-lg border border-[#e5e5e5] bg-white px-4 py-3 text-[#171717] shadow-sm">
                        <div className="overflow-x-auto max-w-full">
                          <MathText content={message.result.answer} className="text-[13px] leading-relaxed" />
                        </div>
                        <div className="mt-4 border-t border-[#f0f0f0] pt-4 text-[12px] text-[#737373]">
                          <p>Modelo: {message.result.modelUsed}</p>
                          <p>Tiempo de respuesta: {message.result.latencySeconds.toFixed(2)} s</p>
                          <p>RAG: {String(message.result.ragEnabled)}</p>
                          {message.result.ragEnabled ? <p>Fuentes: {message.result.sources.length}</p> : null}
                        </div>
                      </div>
                    </div>
                  )}
                  </motion.div>
                ))}
              </AnimatePresence>
            ) : (
              <div className="flex min-h-[50vh] items-center justify-center">
                <div className="max-w-xl text-center">
                  <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100 text-indigo-600">
                    <FileText className="h-6 w-6" />
                  </div>
                  <h2 className="text-[24px] font-semibold text-[#171717]">Tutoría Socrática</h2>
                  <p className="mt-3 text-[14px] leading-7 text-[#737373]">
                    Este espacio está diseñado para guiarte paso a paso. Comparte tu procedimiento matemático, un archivo de audio o una imagen de tus apuntes, y te ayudaré a encontrar la solución sin darte la respuesta directa.
                  </p>
                </div>
              </div>
            )}
            <AnimatePresence>
              {isSubmitting && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="flex justify-start"
                >
                  <TypingIndicator />
                </motion.div>
              )}
            </AnimatePresence>
            <div ref={messagesEndRef} />
          </div>
        </div>

        <div className="border-t border-[#e5e5e5] bg-white p-6">
          <div className="mx-auto max-w-4xl">
            {error ? <p className="mb-3 text-[13px] text-[#b91c1c]">{error}</p> : null}
            <form onSubmit={handleSubmit} className="space-y-3">
              <label className="flex items-center gap-2 text-[12px] text-[#525252]">
                <input
                  type="checkbox"
                  checked={useRag}
                  onChange={(event) => setUseRag(event.target.checked)}
                  className="h-4 w-4 rounded border-[#d4d4d4] text-indigo-600 focus:ring-indigo-600"
                />
                Usar RAG
              </label>
              
              {selectedFile && (
                <div className="flex flex-col gap-1">
                  <div className="flex items-center w-fit gap-2 rounded-full bg-[#f5f5f5] px-3 py-1.5 text-[12px] text-[#525252]">
                    <span className="truncate max-w-[200px] font-medium">{selectedFile.name}</span>
                    <button type="button" onClick={clearFile} className="text-[#a3a3a3] hover:text-[#171717]">
                      <X className="h-3.5 w-3.5" />
                    </button>
                  </div>
                  {fileError && <span className="text-[12px] text-[#b91c1c] px-1">{fileError}</span>}
                </div>
              )}

              <div className="relative flex items-center gap-2">
                <input
                  type="file"
                  className="hidden"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  accept={ALLOWED_TYPES.join(",")}
                />
                <motion.button
                  type="button"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => fileInputRef.current?.click()}
                  className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg border border-[#e5e5e5] bg-white transition-colors hover:bg-indigo-50 hover:text-indigo-600 hover:border-indigo-200"
                  title="Adjuntar archivo"
                >
                  <motion.div
                    animate={{ rotate: selectedFile ? 15 : 0 }}
                    transition={{ type: "spring", stiffness: 300, damping: 20 }}
                  >
                    <Paperclip className="h-5 w-5" />
                  </motion.div>
                </motion.button>
                <div className="relative flex-1">
                  <input
                    type="text"
                    value={query}
                    onChange={(event) => setQuery(event.target.value)}
                    placeholder="Describe tu razonamiento o sube un ejercicio para analizarlo juntos..."
                    className="w-full rounded-lg border border-transparent bg-[#f5f5f5] py-3.5 pl-4 pr-12 text-[13px] placeholder:text-[#a3a3a3] transition-colors focus:border-indigo-500 focus:bg-white focus:outline-none"
                  />
                  <motion.button
                    type="submit"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    disabled={isSubmitting || query.trim().length < 3 || fileError !== null}
                    className="absolute right-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-md bg-indigo-600 transition-colors hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-70"
                  >
                    <Send className="h-4 w-4 text-white" />
                  </motion.button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
