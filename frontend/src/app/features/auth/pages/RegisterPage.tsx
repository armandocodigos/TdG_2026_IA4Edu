import { useState } from "react";
import { Link, useNavigate } from "react-router";
import { BookOpen, Eye, EyeOff, UserPlus } from "lucide-react";

import { useAuth } from "@/app/features/auth/AuthProvider";
import { getErrorMessage } from "@/app/shared/api/errors";
import type { Subject } from "@/app/shared/types/domain";
import { AuthBackground } from "@/app/features/auth/components/AuthBackground";

const subjectOptions: Array<{ value: Subject; label: string }> = [
  { value: "precalculo", label: "Precálculo" },
  { value: "preuniversitario", label: "Curso Preuniversitario" },
];

export function RegisterPage() {
  const [form, setForm] = useState({
    fullName: "",
    email: "",
    password: "",
    subject: "precalculo" as Subject,
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      await register(form);
      navigate("/diagnostic", { replace: true });
    } catch (submitError) {
      setError(getErrorMessage(submitError, "No se pudo crear la cuenta."));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="relative flex min-h-screen items-center justify-center px-4 py-10">
      <AuthBackground />

      <div className="w-full max-w-md">
        {/* Branding */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-600 shadow-lg shadow-blue-500/25">
            <BookOpen className="h-7 w-7 text-white" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900">
            Crear una cuenta
          </h1>
          <p className="mt-1.5 text-sm text-gray-500">
            Regístrate para acceder a tu diagnóstico y plan de estudio personalizado
          </p>
        </div>

        {/* Card */}
        <div className="rounded-2xl border border-blue-100 bg-white/80 p-8 shadow-xl shadow-blue-200/40 backdrop-blur-sm">
          <form className="space-y-5" onSubmit={handleSubmit}>
            {/* Nombre completo */}
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-gray-700" htmlFor="register-name">
                Nombre completo
              </label>
              <input
                id="register-name"
                value={form.fullName}
                onChange={(e) => setForm((c) => ({ ...c, fullName: e.target.value }))}
                placeholder="Juan Pérez"
                required
                className="flex h-11 w-full rounded-xl border border-gray-200 bg-gray-50 px-4 text-sm text-gray-900 outline-none transition-all placeholder:text-gray-400 focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-500/20"
              />
            </div>

            {/* Email */}
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-gray-700" htmlFor="register-email">
                Correo electrónico
              </label>
              <input
                id="register-email"
                type="email"
                value={form.email}
                onChange={(e) => setForm((c) => ({ ...c, email: e.target.value }))}
                placeholder="tu@correo.com"
                required
                className="flex h-11 w-full rounded-xl border border-gray-200 bg-gray-50 px-4 text-sm text-gray-900 outline-none transition-all placeholder:text-gray-400 focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-500/20"
              />
            </div>

            {/* Contraseña */}
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-gray-700" htmlFor="register-password">
                Contraseña
              </label>
              <div className="relative">
                <input
                  id="register-password"
                  type={showPassword ? "text" : "password"}
                  value={form.password}
                  onChange={(e) => setForm((c) => ({ ...c, password: e.target.value }))}
                  placeholder="Mínimo 8 caracteres"
                  minLength={8}
                  required
                  className="flex h-11 w-full rounded-xl border border-gray-200 bg-gray-50 px-4 pr-11 text-sm text-gray-900 outline-none transition-all placeholder:text-gray-400 focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-500/20"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 transition-colors hover:text-gray-600"
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            {/* Materia */}
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-gray-700">
                Materia principal
              </label>
              <div className="grid grid-cols-2 gap-3">
                {subjectOptions.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => setForm((c) => ({ ...c, subject: option.value }))}
                    className={`flex h-11 items-center justify-center rounded-xl border text-sm font-medium transition-all ${
                      form.subject === option.value
                        ? "border-blue-500 bg-blue-50 text-blue-700 ring-2 ring-blue-500/20"
                        : "border-gray-200 bg-gray-50 text-gray-600 hover:border-gray-300 hover:bg-gray-100"
                    }`}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>

            {error ? (
              <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {error}
              </div>
            ) : null}

            <button
              type="submit"
              disabled={isSubmitting}
              className="flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-sm font-semibold text-white shadow-lg shadow-blue-500/25 transition-all hover:from-blue-700 hover:to-indigo-700 hover:shadow-xl hover:shadow-blue-500/30 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isSubmitting ? (
                "Creando cuenta..."
              ) : (
                <>
                  <UserPlus className="h-4 w-4" />
                  Crear cuenta
                </>
              )}
            </button>
          </form>

          <div className="mt-6 border-t border-gray-100 pt-6 text-center">
            <p className="text-sm text-gray-500">
              ¿Ya tienes cuenta?{" "}
              <Link
                className="font-semibold text-blue-600 transition-colors hover:text-blue-700"
                to="/login"
              >
                Inicia sesión
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
