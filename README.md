# IA para la Educación: herramienta de aprendizaje multimodal y centrado en el estudiante

Plataforma de apoyo académico en matemáticas (materias *precálculo* y *preuniversitario*).
Combina un frontend en React con un backend en FastAPI y modelos de lenguaje locales vía Ollama.

Módulos principales: diagnóstico académico, exámenes personalizados, chat rápido, tutoría socrática con entrada multimodal.

## Stack

- **Backend:** FastAPI + SQLAlchemy 2.0 + Alembic
- **Frontend:** React + TypeScript + Vite
- **Base de datos:** PostgreSQL + pgvector
- **IA:** Ollama (LLMs locales + embeddings)

## Estructura del repositorio

```
backend/         API, lógica académica y persistencia
frontend/        Interfaz de usuario
datasets/        Corpus de contenido académico para indexar en RAG
infrastructure/  Imagen de PostgreSQL + pgvector y entorno local
socratic_model/  Módulo de tutoría socrática
```

## Requisitos previos

- **Docker** (para la base de datos)
- **Python 3.12+**
- **Node.js** (frontend)
- **Ollama** corriendo en `http://localhost:11434`

##  Instalación y ejecución

### 1. Modelos de Ollama

El backend necesita un modelo de embeddings (imprescindible para indexar y para el RAG) y el LLM
que usan los módulos de generación:

```bash
ollama pull nomic-embed-text   # embeddings: indexación del corpus y RAG
ollama pull gemma3n            # generación: chat rápido, solve, retroalimentación y tutor socrático
```

### 2. Backend

Desde `backend/`, en este orden:

```bash
cp .env.example .env                       # configurar variables
docker compose up -d --build mathtutor-db  # levantar PostgreSQL + pgvector

python3 -m venv venv                       # crear entorno 
source venv/bin/activate
pip install -r requirements.txt

alembic upgrade head                       # aplicar migraciones

python3 -m scripts.index_corpus                          # indexar el corpus en RAG
python3 -m scripts.seed_diagnostic_question_bank --reset # cargar banco de preguntas del diagnóstico
python3 -m scripts.seed_exam_question_bank --reset       # cargar banco de preguntas de los exámenes

uvicorn app.main:app --reload              # API en http://127.0.0.1:8000
```


### 3. Frontend

Desde `frontend/`:

```bash
cp .env.example .env   # define VITE_API_BASE_URL (default http://127.0.0.1:8000)
npm install
npm run dev            # app en http://localhost:5173
```

### 4. Verificación

- API: http://127.0.0.1:8000
- Frontend: http://localhost:5173
