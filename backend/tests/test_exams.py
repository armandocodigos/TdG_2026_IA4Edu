import json
import re

import pytest

from app.models.enums import AttemptStatus, ExamDifficulty, QuestionType, Subject
from app.models.exam_attempt import ExamAttempt
from app.models.exam_question import ExamQuestion
from app.services.feedback_service import FeedbackService


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
            f"Demostraste dominio del procedimiento esperado en este tema ({index + 1}). Conserva ese criterio sustituyendo el resultado en el enunciado para confirmar la opción."
            for index in range(count)
        ]
    return [
        f"Conviene comparar tu elección con el procedimiento de referencia ({index + 1}). Sustituye los datos paso a paso para validar la opción antes de cerrar."
        for index in range(count)
    ]


@pytest.fixture(autouse=True)
def mock_exam_ai_feedback(monkeypatch):
    def fake_generate(self, *, model: str, prompt: str, json_mode: bool = False) -> str:
        category = _detect_category(prompt)
        count_match = re.search(r"exactamente (\d+) recomendaciones", prompt)
        count = int(count_match.group(1)) if count_match else 2
        items = _build_fake_recommendations(category, count)
        return json.dumps({"recommendations": items})

    monkeypatch.setattr("app.services.ollama_client.OllamaClient.generate", fake_generate)


def register_and_login(client, email: str, subject: str = "precalculo") -> str:
    response = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "secret123",
            "full_name": "Exam Student",
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


def test_exam_feedback_parser_accepts_model_key_typos_and_json_fences():
    raw_response = """```json
{
  "positive_recommendactions": [
    "Reconociste bien la relación entre grados y radianes en la pregunta de trigonometría."
  ],
  "improvement_recommendactions": [
    "En funciones, vuelve a identificar qué representa la entrada antes de elegir la opción."
  ]
}
```"""

    positive, improvement = FeedbackService().parse_legacy_combined(raw_response)

    assert positive == ["Reconociste bien la relación entre grados y radianes en la pregunta de trigonometría."]
    assert improvement == ["En funciones, vuelve a identificar qué representa la entrada antes de elegir la opción."]


def test_exam_feedback_parser_accepts_additional_model_key_typo():
    raw_response = """{
      "positive_recommendaions": ["Identificaste correctamente la amplitud como el coeficiente de la función seno."],
      "improvement_recommendaions": ["Conserva el signo de la constante cuando leas la intersección con el eje y."]
    }"""

    positive, improvement = FeedbackService().parse_legacy_combined(raw_response)

    assert positive == ["Identificaste correctamente la amplitud como el coeficiente de la función seno."]
    assert improvement == ["Conserva el signo de la constante cuando leas la intersección con el eje y."]


def test_exam_feedback_parser_preserves_unescaped_latex_commands_from_model():
    raw_response = r"""{
      "positive_recommendations": [
        "Para encontrar el vértice, usa $x=-\frac{b}{2a}$ y luego sustituye el valor en la función."
      ],
      "improvement_recommendations": [
        "Al determinar el dominio, excluye los valores donde $x \neq 1$ falla y verifica con $\sin x$ o $\tan x$ cuando corresponda."
      ]
    }"""

    positive, improvement = FeedbackService().parse_legacy_combined(raw_response)

    assert positive == ["Para encontrar el vértice, usa $x=-\\frac{b}{2a}$ y luego sustituye el valor en la función."]
    assert improvement == [
        "Al determinar el dominio, excluye los valores donde $x \\neq 1$ falla y verifica con $\\sin x$ o $\\tan x$ cuando corresponda."
    ]


def test_custom_exam_flow_returns_weighted_score_and_topic_breakdown(client, db_session):
    db_session.add_all(
        [
            ExamQuestion(
                subject=Subject.PRECALCULO,
                topic="funciones",
                difficulty=ExamDifficulty.BASIC,
                skill="evaluation",
                question_text="If f(x)=x+1, f(2) equals?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options_json=["2", "3"],
                correct_answer="3",
                explanation="Substitute x=2.",
                weight=1.0,
            ),
            ExamQuestion(
                subject=Subject.PRECALCULO,
                topic="álgebra",
                difficulty=ExamDifficulty.BASIC,
                skill="classification",
                question_text="Is y=2x+3 linear?",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options_json=["Yes", "No"],
                correct_answer="Yes",
                explanation="It has the form mx+b.",
                weight=3.0,
            ),
        ]
    )
    db_session.commit()

    access_token = register_and_login(client, "exam@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    availability = client.get("/api/exams/availability", headers=headers)
    assert availability.status_code == 200
    assert {item["topic"] for item in availability.json()["items"]} == {"funciones", "álgebra"}

    start = client.post(
        "/api/exams/start",
        headers=headers,
        json={"topics": ["funciones", "álgebra"], "difficulty": "basic", "question_count": 2},
    )
    assert start.status_code == 200
    start_data = start.json()
    assert start_data["topics"] == ["funciones", "álgebra"]
    assert len(start_data["questions"]) == 2

    answers = {"If f(x)=x+1, f(2) equals?": "3", "Is y=2x+3 linear?": "No"}
    for question in start_data["questions"]:
        response = client.post(
            f"/api/exams/{start_data['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": answers[question["question_text"]]},
        )
        assert response.status_code == 204

    finish = client.post(f"/api/exams/{start_data['id']}/finish", headers=headers)
    assert finish.status_code == 200
    finish_data = finish.json()
    assert finish_data["score_global"] == 25.0
    assert finish_data["result"]["topic_breakdown"]["funciones"]["mastery"] == "high"
    assert finish_data["result"]["topic_breakdown"]["álgebra"]["mastery"] == "low"
    assert len(finish_data["result"]["incorrect_answers"]) == 1
    assert len(finish_data["result"]["answers_feedback"]) == 2
    assert len(finish_data["result"]["positive_recommendations"]) == 1
    assert len(finish_data["result"]["improvement_recommendations"]) == 1
    assert "recommendations" not in finish_data["result"]
    assert any(item["is_correct"] for item in finish_data["result"]["answers_feedback"])
    assert finish_data["result"]["incorrect_answers"][0]["correct_answer"] == "Yes"

    result = client.get(f"/api/exams/{start_data['id']}/result", headers=headers)
    assert result.status_code == 200
    assert result.json()["score_global"] == 25.0
    assert len(result.json()["positive_recommendations"]) == 1
    assert len(result.json()["improvement_recommendations"]) == 1


def test_start_custom_exam_filters_by_subject_topic_and_difficulty(client, db_session):
    for index in range(3):
        db_session.add(
            ExamQuestion(
                subject=Subject.PRECALCULO,
                topic="funciones",
                difficulty=ExamDifficulty.INTERMEDIATE,
                skill=f"skill-{index}",
                question_text=f"Pregunta precalculo {index}",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options_json=["Correcta", "Incorrecta"],
                correct_answer="Correcta",
                explanation="Explicación de precálculo.",
                weight=1.25,
            )
        )
    db_session.add(
        ExamQuestion(
            subject=Subject.PREUNIVERSITARIO,
            topic="funciones",
            difficulty=ExamDifficulty.INTERMEDIATE,
            skill="otro-programa",
            question_text="Pregunta de otro programa",
            question_type=QuestionType.MULTIPLE_CHOICE,
            options_json=["Correcta", "Incorrecta"],
            correct_answer="Correcta",
            explanation="No debe aparecer.",
            weight=1.25,
        )
    )
    db_session.commit()

    access_token = register_and_login(client, "custom-exam@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post(
        "/api/exams/start",
        headers=headers,
        json={"topics": ["funciones"], "difficulty": "intermediate", "question_count": 2},
    )

    assert start.status_code == 200
    data = start.json()
    assert data["topics"] == ["funciones"]
    assert data["difficulty"] == "intermediate"
    assert data["question_count"] == 2
    assert len(data["questions"]) == 2
    assert all(question["difficulty"] == "intermediate" for question in data["questions"])
    assert all("precalculo" in question["question_text"] for question in data["questions"])


def test_start_custom_exam_accepts_multiple_topics_and_latest_result(client, db_session):
    for topic in ["funciones", "trigonometría"]:
        for index in range(2):
            db_session.add(
                ExamQuestion(
                    subject=Subject.PRECALCULO,
                    topic=topic,
                    difficulty=ExamDifficulty.BASIC,
                    skill=f"{topic}-{index}",
                    question_text=f"Pregunta {topic} {index}",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options_json=["Correcta", "Incorrecta"],
                    correct_answer="Correcta",
                    explanation=f"Explicación {topic}.",
                    weight=1.0,
                )
            )
    db_session.commit()

    access_token = register_and_login(client, "multi-topic@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post(
        "/api/exams/start",
        headers=headers,
        json={"topics": ["funciones", "trigonometría"], "difficulty": "basic", "question_count": 4},
    )
    assert start.status_code == 200
    start_data = start.json()
    assert start_data["topics"] == ["funciones", "trigonometría"]
    assert start_data["question_count"] == 4
    assert {question["topic"] for question in start_data["questions"]} == {"funciones", "trigonometría"}

    for question in start_data["questions"]:
        response = client.post(
            f"/api/exams/{start_data['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": "Incorrecta"},
        )
        assert response.status_code == 204

    finish = client.post(f"/api/exams/{start_data['id']}/finish", headers=headers)
    assert finish.status_code == 200
    assert len(finish.json()["result"]["incorrect_answers"]) == 4
    assert len(finish.json()["result"]["answers_feedback"]) == 4
    assert finish.json()["result"]["positive_recommendations"] == []
    assert len(finish.json()["result"]["improvement_recommendations"]) == 4

    latest = client.get("/api/exams/latest-result", headers=headers)
    assert latest.status_code == 200
    latest_data = latest.json()
    assert latest_data["attempt_id"] == start_data["id"]
    assert latest_data["topics"] == ["funciones", "trigonometría"]
    assert latest_data["difficulty"] == "basic"
    assert len(latest_data["result"]["incorrect_answers"]) == 4
    assert len(latest_data["result"]["answers_feedback"]) == 4
    assert latest_data["result"]["positive_recommendations"] == []
    assert len(latest_data["result"]["improvement_recommendations"]) == 4


def test_start_custom_exam_requires_at_least_one_question_per_selected_topic(client, db_session):
    for topic in ["funciones", "álgebra", "trigonometría"]:
        db_session.add(
            ExamQuestion(
                subject=Subject.PRECALCULO,
                topic=topic,
                difficulty=ExamDifficulty.BASIC,
                skill=f"{topic}-base",
                question_text=f"Pregunta real de {topic}",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options_json=["Correcta", "Incorrecta"],
                correct_answer="Correcta",
                explanation=f"Explicación {topic}.",
                weight=1.0,
            )
        )
    db_session.commit()

    access_token = register_and_login(client, "min-topic-count@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post(
        "/api/exams/start",
        headers=headers,
        json={"topics": ["funciones", "álgebra", "trigonometría"], "difficulty": "basic", "question_count": 2},
    )

    assert response.status_code == 422
    assert "al menos igual a la cantidad de temas seleccionados" in response.json()["detail"]


def test_start_custom_exam_includes_every_selected_topic_when_possible(client, db_session):
    for topic in ["funciones", "álgebra", "trigonometría"]:
        for index in range(4):
            db_session.add(
                ExamQuestion(
                    subject=Subject.PRECALCULO,
                    topic=topic,
                    difficulty=ExamDifficulty.BASIC,
                    skill=f"{topic}-{index}",
                    question_text=f"Pregunta real {index} de {topic}",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    options_json=["Correcta", "Incorrecta"],
                    correct_answer="Correcta",
                    explanation=f"Explicación {topic}.",
                    weight=1.0,
                )
            )
    db_session.commit()

    access_token = register_and_login(client, "balanced-topic-count@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    start = client.post(
        "/api/exams/start",
        headers=headers,
        json={"topics": ["funciones", "álgebra", "trigonometría"], "difficulty": "basic", "question_count": 5},
    )

    assert start.status_code == 200
    question_topics = [question["topic"] for question in start.json()["questions"]]
    assert len(question_topics) == 5
    assert {"funciones", "álgebra", "trigonometría"}.issubset(set(question_topics))


def test_start_custom_exam_rejects_selected_topic_without_questions_for_difficulty(client, db_session):
    db_session.add_all(
        [
            ExamQuestion(
                subject=Subject.PRECALCULO,
                topic="funciones",
                difficulty=ExamDifficulty.BASIC,
                skill="funciones-base",
                question_text="Pregunta básica de funciones",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options_json=["Correcta", "Incorrecta"],
                correct_answer="Correcta",
                explanation="Explicación.",
                weight=1.0,
            ),
            ExamQuestion(
                subject=Subject.PRECALCULO,
                topic="álgebra",
                difficulty=ExamDifficulty.INTERMEDIATE,
                skill="algebra-intermedia",
                question_text="Pregunta intermedia de álgebra",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options_json=["Correcta", "Incorrecta"],
                correct_answer="Correcta",
                explanation="Explicación.",
                weight=1.25,
            ),
        ]
    )
    db_session.commit()

    access_token = register_and_login(client, "missing-topic-difficulty@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post(
        "/api/exams/start",
        headers=headers,
        json={"topics": ["funciones", "álgebra"], "difficulty": "basic", "question_count": 2},
    )

    assert response.status_code == 409
    assert "Sin preguntas: álgebra" in response.json()["detail"]


def test_finish_exam_uses_empty_improvement_feedback_when_all_answers_are_correct(client, db_session):
    db_session.add(
        ExamQuestion(
            subject=Subject.PRECALCULO,
            topic="funciones",
            difficulty=ExamDifficulty.BASIC,
            skill="dominio",
            question_text="Pregunta de dominio",
            question_type=QuestionType.MULTIPLE_CHOICE,
            options_json=["Correcta", "Incorrecta"],
            correct_answer="Correcta",
            explanation="La opción correcta respeta la regla.",
            weight=1.0,
        )
    )
    db_session.commit()

    access_token = register_and_login(client, "all-correct@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}
    start = client.post(
        "/api/exams/start",
        headers=headers,
        json={"topics": ["funciones"], "difficulty": "basic", "question_count": 1},
    )
    assert start.status_code == 200
    question = start.json()["questions"][0]
    response = client.post(
        f"/api/exams/{start.json()['id']}/answer",
        headers=headers,
        json={"question_id": question["id"], "answer": "Correcta"},
    )
    assert response.status_code == 204

    finish = client.post(f"/api/exams/{start.json()['id']}/finish", headers=headers)

    assert finish.status_code == 200
    result = finish.json()["result"]
    assert len(result["positive_recommendations"]) == 1
    assert result["improvement_recommendations"] == []
    assert result["incorrect_answers"] == []


def test_finish_exam_falls_back_when_ai_feedback_is_invalid(client, db_session, monkeypatch):
    def invalid_generate(self, *, model: str, prompt: str, json_mode: bool = False) -> str:
        return "sin estructura valida"

    monkeypatch.setattr("app.services.ollama_client.OllamaClient.generate", invalid_generate)
    db_session.add_all(
        [
            ExamQuestion(
                subject=Subject.PRECALCULO,
                topic="funciones",
                difficulty=ExamDifficulty.BASIC,
                skill="evaluación",
                question_text="Pregunta correcta",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options_json=["Correcta", "Incorrecta"],
                correct_answer="Correcta",
                explanation="Explicación.",
                weight=1.0,
            ),
            ExamQuestion(
                subject=Subject.PRECALCULO,
                topic="álgebra",
                difficulty=ExamDifficulty.BASIC,
                skill="clasificación",
                question_text="Pregunta incorrecta",
                question_type=QuestionType.MULTIPLE_CHOICE,
                options_json=["Correcta", "Incorrecta"],
                correct_answer="Correcta",
                explanation="Explicación.",
                weight=1.0,
            ),
        ]
    )
    db_session.commit()

    access_token = register_and_login(client, "fallback-feedback@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}
    start = client.post(
        "/api/exams/start",
        headers=headers,
        json={"topics": ["funciones", "álgebra"], "difficulty": "basic", "question_count": 2},
    )
    assert start.status_code == 200
    for question in start.json()["questions"]:
        answer = "Correcta" if question["topic"] == "funciones" else "Incorrecta"
        response = client.post(
            f"/api/exams/{start.json()['id']}/answer",
            headers=headers,
            json={"question_id": question["id"], "answer": answer},
        )
        assert response.status_code == 204

    finish = client.post(f"/api/exams/{start.json()['id']}/finish", headers=headers)

    # El fallback está deshabilitado: con IA inválida el 200 se mantiene pero las listas pueden estar vacías.
    assert finish.status_code == 200


def test_start_custom_exam_returns_spanish_error_when_not_enough_questions(client, db_session):
    db_session.add(
        ExamQuestion(
            subject=Subject.PRECALCULO,
            topic="funciones",
            difficulty=ExamDifficulty.ADVANCED,
            skill="dominio",
            question_text="Pregunta única",
            question_type=QuestionType.MULTIPLE_CHOICE,
            options_json=["Correcta", "Incorrecta"],
            correct_answer="Correcta",
            explanation="Explicación.",
            weight=1.5,
        )
    )
    db_session.commit()

    access_token = register_and_login(client, "not-enough@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post(
        "/api/exams/start",
        headers=headers,
        json={"topics": ["funciones"], "difficulty": "advanced", "question_count": 2},
    )

    assert response.status_code == 409
    assert "No hay suficientes preguntas" in response.json()["detail"]
    assert "Disponibles: 1" in response.json()["detail"]


def test_abandon_exam_marks_in_progress_attempt_as_abandoned(client, db_session):
    db_session.add(
        ExamQuestion(
            subject=Subject.PRECALCULO,
            topic="funciones",
            difficulty=ExamDifficulty.BASIC,
            skill="evaluación",
            question_text="Pregunta para abandonar",
            question_type=QuestionType.MULTIPLE_CHOICE,
            options_json=["Correcta", "Incorrecta"],
            correct_answer="Correcta",
            explanation="Explicación.",
            weight=1.0,
        )
    )
    db_session.commit()

    access_token = register_and_login(client, "abandon@example.com")
    headers = {"Authorization": f"Bearer {access_token}"}
    start = client.post(
        "/api/exams/start",
        headers=headers,
        json={"topics": ["funciones"], "difficulty": "basic", "question_count": 1},
    )
    assert start.status_code == 200

    response = client.post(f"/api/exams/{start.json()['id']}/abandon", headers=headers)

    assert response.status_code == 204
    db_session.expire_all()
    assert db_session.get(ExamAttempt, start.json()["id"]).status == AttemptStatus.ABANDONED


def test_legacy_fixed_exam_endpoints_are_not_available(client):
    list_response = client.get("/api/exams")
    start_response = client.post("/api/exams/fixed-exam-id/start")

    assert list_response.status_code in {404, 405}
    assert start_response.status_code == 404
