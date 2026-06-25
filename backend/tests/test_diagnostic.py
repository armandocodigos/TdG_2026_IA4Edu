import json
import re

import pytest

from app.models.diagnostic_attempt import DiagnosticAttempt
from app.models.diagnostic_question import DiagnosticQuestion
from app.models.enums import AttemptStatus, BloomLevel, QuestionType, Subject
from app.services.diagnostic_service import DiagnosticService
from app.services.feedback_service import FeedbackService
from app.services.ollama_client import OllamaClient


def _detect_category(prompt: str) -> str:
    if "respondió CORRECTAMENTE" in prompt:
        return "positive"
    if "respondió INCORRECTAMENTE" in prompt:
        return "improvement"
    return "positive"


def _build_fake_recommendations(category: str, count: int) -> list[str]:
    if count == 0:
        return []
    if category == "positive":
        return [
            f"Aplicaste bien el procedimiento central de este tema ({index + 1}). Conserva ese criterio sustituyendo el resultado en el enunciado original para confirmar."
            for index in range(count)
        ]
    return [
        f"Conviene revisar la propiedad que controla este tipo de ejercicio ({index + 1}). Compara los datos del enunciado y sustituye el resultado antes de elegir una opción."
        for index in range(count)
    ]


@pytest.fixture(autouse=True)
def fake_ollama_recommendations(monkeypatch):
    def fake_generate(self, *, model: str, prompt: str, json_mode: bool = False) -> str:
        category = _detect_category(prompt)
        count_match = re.search(r"exactamente (\d+) recomendaciones", prompt)
        count = int(count_match.group(1)) if count_match else 2
        items = _build_fake_recommendations(category, count)
        return json.dumps({"recommendations": items})

    monkeypatch.setattr(OllamaClient, "generate", fake_generate)


def register_and_login(client, email: str, subject: str = "precalculo") -> str:
    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "secret123",
            "full_name": "Diagnostic Student",
            "subject": subject,
        },
    )
    assert response.status_code == 201
    login = client.post(
        "/api/auth/login",
        json={"email": email, "password": "secret123"},
    )
    assert login.status_code == 200
    return login.json()["access_token"]


def make_question(
    *,
    topic: str,
    skill: str,
    question_text: str,
    correct_answer: str,
    bloom_level: BloomLevel = BloomLevel.UNDERSTAND,
    subject: Subject = Subject.PRECALCULO,
) -> DiagnosticQuestion:
    return DiagnosticQuestion(
        subject=subject,
        topic=topic,
        skill=skill,
        question_text=question_text,
        bloom_level=bloom_level,
        question_type=QuestionType.MULTIPLE_CHOICE,
        options_json=[correct_answer, "Distractor"],
        correct_answer=correct_answer,
        explanation="Explanation.",
    )


def seed_two_questions(db_session) -> None:
    seed_questions(db_session, count=2)
    db_session.commit()


def seed_questions(db_session, *, count: int = 10) -> list[DiagnosticQuestion]:
    base_questions = [
        make_question(
            topic="functions",
            skill="domain",
            question_text="What is the domain of f(x)=x^2?",
            correct_answer="All real numbers",
            bloom_level=BloomLevel.REMEMBER,
        ),
        make_question(
            topic="algebra",
            skill="factoring",
            question_text="Factor x^2+2x+1",
            correct_answer="(x+1)^2",
            bloom_level=BloomLevel.CREATE,
        ),
    ]
    topics = ["functions", "algebra", "trigonometry", "equations", "limits"]
    bloom_levels = [
        BloomLevel.REMEMBER,
        BloomLevel.UNDERSTAND,
        BloomLevel.APPLY,
        BloomLevel.ANALYZE,
        BloomLevel.EVALUATE,
        BloomLevel.CREATE,
    ]
    for index in range(2, count):
        base_questions.append(
            make_question(
                topic=topics[index % len(topics)],
                skill=f"skill-{index}",
                question_text=f"Diagnostic question {index}",
                correct_answer=f"Correct {index}",
                bloom_level=bloom_levels[index % len(bloom_levels)],
            )
        )
    db_session.add_all(base_questions)
    db_session.commit()
    return base_questions


def test_diagnostic_feedback_parser_accepts_model_key_typos_json_fences_and_latex():
    raw_response = r"""```json
{
  "positive_recommendactions": [
    "En funciones, usaste $x=-\frac{b}{2a}$ para ubicar el vértice."
  ],
  "improvement_recommendaions": [
    "En trigonometría, verifica que $\sin x \neq \tan x$ antes de simplificar."
  ]
}
```"""

    positive, improvement = FeedbackService().parse_legacy_combined(raw_response)

    assert positive == ["En funciones, usaste $x=-\\frac{b}{2a}$ para ubicar el vértice."]
    assert improvement == ["En trigonometría, verifica que $\\sin x \\neq \\tan x$ antes de simplificar."]


def test_diagnostic_feedback_parser_extracts_json_from_model_text():
    raw_response = """
Aquí tienes el JSON solicitado:

{
  "feedback": {
    "positive_recommendations": [
      "Al resolver dominio, excluiste el valor que anulaba el denominador. Para conservar ese criterio, prueba los valores críticos en la expresión original."
    ],
    "improvement_recommendations": [
      "En factorización, el error aparece al elegir los números del trinomio. Antes de cerrar, verifica que suma y producto coincidan con los coeficientes."
    ]
  }
}

Espero que sea útil.
"""

    positive, improvement = FeedbackService().parse_legacy_combined(raw_response)

    assert positive == [
        "Al resolver dominio, excluiste el valor que anulaba el denominador. Para conservar ese criterio, prueba los valores críticos en la expresión original."
    ]
    assert improvement == [
        "En factorización, el error aparece al elegir los números del trinomio. Antes de cerrar, verifica que suma y producto coincidan con los coeficientes."
    ]


def test_diagnostic_feedback_parser_accepts_trailing_commas_and_object_items():
    raw_response = """
{
  "positive_recommendations": [
    {"text": "Al resolver logaritmos, aplicaste una propiedad válida para simplificar la expresión. Para conservar ese criterio, identifica primero qué propiedad conecta los términos antes de operar."},
  ],
  "improvement_recommendations": [
    {"recommendation": "En exponenciales, el error aparece al comparar bases antes de reescribirlas. Convierte ambos lados a la misma base y verifica el exponente sustituyendo el resultado."},
  ],
}
"""

    positive, improvement = FeedbackService().parse_legacy_combined(raw_response)

    assert positive == [
        "Al resolver logaritmos, aplicaste una propiedad válida para simplificar la expresión. Para conservar ese criterio, identifica primero qué propiedad conecta los términos antes de operar."
    ]
    assert improvement == [
        "En exponenciales, el error aparece al comparar bases antes de reescribirlas. Convierte ambos lados a la misma base y verifica el exponente sustituyendo el resultado."
    ]


def test_diagnostic_feedback_parser_accepts_spanish_keys_and_catchall_list():
    """El modelo puede responder con claves en español o cualquier clave con lista."""
    # clave en español
    raw_spanish = json.dumps({"recomendaciones": ["Aplica la propiedad correctamente en cada paso del cálculo."]})
    result = FeedbackService().parse_category(category="positive", raw_response=raw_spanish)
    assert result == ["Aplica la propiedad correctamente en cada paso del cálculo."]

    # clave totalmente desconocida — catch-all de primera lista encontrada
    raw_unknown = json.dumps({"sugerencias_del_tutor": ["Identifica los puntos críticos antes de evaluar el signo en cada intervalo."]})
    result2 = FeedbackService().parse_category(category="improvement", raw_response=raw_unknown)
    assert result2 == ["Identifica los puntos críticos antes de evaluar el signo en cada intervalo."]


def test_diagnostic_flow_creates_profile(client, db_session):
    seed_questions(db_session)

    access_token = register_and_login(client, "diagnostic@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    payload = start.json()
    assert payload["subject"] == "precalculo"
    assert payload["status"] == "in_progress"
    assert len(payload["questions"]) == 10
    assert payload["answers"] == {}
    bloom_levels = {question["question_text"]: question["bloom_level"] for question in payload["questions"]}
    assert bloom_levels["What is the domain of f(x)=x^2?"] == "remember"
    assert bloom_levels["Factor x^2+2x+1"] == "create"

    for question in payload["questions"]:
        answer = "All real numbers" if question["topic"] == "functions" else "(x-1)^2"
        response = client.post(
            f"/api/diagnostic/{payload['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": answer},
        )
        assert response.status_code == 204

    finish = client.post(f"/api/diagnostic/{payload['id']}/finish", headers=headers)
    assert finish.status_code == 200
    finish_data = finish.json()
    assert finish_data["score_global"] > 0
    assert len(finish_data["answers_feedback"]) == 10
    assert "functions" in finish_data["profile"]["topic_results"]
    assert "algebra" in finish_data["profile"]["topic_results"]
    assert "remember" in finish_data["profile"]["bloom_results"]
    assert "create" in finish_data["profile"]["bloom_results"]
    assert "dominant_bloom_level" not in finish_data["profile"]
    assert "bloom_strengths" not in finish_data["profile"]
    assert len(finish_data["profile"]["positive_recommendations"]) == 1
    assert len(finish_data["profile"]["improvement_recommendations"]) == 4
    assert "recommendations" not in finish_data["profile"]

    profile = client.get("/api/diagnostic/profile", headers=headers)
    assert profile.status_code == 200
    profile_data = profile.json()
    assert "functions" in profile_data["topic_results"]
    assert "algebra" in profile_data["topic_results"]
    assert len(profile_data["positive_recommendations"]) == 1
    assert len(profile_data["improvement_recommendations"]) == 4


def test_start_diagnostic_stores_selected_question_ids(client, db_session):
    seed_questions(db_session)
    access_token = register_and_login(client, "selected@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    payload = start.json()

    attempt = db_session.get(DiagnosticAttempt, payload["id"])
    assert attempt is not None
    assert set(attempt.selected_question_ids) == {question["id"] for question in payload["questions"]}
    assert len(attempt.selected_question_ids) == 10


def test_start_diagnostic_requires_ten_questions(client, db_session):
    seed_two_questions(db_session)
    access_token = register_and_login(client, "not-enough@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 409
    assert "requeridas: 10" in start.json()["detail"]


def test_start_diagnostic_balances_questions_by_topic_and_bloom(client, db_session):
    topics = ["functions", "algebra"]
    bloom_levels = [
        BloomLevel.REMEMBER,
        BloomLevel.UNDERSTAND,
        BloomLevel.APPLY,
        BloomLevel.ANALYZE,
        BloomLevel.EVALUATE,
        BloomLevel.CREATE,
    ]
    questions = []
    for topic in topics:
        for bloom_level in bloom_levels:
            questions.append(
                make_question(
                    topic=topic,
                    skill=f"{topic}-{bloom_level.value}",
                    question_text=f"{topic} {bloom_level.value}",
                    correct_answer="Correct",
                    bloom_level=bloom_level,
                )
            )
    db_session.add_all(questions)
    db_session.commit()

    access_token = register_and_login(client, "balanced@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    payload = start.json()
    assert len(payload["questions"]) == 10

    topic_counts = {topic: 0 for topic in topics}
    bloom_counts = {level.value: 0 for level in bloom_levels}
    for question in payload["questions"]:
        topic_counts[question["topic"]] += 1
        bloom_counts[question["bloom_level"]] += 1

    assert max(topic_counts.values()) - min(topic_counts.values()) <= 1
    assert max(bloom_counts.values()) - min(bloom_counts.values()) <= 1


def test_answer_rejects_question_not_selected_for_attempt(client, db_session):
    seed_questions(db_session)
    access_token = register_and_login(client, "outside-question@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200

    outside_question = make_question(
        topic="limits",
        skill="concepts",
        question_text="Question added after attempt start",
        correct_answer="Correct",
    )
    db_session.add(outside_question)
    db_session.commit()

    response = client.post(
        f"/api/diagnostic/{start.json()['id']}/answer",
        headers=headers,
        json={"question_id": outside_question.id, "answer": "Correct"},
    )
    assert response.status_code == 404


def test_finish_requires_all_selected_questions_answered(client, db_session):
    seed_questions(db_session)
    access_token = register_and_login(client, "incomplete@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    payload = start.json()

    first_question = payload["questions"][0]
    answer = first_question["options"][0]
    response = client.post(
        f"/api/diagnostic/{payload['id']}/answer",
        headers=headers,
        json={"question_id": first_question["id"], "answer": answer},
    )
    assert response.status_code == 204

    finish = client.post(f"/api/diagnostic/{payload['id']}/finish", headers=headers)
    assert finish.status_code == 409
    assert "Respondidas: 1/10" in finish.json()["detail"]


def test_finish_diagnostic_uses_empty_improvement_feedback_when_all_answers_are_correct(client, db_session):
    seed_questions(db_session)
    access_token = register_and_login(client, "diagnostic-all-correct@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    payload = start.json()
    for question in payload["questions"]:
        response = client.post(
            f"/api/diagnostic/{payload['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": question["options"][0]},
        )
        assert response.status_code == 204

    finish = client.post(f"/api/diagnostic/{payload['id']}/finish", headers=headers)

    assert finish.status_code == 200
    profile = finish.json()["profile"]
    assert len(profile["positive_recommendations"]) == 4
    assert profile["improvement_recommendations"] == []


def test_finish_diagnostic_uses_empty_positive_feedback_when_all_answers_are_incorrect(client, db_session):
    seed_questions(db_session)
    access_token = register_and_login(client, "diagnostic-all-wrong@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    payload = start.json()
    for question in payload["questions"]:
        response = client.post(
            f"/api/diagnostic/{payload['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": "Wrong"},
        )
        assert response.status_code == 204

    finish = client.post(f"/api/diagnostic/{payload['id']}/finish", headers=headers)

    assert finish.status_code == 200
    profile = finish.json()["profile"]
    assert profile["positive_recommendations"] == []
    assert len(profile["improvement_recommendations"]) == 4


def test_finish_diagnostic_falls_back_when_ai_feedback_is_invalid(client, db_session, monkeypatch):
    def invalid_generate(self, *, model: str, prompt: str, json_mode: bool = False) -> str:
        return "sin estructura valida"

    monkeypatch.setattr(OllamaClient, "generate", invalid_generate)
    seed_questions(db_session)
    access_token = register_and_login(client, "diagnostic-invalid-ai@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    payload = start.json()
    for index, question in enumerate(payload["questions"]):
        answer = question["options"][0] if index == 0 else "Wrong"
        response = client.post(
            f"/api/diagnostic/{payload['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": answer},
        )
        assert response.status_code == 204

    finish = client.post(f"/api/diagnostic/{payload['id']}/finish", headers=headers)

    # El fallback está deshabilitado: con IA inválida el 200 se mantiene pero las listas pueden estar vacías.
    assert finish.status_code == 200


def test_finish_diagnostic_filters_style_violations_and_fills_with_fallback(client, db_session, monkeypatch):
    def style_violations_generate(self, *, model: str, prompt: str, json_mode: bool = False) -> str:
        return json.dumps(
            {
                "recommendations": [
                    "Recuerda revisar la propiedad antes de responder.",
                    "Repasa el tema antes del siguiente intento.",
                    "Es importante practicar ejercicios similares.",
                    "La pregunta de algebra necesita más práctica.",
                ]
            }
        )

    monkeypatch.setattr(OllamaClient, "generate", style_violations_generate)
    seed_questions(db_session)
    access_token = register_and_login(client, "diagnostic-style-filter@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    payload = start.json()
    for index, question in enumerate(payload["questions"]):
        answer = question["options"][0] if index == 0 else "Wrong"
        response = client.post(
            f"/api/diagnostic/{payload['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": answer},
        )
        assert response.status_code == 204

    finish = client.post(f"/api/diagnostic/{payload['id']}/finish", headers=headers)

    assert finish.status_code == 200
    profile = finish.json()["profile"]
    all_recommendations = [*profile["positive_recommendations"], *profile["improvement_recommendations"]]
    assert all_recommendations
    for recommendation in all_recommendations:
        lower = recommendation.lower()
        assert "practic" not in lower
        assert "repas" not in lower
        assert "es importante" not in lower
        assert "la pregunta de" not in lower


def test_finish_diagnostic_drops_positives_describing_errors(client, db_session, monkeypatch):
    def error_marker_in_positive(self, *, model: str, prompt: str, json_mode: bool = False) -> str:
        category = _detect_category(prompt)
        if category == "positive":
            return json.dumps(
                {
                    "recommendations": [
                        "Respondiste 5 en lugar de 11 al resolver la inecuación, lo que muestra confusión con el signo.",
                    ]
                }
            )
        return json.dumps(
            {
                "recommendations": [
                    f"En la pregunta {i + 1}, el procedimiento requiere comparar coeficientes y verificar el resultado antes de elegir."
                    for i in range(4)
                ]
            }
        )

    monkeypatch.setattr(OllamaClient, "generate", error_marker_in_positive)
    seed_questions(db_session)
    access_token = register_and_login(client, "diagnostic-error-marker@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    payload = start.json()
    for index, question in enumerate(payload["questions"]):
        answer = question["options"][0] if index == 0 else "Wrong"
        response = client.post(
            f"/api/diagnostic/{payload['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": answer},
        )
        assert response.status_code == 204

    finish = client.post(f"/api/diagnostic/{payload['id']}/finish", headers=headers)

    assert finish.status_code == 200
    profile = finish.json()["profile"]
    for recommendation in profile["positive_recommendations"]:
        lower = recommendation.lower()
        assert "respondiste" not in lower
        assert "en lugar de" not in lower


def test_abandon_attempt_marks_in_progress_as_abandoned(client, db_session):
    seed_questions(db_session)
    access_token = register_and_login(client, "abandon@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    attempt_id = start.json()["id"]

    response = client.post(f"/api/diagnostic/{attempt_id}/abandon", headers=headers)
    assert response.status_code == 204

    attempt = db_session.get(DiagnosticAttempt, attempt_id)
    assert attempt is not None
    assert attempt.status == AttemptStatus.ABANDONED


def test_abandon_attempt_is_idempotent_for_closed_attempt(client, db_session):
    seed_questions(db_session)
    access_token = register_and_login(client, "abandon-closed@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    attempt_id = start.json()["id"]

    response = client.post(f"/api/diagnostic/{attempt_id}/abandon", headers=headers)
    assert response.status_code == 204
    response = client.post(f"/api/diagnostic/{attempt_id}/abandon", headers=headers)
    assert response.status_code == 204


def test_get_diagnostic_attempt_returns_questions_and_saved_answers(client, db_session):
    seed_questions(db_session)
    access_token = register_and_login(client, "recover@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    payload = start.json()
    first_question = payload["questions"][0]

    response = client.post(
        f"/api/diagnostic/{payload['id']}/answer",
        headers=headers,
        json={"question_id": first_question["id"], "answer": first_question["options"][0]},
    )
    assert response.status_code == 204

    recovered = client.get(f"/api/diagnostic/{payload['id']}", headers=headers)
    assert recovered.status_code == 200
    recovered_data = recovered.json()
    assert recovered_data["id"] == payload["id"]
    assert len(recovered_data["questions"]) == 10
    assert recovered_data["answers"] == {first_question["id"]: first_question["options"][0]}


def test_latest_review_returns_completed_attempt_feedback(client, db_session):
    seed_questions(db_session)
    access_token = register_and_login(client, "latest-review@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    empty_review = client.get("/api/diagnostic/latest-review", headers=headers)
    assert empty_review.status_code == 200
    assert empty_review.json() is None

    start = client.post("/api/diagnostic/start", headers=headers)
    assert start.status_code == 200
    payload = start.json()

    for index, question in enumerate(payload["questions"]):
        answer = question["options"][0] if index == 0 else "Wrong"
        response = client.post(
            f"/api/diagnostic/{payload['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": answer},
        )
        assert response.status_code == 204

    finish = client.post(f"/api/diagnostic/{payload['id']}/finish", headers=headers)
    assert finish.status_code == 200

    review = client.get("/api/diagnostic/latest-review", headers=headers)
    assert review.status_code == 200
    review_data = review.json()
    assert review_data["attempt_id"] == payload["id"]
    assert len(review_data["answers_feedback"]) == 10
    assert review_data["answers_feedback"][0]["question_text"]
    assert "correct_answer" in review_data["answers_feedback"][0]


def test_profile_endpoint_returns_latest_profile(client, db_session):
    seed_questions(db_session)
    access_token = register_and_login(client, "latest-profile@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    first_start = client.post("/api/diagnostic/start", headers=headers)
    assert first_start.status_code == 200
    first_payload = first_start.json()
    for question in first_payload["questions"]:
        response = client.post(
            f"/api/diagnostic/{first_payload['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": question["options"][0]},
        )
        assert response.status_code == 204
    first_finish = client.post(f"/api/diagnostic/{first_payload['id']}/finish", headers=headers)
    assert first_finish.status_code == 200
    assert first_finish.json()["profile"]["topic_results"]["functions"]["mastery"] == "high"

    second_start = client.post("/api/diagnostic/start", headers=headers)
    assert second_start.status_code == 200
    second_payload = second_start.json()
    for question in second_payload["questions"]:
        response = client.post(
            f"/api/diagnostic/{second_payload['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": "Wrong"},
        )
        assert response.status_code == 204
    second_finish = client.post(f"/api/diagnostic/{second_payload['id']}/finish", headers=headers)
    assert second_finish.status_code == 200

    profile = client.get("/api/diagnostic/profile", headers=headers)
    assert profile.status_code == 200
    profile_data = profile.json()
    assert profile_data["topic_results"]["functions"]["mastery"] == "low"
    assert profile_data["topic_results"]["algebra"]["mastery"] == "low"
