from app.models.document import Document
from app.models.enums import Subject
from scripts.index_corpus import should_index_file


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


def test_solve_uses_rag_for_user_subject(client, db_session, monkeypatch):
    db_session.add(
        Document(
            source="algebra.md",
            topic="functions",
            subject=Subject.PRECALCULO,
            content="A quadratic function has the form ax^2 + bx + c.",
            embedding=[1.0, 0.0, 0.0],
            chunk_index=0,
            metadata_json={},
        )
    )
    db_session.commit()

    monkeypatch.setattr(
        "app.services.ollama_client.OllamaClient.embed",
        lambda self, model, text: [1.0, 0.0, 0.0],
    )
    monkeypatch.setattr(
        "app.services.ollama_client.OllamaClient.generate",
        lambda self, model, prompt: "Generated answer with context",
    )

    access_token = create_user(client, "student@example.com", "precalculo")
    response = client.post(
        "/api/solve",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"query": "Explain quadratic functions", "topic": "functions"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["rag_enabled"] is True
    assert data["context_count"] == 1
    assert len(data["sources"]) == 1


def test_solve_returns_no_context_when_subject_has_no_matching_documents(client, db_session, monkeypatch):
    monkeypatch.setattr(
        "app.services.ollama_client.OllamaClient.embed",
        lambda self, model, text: [1.0, 0.0, 0.0],
    )
    monkeypatch.setattr(
        "app.services.ollama_client.OllamaClient.generate",
        lambda self, model, prompt: "Generated answer without context",
    )

    access_token = create_user(client, "student2@example.com", "preuniversitario")
    response = client.post(
        "/api/solve",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"query": "Explain quadratic functions", "topic": "functions"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["rag_enabled"] is True
    assert data["context_count"] == 0
    assert data["sources"] == []


def test_solve_prompt_forces_same_language(monkeypatch, db_session):
    from app.models.enums import UserRole
    from app.models.user import User
    from app.services.rag_service import RAGService

    user = User(
        email="language@example.com",
        hashed_password="hashed",
        full_name="Language Example",
        subject=Subject.PRECALCULO,
        role=UserRole.STUDENT,
        is_active=True,
    )

    prompt = RAGService(db_session)._build_prompt(
        user=user,
        query="Explica que es una funcion cuadratica",
        topic="quadratic functions",
        rag_enabled=True,
        retrieved_documents=[
            Document(
                source="basic/quadratic_functions.md",
                topic="quadratic functions",
                subject=Subject.PRECALCULO,
                content="A quadratic function has the form ax^2 + bx + c.",
                embedding=[1.0, 0.0, 0.0],
                chunk_index=0,
                metadata_json={},
            )
        ],
    )

    assert "Always answer in the same language as the student's question." in prompt
    assert "If the retrieved context is in another language" in prompt
    assert "Student subject: precalculo." in prompt


def test_should_index_file_skips_readme_and_unsupported_files(tmp_path):
    readme_file = tmp_path / "README.md"
    readme_file.write_text("ignored", encoding="utf-8")
    supported_file = tmp_path / "quadratic_functions.md"
    supported_file.write_text("indexed", encoding="utf-8")
    unsupported_file = tmp_path / "lesson.pdf"
    unsupported_file.write_text("ignored", encoding="utf-8")

    assert should_index_file(readme_file) is False
    assert should_index_file(supported_file) is True
    assert should_index_file(unsupported_file) is False
