import { env } from "@/app/shared/config/env";
import { ApiError } from "@/app/shared/api/errors";
import { clearStoredSession, getStoredSession, storeSession } from "@/app/features/auth/storage";
import type { AuthSession, SessionUser } from "@/app/features/auth/types";
import type { Subject, UserRole } from "@/app/shared/types/domain";

interface RequestOptions extends Omit<RequestInit, "body"> {
  auth?: boolean;
  body?: BodyInit | null | undefined;
}

async function parseError(response: Response) {
  try {
    const data = await response.json();
    if (typeof data?.detail === "string") {
      return data.detail;
    }
    return JSON.stringify(data);
  } catch {
    return response.statusText || "Request failed.";
  }
}

interface SessionUserResponse {
  id: string;
  email: string;
  full_name: string;
  subject: Subject;
  role: UserRole;
}

interface AuthSessionResponse {
  access_token: string;
  refresh_token: string;
  user: SessionUserResponse;
}

let refreshPromise: Promise<AuthSession | null> | null = null;

function mapSessionUser(payload: SessionUserResponse): SessionUser {
  return {
    id: payload.id,
    email: payload.email,
    fullName: payload.full_name,
    subject: payload.subject,
    role: payload.role,
  };
}

function mapAuthSession(payload: AuthSessionResponse): AuthSession {
  return {
    accessToken: payload.access_token,
    refreshToken: payload.refresh_token,
    user: mapSessionUser(payload.user),
  };
}

async function refreshStoredSession() {
  const session = getStoredSession();
  if (!session?.refreshToken) {
    return null;
  }

  if (!refreshPromise) {
    refreshPromise = fetch(`${env.apiBaseUrl}/api/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: session.refreshToken }),
    })
      .then(async (response) => {
        if (!response.ok) {
          clearStoredSession();
          return null;
        }

        const nextSession = mapAuthSession((await response.json()) as AuthSessionResponse);
        storeSession(nextSession);
        return nextSession;
      })
      .finally(() => {
        refreshPromise = null;
      });
  }

  return refreshPromise;
}

async function runRequest(path: string, options: RequestOptions, accessToken?: string) {
  const { auth = true, headers, body, ...rest } = options;

  const requestHeaders = new Headers(headers);

  if (body && !requestHeaders.has("Content-Type") && !(body instanceof FormData)) {
    requestHeaders.set("Content-Type", "application/json");
  }

  if (auth && accessToken) {
    requestHeaders.set("Authorization", `Bearer ${accessToken}`);
  }

  return fetch(`${env.apiBaseUrl}${path}`, {
    ...rest,
    headers: requestHeaders,
    body,
  });
}

export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { auth = true } = options;
  const session = getStoredSession();

  let response = await runRequest(path, options, session?.accessToken);

  if (auth && response.status === 401 && session?.refreshToken && path !== "/api/auth/refresh") {
    const nextSession = await refreshStoredSession();
    if (nextSession?.accessToken) {
      response = await runRequest(path, options, nextSession.accessToken);
    }
  }

  if (!response.ok) {
    throw new ApiError(response.status, await parseError(response));
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}
