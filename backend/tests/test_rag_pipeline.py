import re
import asyncio
import httpx
from httpx import ASGITransport

from app.main import app
from app.core.database import get_db
from app.models.document import Document
from app.models.enums import Subject


def test_socratic_rag_pipeline_e2e(db_session):
    asyncio.run(_async_test_socratic_rag_pipeline_e2e(db_session))


async def _async_test_socratic_rag_pipeline_e2e(db_session):
    # Pre-populate RAG database context
    docs = [
        Document(
            source="math_book_v1.md",
            topic="algebra",
            subject=Subject.PRECALCULO,
            content="La diferencia de cuadrados es una técnica de factorización importante. a^2 - b^2 = (a-b)(a+b)",
            embedding=[1.0, 0.0, 0.0],
            chunk_index=1,
            metadata_json={}
        ),
        Document(
            source="math_book_v2.md",
            topic="algebra",
            subject=Subject.PRECALCULO,
            content="Ejemplos de trinomios cuadrados perfectos.",
            embedding=[0.9, 0.1, 0.0],
            chunk_index=2,
            metadata_json={}
        ),
        Document(
            source="math_book_v3.md",
            topic="algebra",
            subject=Subject.PRECALCULO,
            content="Para factorizar x^2 - 9, se identifica a=x y b=3.",
            embedding=[0.8, 0.2, 0.0],
            chunk_index=3,
            metadata_json={}
        ),
        Document(
            source="math_book_v4.md",
            topic="algebra",
            subject=Subject.PRECALCULO,
            content="Otros temas de calculo que no importan mucho aca.",
            embedding=[0.1, 0.9, 0.0],
            chunk_index=4,
            metadata_json={}
        ),
    ]
    db_session.add_all(docs)
    db_session.commit()

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
            # Create student
            register_response = await client.post(
                "/api/auth/register",
                json={
                    "email": "student_rag_test@example.com",
                    "password": "secret_password",
                    "full_name": "RAG Student",
                    "subject": "precalculo",
                },
            )
            assert register_response.status_code == 201

            login_response = await client.post(
                "/api/auth/login",
                json={"email": "student_rag_test@example.com", "password": "secret_password"},
            )
            assert login_response.status_code == 200
            token = login_response.json()["access_token"]

            # a) Confirmar que el código de estado de respuesta sea 200 OK.
            response = await client.post(
                "/api/solve",
                headers={"Authorization": f"Bearer {token}"},
                json={"query": "Cómo factorizo x^2 - 9", "topic": "algebra"},
                timeout=120.0  # Allow enough time for local LLM inference
            )
            assert response.status_code == 200
            data = response.json()

            # b) Verificar que el campo rag_metadata contenga exactamente 3 registros y que el similarity_score sea flotante
            rag_metadata = data.get("rag_metadata", [])
            assert len(rag_metadata) == 3
            for item in rag_metadata:
                assert "similarity_score" in item
                assert isinstance(item["similarity_score"], float)

            # c) Validar mediante expresiones regulares que el texto generado posea delimitadores matemáticos balanceados
            answer = data.get("answer", "")
            # Basic check for balanced $$ and $ using regex
            block_count = len(re.findall(r"(?<!\\)\$\$", answer))
            assert block_count % 2 == 0, "Unbalanced block KaTeX delimiters ($$)"

            without_blocks = re.sub(r"(?s)(?<!\\)\$\$.*?(?<!\\)\$\$", "", answer)
            inline_count = len(re.findall(r"(?<!\\)\$(?!\$)", without_blocks))
            assert inline_count % 2 == 0, "Unbalanced inline KaTeX delimiters ($)"

            # d) Certificar que se cumple la estrategia socrática Zero-Reveal
            # The tutor should NOT give the direct simplified factorization (x-3)(x+3) or (x+3)(x-3)
            stripped_answer = answer.replace(" ", "").replace("\n", "").lower()
            assert "(x-3)(x+3)" not in stripped_answer, "Zero-Reveal failed: direct answer given"
            assert "(x+3)(x-3)" not in stripped_answer, "Zero-Reveal failed: direct answer given"

    finally:
        app.dependency_overrides.clear()
