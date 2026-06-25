from dataclasses import dataclass, field
from pathlib import Path
import sys
from time import perf_counter

from app.schemas.fast_chat import FastChatRequest, FastChatResponse
from app.models.user import User

SOCRATIC_MODEL_PATH = Path(__file__).resolve().parents[3] / "socratic_model"
if str(SOCRATIC_MODEL_PATH) not in sys.path:
    sys.path.insert(0, str(SOCRATIC_MODEL_PATH))

from core.classification.detector import TopicDetector
from core.config import MODEL
from core.parsing.parser import MathParser
from core.pedagogy.state_tracker import AlgebraStateTracker
from core.tutoring.tutor import TutorSocratico


def build_memory(turns: list[dict[str, str]]) -> str:
    if not turns:
        return ""

    lines: list[str] = []
    for index, turn in enumerate(turns[-6:], 1):
        lines.extend(
            [
                f"T{index}:",
                f"Estudiante: {turn['student']}",
                f"Estado pedagogico: {turn['pedagogical_state']}",
                f"Tutor: {turn['tutor']}",
                "",
            ]
        )
    return "\n".join(lines)


def detect_text_topic(message: str | None) -> str | None:
    lower = (message or "").lower()
    if "funcion" in lower or "función" in lower or "funciones" in lower:
        return "functions"
    if "trig" in lower or "seno" in lower or "coseno" in lower or "tangente" in lower:
        return "trigonometry_basics"
    return None


def is_function_domain_intent(message: str | None) -> bool:
    lower = (message or "").lower()
    return any(
        marker in lower
        for marker in (
            "dominio",
            "valores de x",
            "definida",
            "restriccion",
            "restricci",
        )
    )


def is_function_validation_message(message: str | None) -> bool:
    lower = (message or "").lower()
    return any(
        marker in lower
        for marker in (
            "f(",
            "f (",
            "resultado",
            "respuesta",
            "evalu",
            "sustit",
            "reemplaz",
        )
    )


def is_explicit_exercise_switch(message: str | None) -> bool:
    lower = (message or "").lower()
    return any(
        phrase in lower
        for phrase in (
            "cambiemos de ejercicio",
            "cambiar de ejercicio",
            "otro ejercicio",
            "nuevo ejercicio",
            "nueva ecuacion",
            "nueva ecuación",
            "hagamos otro",
            "resolvamos el siguiente",
            "tengo el sistema",
            "tengo la ecuacion",
            "tengo la ecuación",
            "la ecuacion es",
            "la ecuación es",
        )
    )


def detect_context_switch(message: str | None) -> str | None:
    lower = (message or "").lower()
    wants_change = any(
        marker in lower
        for marker in (
            "ahora",
            "cambiar",
            "cambiemos",
            "estudiemos",
            "quiero estudiar",
            "quiero practicar",
        )
    )
    if not wants_change:
        return None
    if "algebra" in lower:
        return "algebra"
    if "prec" in lower:
        return "precalculo"
    if "limite" in lower or "limites" in lower:
        return "limits"
    return detect_text_topic(message)


def classify_message_intent(message: str | None) -> dict[str, str | None]:
    lower = (message or "").lower()
    study_topic = detect_context_switch(message)
    if study_topic:
        return {"kind": "topic_change", "topic": study_topic}
    if is_function_domain_intent(message):
        return {"kind": "function_domain", "topic": "functions"}
    if any(
        marker in lower
        for marker in (
            "tengo",
            "nueva",
            "nuevo",
            "otra",
            "otro",
            "sistema",
            "resolvamos",
            "hagamos",
            "ecuacion",
            "funcion",
            "funciones",
        )
    ):
        return {"kind": "new_exercise", "topic": detect_text_topic(message)}
    return {"kind": "step", "topic": detect_text_topic(message)}


def topic_from_intent(intent: dict[str, str | None]) -> str | None:
    topic = intent.get("topic")
    if topic in ("functions", "trigonometry_basics"):
        return topic
    return None


def choose_conversation_state(pedagogical_state: str, topic: str | None = None) -> str:
    if pedagogical_state in (
        "paso_incorrecto",
        "error_sustitucion_funcion",
        "error_operacion_funcion",
    ):
        if topic == "trigonometry_basics":
            return "CORREGIR_TRIG"
        if topic == "functions":
            return "CORREGIR_FUNCION"
        return "CORREGIR"
    if pedagogical_state == "solucion_final":
        return "COMPLETADO"
    return "EJERCICIO"


def specialize_exercise_state(state: str, topic: str | None = None) -> str:
    if state != "EJERCICIO":
        return state
    if topic == "functions":
        return "EJERCICIO_FUNCION"
    if topic == "trigonometry_basics":
        return "EJERCICIO_TRIG"
    return state


def should_remember_step(topic: str | None, state_result, current_step: str) -> bool:
    if not state_result.mathematically_valid:
        return False
    if topic == "functions":
        return False
    if topic in ("linear_system", "nonlinear_system"):
        return state_result.pedagogical_state in (
            "avance_valido",
            "solucion_parcial_sistema",
        )
    return bool(current_step)


@dataclass
class SocraticSession:
    parser: MathParser = field(default_factory=MathParser)
    tracker: AlgebraStateTracker = field(default_factory=AlgebraStateTracker)
    tutor: TutorSocratico = field(default_factory=TutorSocratico)
    topic_detector: TopicDetector = field(default_factory=TopicDetector)
    active_equation: str | None = None
    previous_step: str | None = None
    active_topic: str | None = None
    turns: list[dict[str, str]] = field(default_factory=list)
    exercise_completed: bool = False


class SocraticTutorService:
    _sessions: dict[str, SocraticSession] = {}

    def answer(
        self,
        *,
        user: User,
        payload: FastChatRequest,
        extracted_content: str | None = None,
    ) -> FastChatResponse:
        started_at = perf_counter()
        session = self._sessions.setdefault(str(user.id), SocraticSession())
        message = payload.query.strip()
        if extracted_content:
            message = f"{message}\n\nContenido adjunto:\n{extracted_content}"

        answer = self._answer_with_session(session, message)
        return FastChatResponse(
            answer=answer,
            model_used=MODEL,
            rag_enabled=payload.use_rag,
            context_count=0,
            sources=[],
            rag_metadata=[],
            latency_ms=int((perf_counter() - started_at) * 1000),
        )

    def _answer_with_session(self, session: SocraticSession, message: str) -> str:
        intent = classify_message_intent(message)

        if message.lower() in ("reiniciar", "reset"):
            self._reset(session)
            return "Sesion reiniciada. Que ejercicio quieres trabajar?"

        if message.lower() in ("otro", "otro ejercicio"):
            self._reset(session, keep_turns=True)
            return self._respond(
                session,
                message="El estudiante quiere practicar otro ejercicio.",
                state="EXPLORAR",
                pedagogical_state="solicitud_nuevo_ejercicio",
                equation="",
                student_message=message,
            )

        if intent["kind"] == "topic_change" and session.active_equation is not None:
            self._reset(session)
            session.active_topic = topic_from_intent(intent)
            return self._respond(
                session,
                message=message,
                state="EXPLORAR",
                pedagogical_state="cambio_contexto",
                equation="",
                student_message=message,
            )

        parsed = session.parser.parse(message)
        topic_id = session.topic_detector.detect(parsed) or detect_text_topic(message)

        if session.active_equation is None:
            if parsed.success and parsed.sympy_expr is not None:
                session.active_equation = parsed.extracted_math
                session.previous_step = parsed.extracted_math
                session.exercise_completed = False
                session.active_topic = topic_id
                return self._respond(
                    session,
                    message=message,
                    state=specialize_exercise_state("EJERCICIO", session.active_topic),
                    pedagogical_state="inicio_ejercicio",
                    equation=session.active_equation,
                    student_message=message,
                )

            explorar_mensaje = message
            context_topic = topic_id or session.active_topic
            if context_topic:
                explorar_mensaje = f"[tema detectado: {context_topic}] {message}"
            return self._respond(
                session,
                message=explorar_mensaje,
                state="EXPLORAR",
                pedagogical_state="sin_ejercicio",
                equation="",
                student_message=message,
            )

        if not parsed.success:
            return self._handle_unparsed_message(session, message, intent)

        current_step = parsed.extracted_math
        if (
            intent["kind"] == "new_exercise"
            and current_step != session.previous_step
            and (session.exercise_completed or is_explicit_exercise_switch(message))
        ):
            session.active_equation = current_step
            session.previous_step = current_step
            session.exercise_completed = False
            session.active_topic = topic_id
            session.turns = []
            return self._respond(
                session,
                message=message,
                state=specialize_exercise_state("EJERCICIO", session.active_topic),
                pedagogical_state="inicio_ejercicio",
                equation=session.active_equation,
                student_message=message,
            )

        validation_previous_step = session.active_equation if session.active_topic == "functions" else session.previous_step
        state_result = session.tracker.analyze_step(
            validation_previous_step,
            message if session.active_topic == "functions" else current_step,
            topic=session.active_topic,
        )
        conversation_state = specialize_exercise_state(
            choose_conversation_state(state_result.pedagogical_state, topic=session.active_topic),
            session.active_topic,
        )
        response = self._respond(
            session,
            message=message,
            state=conversation_state,
            pedagogical_state=state_result.pedagogical_state,
            equation=session.active_equation or "",
            student_message=message,
        )

        if should_remember_step(session.active_topic, state_result, current_step):
            session.previous_step = current_step
        if state_result.pedagogical_state == "solucion_final":
            session.exercise_completed = True
        return response

    def _handle_unparsed_message(
        self,
        session: SocraticSession,
        message: str,
        intent: dict[str, str | None],
    ) -> str:
        if (
            intent["kind"] == "function_domain"
            and session.active_topic == "functions"
            and session.active_equation
        ):
            return self._respond(
                session,
                message=message,
                state="EJERCICIO_DOMINIO_FUNCION",
                pedagogical_state="consulta_dominio",
                equation=session.active_equation,
                student_message=message,
            )

        if (
            session.active_topic == "functions"
            and session.active_equation
            and not is_function_validation_message(message)
        ):
            return self._respond(
                session,
                message=message,
                state="EJERCICIO_FUNCION",
                pedagogical_state="entrada_no_parseada",
                equation=session.active_equation,
                student_message=message,
            )

        if session.active_topic in ("functions", "trigonometry_basics") and session.active_equation:
            state_result = session.tracker.analyze_step(
                session.active_equation if session.active_topic == "functions" else session.previous_step,
                message,
                topic=session.active_topic,
            )
            conversation_state = specialize_exercise_state(
                choose_conversation_state(state_result.pedagogical_state, topic=session.active_topic),
                session.active_topic,
            )
            if state_result.pedagogical_state == "solucion_final":
                session.exercise_completed = True
            return self._respond(
                session,
                message=message,
                state=conversation_state,
                pedagogical_state=state_result.pedagogical_state,
                equation=session.active_equation,
                student_message=message,
            )

        return self._respond(
            session,
            message=message,
            state=specialize_exercise_state("EJERCICIO", session.active_topic),
            pedagogical_state="entrada_no_parseada",
            equation=session.active_equation or "",
            student_message=message,
        )

    def _respond(
        self,
        session: SocraticSession,
        *,
        message: str,
        state: str,
        pedagogical_state: str,
        equation: str,
        student_message: str,
    ) -> str:
        response = session.tutor.responder(
            mensaje=message,
            memoria=build_memory(session.turns),
            estado=state,
            pedagogical_state=pedagogical_state,
            ecuacion=equation,
        )
        session.turns.append(
            {
                "student": student_message,
                "pedagogical_state": pedagogical_state,
                "tutor": response,
            }
        )
        return response

    def _reset(self, session: SocraticSession, *, keep_turns: bool = False) -> None:
        session.active_equation = None
        session.previous_step = None
        session.active_topic = None
        session.tracker.history = []
        session.exercise_completed = False
        if not keep_turns:
            session.turns = []
