import { createBrowserRouter, Navigate } from "react-router";

import { Layout } from "@/app/components/Layout";
import { GuestRoute, ProtectedRoute } from "@/app/features/auth/guards";
import { LoginPage } from "@/app/features/auth/pages/LoginPage";
import { RegisterPage } from "@/app/features/auth/pages/RegisterPage";
import { DiagnosticAttemptPage } from "@/app/features/diagnostic/pages/DiagnosticAttemptPage";
import { DiagnosticOverviewPage } from "@/app/features/diagnostic/pages/DiagnosticOverviewPage";
import { ExamAttemptPage } from "@/app/features/exams/pages/ExamAttemptPage";
import { ExamsOverviewPage } from "@/app/features/exams/pages/ExamsOverviewPage";
import { FastChatPage } from "@/app/features/fast-chat/pages/FastChatPage";
import { SocraticChatPage } from "@/app/features/socratic-chat/pages/SocraticChatPage";
import { ComingSoonPage } from "@/app/features/placeholders/pages/ComingSoonPage";

export const router = createBrowserRouter([
  {
    path: "/login",
    Component: GuestRoute,
    children: [{ index: true, Component: LoginPage }],
  },
  {
    path: "/register",
    Component: GuestRoute,
    children: [{ index: true, Component: RegisterPage }],
  },
  {
    path: "/",
    Component: ProtectedRoute,
    children: [
      {
        Component: Layout,
        children: [
          { index: true, element: <Navigate to="/diagnostic" replace /> },
          { path: "diagnostic", Component: DiagnosticOverviewPage },
          { path: "diagnostic/:attemptId", Component: DiagnosticAttemptPage },
          { path: "exams", Component: ExamsOverviewPage },
          { path: "exams/:attemptId", Component: ExamAttemptPage },
          { path: "fast-ai-chat", Component: FastChatPage },
          { path: "socratic-chat", Component: SocraticChatPage },
          {
            path: "multimodal-input",
            element: (
              <ComingSoonPage
                title="Multimodal input is not connected yet"
                description="The backend still does not expose the multimodal pipeline, so this module remains planned only."
              />
            ),
          },
          { path: "diagnostic-test", element: <Navigate to="/diagnostic" replace /> },
          { path: "diagnostic-test/:id", element: <Navigate to="/diagnostic" replace /> },
          { path: "exam-mode", element: <Navigate to="/exams" replace /> },
          { path: "exam-mode/:id", element: <Navigate to="/exams" replace /> },
        ],
      },
    ],
  },
]);
