import { NavLink, Outlet } from "react-router";
import {
  Bell,
  ChevronLeft,
  ChevronRight,
  ClipboardList,
  GraduationCap,
  Layers,
  LogOut,
  MessageCircle,
  Settings,
  Zap,
} from "lucide-react";
import { useState } from "react";

import { useAuth } from "@/app/features/auth/AuthProvider";
import { SubjectModal } from "@/app/components/SubjectModal";

const SUBJECT_LABELS: Record<string, string> = {
  precalculo: "Precálculo",
  preuniversitario: "Preuniversitario",
};

const menuItems = [
  { path: "/diagnostic", label: "Diagnóstico", icon: ClipboardList },
  { path: "/exams", label: "Exámenes", icon: GraduationCap },
  { path: "/fast-ai-chat", label: "Chat AI Rápido", icon: Zap },
  { path: "/socratic-chat", label: "Chat Socrático", icon: MessageCircle },
];

export function Layout() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isSubjectModalOpen, setIsSubjectModalOpen] = useState(false);
  const { user, logout } = useAuth();

  return (
    <div className="flex h-screen w-full bg-[#fafafa]">
      <aside
        className={`${isCollapsed ? "w-16" : "w-64"} flex flex-col border-r border-[#e5e5e5] bg-white transition-all duration-300`}
      >
        <div className="flex h-16 items-center justify-between border-b border-[#e5e5e5] px-4">
          {!isCollapsed ? (
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
                <span className="text-sm font-semibold text-white"></span>
              </div>
              <span className="text-[15px] font-semibold text-[#171717]">SocraChat</span>
            </div>
          ) : (
            <div className="mx-auto flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
              <span className="text-sm font-semibold text-white"></span>
            </div>
          )}
        </div>

        <nav className="flex-1 px-2 py-4">
          <div className="space-y-1">
            {menuItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    `flex items-center gap-3 rounded-md px-3 py-2.5 text-[13px] font-medium transition-colors ${
                      isActive
                        ? "bg-[#f5f5f5] text-[#171717]"
                        : "text-[#737373] hover:bg-[#fafafa] hover:text-[#171717]"
                    }`
                  }
                  title={isCollapsed ? item.label : undefined}
                >
                  <Icon className="h-4 w-4 flex-shrink-0" strokeWidth={2} />
                  {!isCollapsed ? <span>{item.label}</span> : null}
                </NavLink>
              );
            })}
          </div>
        </nav>

        <div className="border-t border-[#e5e5e5] px-2 py-3">
          {!isCollapsed ? (
            <div className="mb-2 flex items-center gap-3 rounded-md border border-[#e5e5e5] bg-[#fafafa] p-3">
              <div className="h-9 w-9 flex-shrink-0 rounded-full bg-gradient-to-br from-orange-400 to-pink-500" />
              <div className="min-w-0">
                <p className="truncate text-[13px] font-medium text-[#171717]">{user?.fullName || "Usuario"}</p>
                <p className="truncate text-[11px] text-[#737373]">{user?.email || "user@example.com"}</p>
                <p className="mt-0.5 text-[11px] font-medium text-blue-600">
                  {user?.subject ? SUBJECT_LABELS[user.subject] ?? user.subject : "—"}
                </p>
              </div>
            </div>
          ) : null}

          <button
            onClick={() => setIsCollapsed((value) => !value)}
            className="flex w-full items-center justify-center gap-2 rounded-md px-3 py-2 text-[13px] font-medium text-[#737373] transition-colors hover:bg-[#fafafa] hover:text-[#171717]"
            title={isCollapsed ? "Expandir" : "Contraer"}
          >
            {isCollapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <>
                <ChevronLeft className="h-4 w-4" />
                <span>Contraer</span>
              </>
            )}
          </button>
        </div>
      </aside>

      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="flex h-16 items-center justify-between border-b border-[#e5e5e5] bg-white px-6">
          <div className="flex items-center gap-4">
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsSubjectModalOpen(true)}
              className="flex h-9 w-9 items-center justify-center rounded-md transition-colors hover:bg-[#f5f5f5]"
              title="Configuración de materia"
            >
              <Settings className="h-4 w-4 text-[#737373]" />
            </button>
            <div className="mx-1 h-6 w-px bg-[#e5e5e5]" />
            <button
              onClick={() => void logout()}
              className="flex items-center gap-2 rounded-md px-3 py-2 text-[13px] font-medium text-[#737373] transition-colors hover:bg-[#fef2f2] hover:text-red-600"
              title="Cerrar sesión"
            >
              <LogOut className="h-4 w-4" />
              <span>Salir</span>
            </button>
          </div>
        </header>

        <main className="flex-1 overflow-auto">
          <Outlet />
        </main>
      </div>

      <SubjectModal isOpen={isSubjectModalOpen} onClose={() => setIsSubjectModalOpen(false)} />
    </div>
  );
}
