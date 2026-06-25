const rawApiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim() || "http://127.0.0.1:8000";

export const env = {
  apiBaseUrl: rawApiBaseUrl.replace(/\/$/, ""),
};
