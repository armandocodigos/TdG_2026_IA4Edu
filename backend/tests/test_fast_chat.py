from fastapi import HTTPException, status

from app.models.document import Document
from app.models.enums import Subject


def create_user(client, email: str, subject: str = "precalculo") -> str:
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "secret123",
            "full_name": "Student Example",
            "subject": subject,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={"email": email, "password": "secret123"},
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


def test_fast_chat_requires_auth(client):
    response = client.post(
        "/api/fast-chat",
        json={"query": "Explica una funcion cuadratica"},
    )

    assert response.status_code == 401


def test_fast_chat_returns_direct_answer(client, monkeypatch):
    captured_prompt = {}

    def fake_generate(self, model: str, prompt: str):
        captured_prompt["model"] = model
        captured_prompt["prompt"] = prompt
        return "La funcion cuadratica tiene forma ax^2 + bx + c."

    monkeypatch.setattr("app.services.ollama_client.OllamaClient.generate", fake_generate)

    access_token = create_user(client, "fastchat@example.com", "precalculo")
    response = client.post(
        "/api/fast-chat",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"query": "Explica que es una funcion cuadratica", "topic": "funciones"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["answer"]
    assert data["rag_enabled"] is False
    assert data["context_count"] == 0
    assert data["sources"] == []
    assert data["model_used"]
    assert isinstance(data["latency_ms"], int)
    assert "Be direct and brief." in captured_prompt["prompt"]
    assert "Student subject: precalculo." in captured_prompt["prompt"]


def test_fast_chat_with_rag_uses_context(client, db_session, monkeypatch):
    db_session.add(
        Document(
            source="basic/derivadas_basicas.md",
            topic="derivadas basicas",
            subject=Subject.PRECALCULO,
            content="La derivada de x^2 es 2x y representa la pendiente de la recta tangente.",
            embedding=[1.0, 0.0, 0.0],
            chunk_index=0,
            metadata_json={},
        )
    )
    db_session.commit()

    captured_prompt = {}

    monkeypatch.setattr(
        "app.services.ollama_client.OllamaClient.embed",
        lambda self, model, text: [1.0, 0.0, 0.0],
    )

    def fake_generate(self, model: str, prompt: str):
        captured_prompt["prompt"] = prompt
        return "La derivada de x^2 es 2x."

    monkeypatch.setattr("app.services.ollama_client.OllamaClient.generate", fake_generate)

    access_token = create_user(client, "fastchatrag@example.com", "precalculo")
    response = client.post(
        "/api/fast-chat",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "query": "Cual es la derivada de x^2",
            "topic": "derivadas basicas",
            "use_rag": True,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["rag_enabled"] is True
    assert data["context_count"] == 1
    assert len(data["sources"]) == 1
    assert "Use the provided context when it is relevant" in captured_prompt["prompt"]
    assert "Context:" in captured_prompt["prompt"]


def test_fast_chat_validates_query_length(client):
    access_token = create_user(client, "shortquery@example.com")

    response = client.post(
        "/api/fast-chat",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"query": "hi"},
    )

    assert response.status_code == 422


def test_fast_chat_returns_503_when_ollama_fails(client, monkeypatch):
    def fake_generate(self, model: str, prompt: str):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Ollama generate request failed")

    monkeypatch.setattr("app.services.ollama_client.OllamaClient.generate", fake_generate)

    access_token = create_user(client, "ollamafail@example.com")
    response = client.post(
        "/api/fast-chat",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"query": "Resuelve x^2 - 5x + 6 = 0"},
    )

    assert response.status_code == 503
