import { Navigate, Outlet, useLocation } from "react-router";

import { useAuth } from "@/app/features/auth/AuthProvider";
import { LoadingScreen } from "@/app/shared/ui/LoadingScreen";

export function ProtectedRoute() {
  const { status } = useAuth();
  const location = useLocation();

  if (status === "loading") {
    return <LoadingScreen message="Loading your workspace..." />;
  }

  if (status === "anonymous") {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return <Outlet />;
}

export function GuestRoute() {
  const { status } = useAuth();

  if (status === "loading") {
    return <LoadingScreen message="Checking session..." />;
  }

  if (status === "authenticated") {
    return <Navigate to="/diagnostic" replace />;
  }

  return <Outlet />;
}
