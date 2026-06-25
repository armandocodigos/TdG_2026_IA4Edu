import { apiRequest } from "@/app/shared/api/http";
import type { RegisterPayload, LoginPayload, AuthSession, SessionUser, UserProfile } from "@/app/features/auth/types";
import type { Subject, UserRole } from "@/app/shared/types/domain";

interface SessionUserResponse {
  id: string;
  email: string;
  full_name: string;
  subject: Subject;
  role: UserRole;
}

interface UserProfileResponse extends SessionUserResponse {
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface AuthSessionResponse {
  access_token: string;
  refresh_token: string;
  user: SessionUserResponse;
}

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

function mapUserProfile(payload: UserProfileResponse): UserProfile {
  return {
    ...mapSessionUser(payload),
    isActive: payload.is_active,
    createdAt: payload.created_at,
    updatedAt: payload.updated_at,
  };
}

export function login(payload: LoginPayload) {
  return apiRequest<AuthSessionResponse>("/api/auth/login", {
    auth: false,
    method: "POST",
    body: JSON.stringify(payload),
  }).then(mapAuthSession);
}

export function register(payload: RegisterPayload) {
  return apiRequest<AuthSessionResponse>("/api/auth/register", {
    auth: false,
    method: "POST",
    body: JSON.stringify({
      email: payload.email,
      password: payload.password,
      full_name: payload.fullName,
      subject: payload.subject,
    }),
  }).then(mapAuthSession);
}

export function logout(refreshToken: string) {
  return apiRequest<void>("/api/auth/logout", {
    method: "POST",
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
}

export function fetchCurrentUser() {
  return apiRequest<UserProfileResponse>("/api/users/me").then(mapUserProfile);
}

export function updateSubject(subject: Subject) {
  return apiRequest<UserProfileResponse>("/api/users/me/subject", {
    method: "PATCH",
    body: JSON.stringify({ subject }),
  }).then(mapUserProfile);
}
