import type { Subject, UserRole } from "@/app/shared/types/domain";

export interface SessionUser {
  id: string;
  email: string;
  fullName: string;
  subject: Subject;
  role: UserRole;
}

export interface UserProfile extends SessionUser {
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface AuthSession {
  accessToken: string;
  refreshToken: string;
  user: SessionUser;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  fullName: string;
  subject: Subject;
}
