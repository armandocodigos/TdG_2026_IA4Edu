# Frontend

Frontend React + Vite del proyecto, conectado al backend real de FastAPI.

## Módulos conectados

- `auth`: login, registro, sesión persistida y rutas protegidas
- `diagnostic`: inicio de diagnóstico, intento activo y visualización del perfil final
- `exams`: listado de exámenes, intento activo y resultado final
- `solve`: consulta individual sobre `POST /api/solve`

## Estructura

- `src/app/features`: módulos por dominio
- `src/app/shared`: cliente API, configuración, tipos compartidos y UI reutilizable
- `src/app/components`: layout y componentes base de UI

## Variables de entorno

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Valor esperado:

```bash
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Desarrollo

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```
  
