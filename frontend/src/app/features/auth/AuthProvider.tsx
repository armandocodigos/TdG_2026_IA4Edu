import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

import { fetchCurrentUser, login as loginRequest, logout as logoutRequest, register as registerRequest } from "@/app/features/auth/api";
import { clearStoredSession, getStoredSession, storeSession } from "@/app/features/auth/storage";
import type { AuthSession, LoginPayload, RegisterPayload, SessionUser } from "@/app/features/auth/types";

type AuthStatus = "loading" | "authenticated" | "anonymous";

interface AuthContextValue {
  status: AuthStatus;
  session: AuthSession | null;
  user: SessionUser | null;
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

function normalizeSessionUser(session: AuthSession, user: SessionUser) {
  return {
    ...session,
    user,
  };
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<AuthStatus>("loading");
  const [session, setSession] = useState<AuthSession | null>(null);

  useEffect(() => {
    const storedSession = getStoredSession();
    if (!storedSession) {
      setStatus("anonymous");
      return;
    }

    setSession(storedSession);
    fetchCurrentUser()
      .then((user) => {
        const currentSession = getStoredSession() ?? storedSession;
        const nextSession = normalizeSessionUser(currentSession, user);
        setSession(nextSession);
        storeSession(nextSession);
        setStatus("authenticated");
      })
      .catch(() => {
        clearStoredSession();
        setSession(null);
        setStatus("anonymous");
      });
  }, []);

  async function login(payload: LoginPayload) {
    const nextSession = await loginRequest(payload);
    storeSession(nextSession);
    setSession(nextSession);
    setStatus("authenticated");
  }

  async function register(payload: RegisterPayload) {
    const nextSession = await registerRequest(payload);
    storeSession(nextSession);
    setSession(nextSession);
    setStatus("authenticated");
  }

  async function logout() {
    try {
      const currentSession = getStoredSession() ?? session;
      if (currentSession?.refreshToken) {
        await logoutRequest(currentSession.refreshToken);
      }
    } catch {
      // Keep the frontend session cleanup even if backend logout fails.
    } finally {
      clearStoredSession();
      setSession(null);
      setStatus("anonymous");
    }
  }

  async function refreshUser() {
    if (!session) {
      return;
    }

    const profile = await fetchCurrentUser();
    const currentSession = getStoredSession() ?? session;
    const nextSession = normalizeSessionUser(currentSession, profile);
    setSession(nextSession);
    storeSession(nextSession);
  }

  return (
    <AuthContext.Provider
      value={{
        status,
        session,
        user: session?.user ?? null,
        login,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
