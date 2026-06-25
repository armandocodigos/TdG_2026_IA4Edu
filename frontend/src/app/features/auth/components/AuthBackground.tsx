import {
  Award,
  BookOpen,
  Brain,
  Calculator,
  GraduationCap,
  Lightbulb,
  Target,
  TrendingUp,
} from "lucide-react";

interface IconCard {
  icon: React.ElementType;
  color: string;
  bg: string;
  top?: string;
  bottom?: string;
  left?: string;
  right?: string;
  delay: string;
  duration: string;
  animation: string;
}

interface Sphere {
  size: number;
  gradient: string;
  top?: string;
  bottom?: string;
  left?: string;
  right?: string;
  delay: string;
  duration: string;
  animation: string;
  opacity: number;
}

const CARDS: IconCard[] = [
  {
    icon: GraduationCap,
    color: "#3b82f6",
    bg: "#eff6ff",
    top: "7%",
    left: "4%",
    delay: "0s",
    duration: "6.5s",
    animation: "auth-card-float",
  },
  {
    icon: TrendingUp,
    color: "#8b5cf6",
    bg: "#f5f3ff",
    top: "6%",
    right: "5%",
    delay: "1.2s",
    duration: "7s",
    animation: "auth-card-float-b",
  },
  {
    icon: BookOpen,
    color: "#6366f1",
    bg: "#eef2ff",
    top: "38%",
    left: "2%",
    delay: "0.6s",
    duration: "8s",
    animation: "auth-card-float",
  },
  {
    icon: Calculator,
    color: "#0ea5e9",
    bg: "#f0f9ff",
    top: "35%",
    right: "3%",
    delay: "2s",
    duration: "7.5s",
    animation: "auth-card-float-b",
  },
  {
    icon: Brain,
    color: "#7c3aed",
    bg: "#faf5ff",
    bottom: "22%",
    left: "3%",
    delay: "1.5s",
    duration: "9s",
    animation: "auth-card-float",
  },
  {
    icon: Target,
    color: "#2563eb",
    bg: "#eff6ff",
    bottom: "20%",
    right: "4%",
    delay: "0.3s",
    duration: "6s",
    animation: "auth-card-float-b",
  },
  {
    icon: Lightbulb,
    color: "#f59e0b",
    bg: "#fffbeb",
    bottom: "5%",
    left: "18%",
    delay: "2.5s",
    duration: "8.5s",
    animation: "auth-card-float",
  },
  {
    icon: Award,
    color: "#10b981",
    bg: "#f0fdf4",
    bottom: "4%",
    right: "16%",
    delay: "1s",
    duration: "7.2s",
    animation: "auth-card-float-b",
  },
];

const SPHERES: Sphere[] = [
  /* Izquierda, entre GraduationCap y BookOpen */
  {
    size: 18,
    gradient: "radial-gradient(circle at 35% 35%, #93c5fd, #3b82f6cc)",
    top: "22%",
    left: "7%",
    delay: "0.4s",
    duration: "5.5s",
    animation: "auth-card-float",
    opacity: 0.7,
  },
  {
    size: 11,
    gradient: "radial-gradient(circle at 35% 35%, #c7d2fe, #6366f1aa)",
    top: "30%",
    left: "12%",
    delay: "1.8s",
    duration: "7s",
    animation: "auth-card-float-b",
    opacity: 0.55,
  },
  /* Derecha, entre TrendingUp y Calculator */
  {
    size: 16,
    gradient: "radial-gradient(circle at 35% 35%, #ddd6fe, #8b5cf6cc)",
    top: "20%",
    right: "9%",
    delay: "0.9s",
    duration: "6s",
    animation: "auth-card-float-b",
    opacity: 0.65,
  },
  {
    size: 10,
    gradient: "radial-gradient(circle at 35% 35%, #bfdbfe, #60a5faaa)",
    top: "28%",
    right: "14%",
    delay: "2.2s",
    duration: "8s",
    animation: "auth-card-float",
    opacity: 0.5,
  },
  /* Izquierda, entre BookOpen y Brain */
  {
    size: 22,
    gradient: "radial-gradient(circle at 35% 35%, #a5f3fc, #0ea5e9bb)",
    top: "55%",
    left: "6%",
    delay: "1.1s",
    duration: "9s",
    animation: "auth-card-float",
    opacity: 0.6,
  },
  /* Derecha, entre Calculator y Target */
  {
    size: 14,
    gradient: "radial-gradient(circle at 35% 35%, #e9d5ff, #a855f7bb)",
    top: "58%",
    right: "7%",
    delay: "0.7s",
    duration: "6.8s",
    animation: "auth-card-float-b",
    opacity: 0.6,
  },
  /* Zonas centrales altas */
  {
    size: 13,
    gradient: "radial-gradient(circle at 35% 35%, #bfdbfe, #3b82f6aa)",
    top: "14%",
    left: "22%",
    delay: "3s",
    duration: "7.5s",
    animation: "auth-card-float-b",
    opacity: 0.45,
  },
  {
    size: 9,
    gradient: "radial-gradient(circle at 35% 35%, #ddd6fe, #7c3aedaa)",
    top: "16%",
    right: "22%",
    delay: "1.6s",
    duration: "6.2s",
    animation: "auth-card-float",
    opacity: 0.4,
  },
  /* Zonas bajas */
  {
    size: 16,
    gradient: "radial-gradient(circle at 35% 35%, #bbf7d0, #10b981bb)",
    bottom: "12%",
    left: "30%",
    delay: "2.8s",
    duration: "8.2s",
    animation: "auth-card-float",
    opacity: 0.5,
  },
  {
    size: 12,
    gradient: "radial-gradient(circle at 35% 35%, #fde68a, #f59e0bbb)",
    bottom: "14%",
    right: "28%",
    delay: "1.4s",
    duration: "7.8s",
    animation: "auth-card-float-b",
    opacity: 0.5,
  },
];

export function AuthBackground() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden bg-[#f0f5ff]">
      {/* Orbs de fondo difuminados */}
      <div className="auth-orb auth-orb-1" />
      <div className="auth-orb auth-orb-2" />
      <div className="auth-orb auth-orb-3" />
      <div className="auth-orb auth-orb-4" />

      {/* Grilla sutil */}
      <div
        className="absolute inset-0 opacity-[0.05]"
        style={{
          backgroundImage:
            "linear-gradient(rgba(99,102,241,1) 1px, transparent 1px), linear-gradient(90deg, rgba(99,102,241,1) 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      />

      {/* Esferas decorativas */}
      {SPHERES.map((sphere, index) => (
        <div
          key={`sphere-${index}`}
          className="absolute hidden lg:block rounded-full"
          style={{
            width: sphere.size,
            height: sphere.size,
            background: sphere.gradient,
            top: sphere.top,
            bottom: sphere.bottom,
            left: sphere.left,
            right: sphere.right,
            opacity: sphere.opacity,
            animation: `${sphere.animation} ${sphere.duration} ease-in-out ${sphere.delay} infinite`,
            boxShadow: `0 2px 8px rgba(99,102,241,0.25)`,
          }}
        />
      ))}

      {/* Tarjetas flotantes con íconos */}
      {CARDS.map((card, index) => {
        const Icon = card.icon;
        return (
          <div
            key={`card-${index}`}
            className="absolute hidden lg:flex h-[72px] w-[72px] items-center justify-center rounded-2xl shadow-lg shadow-blue-100/60"
            style={{
              top: card.top,
              bottom: card.bottom,
              left: card.left,
              right: card.right,
              animation: `${card.animation} ${card.duration} ease-in-out ${card.delay} infinite`,
              backgroundColor: card.bg,
            }}
          >
            <Icon
              style={{ color: card.color }}
              className="h-7 w-7"
              strokeWidth={1.8}
            />
          </div>
        );
      })}
    </div>
  );
}
