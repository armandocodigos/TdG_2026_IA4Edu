from core.parsing.parser import MathParser
from core.pedagogy.state_tracker import AlgebraStateTracker
from core.tutoring.tutor import TutorSocratico

from core.classification.detector import (
    TopicDetector
)

from core.classification.resolver import (
    TopicResolver
)


def build_memory(turns):

    if not turns:
        return ""

    lines = []

    for index, turn in enumerate(turns[-6:], 1):

        lines.append(f"T{index}:")

        lines.append(
            f"Estudiante: "
            f"{turn['student']}"
        )

        lines.append(
            f"Estado pedagogico: "
            f"{turn['pedagogical_state']}"
        )

        lines.append(
            f"Tutor: "
            f"{turn['tutor']}"
        )

        lines.append("")

    return "\n".join(lines)


def choose_conversation_state(
    pedagogical_state,
    topic=None,
):

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


def specialize_exercise_state(
    state,
    topic=None,
):

    if state != "EJERCICIO":
        return state

    if topic == "functions":
        return "EJERCICIO_FUNCION"

    if topic == "trigonometry_basics":
        return "EJERCICIO_TRIG"

    return state


def detect_text_topic(
    message
):

    lower = (
        message
        or
        ""
    ).lower()

    if (
        "funcion" in lower
        or
        "función" in lower
        or
        "funciones" in lower
    ):

        return "functions"

    if (
        "trig" in lower
        or
        "seno" in lower
        or
        "coseno" in lower
        or
        "tangente" in lower
    ):

        return "trigonometry_basics"

    return None


def is_function_domain_intent(
    message
):

    lower = (
        message
        or
        ""
    ).lower()

    return (
        "dominio" in lower
        or
        "valores de x" in lower
        or
        "definida" in lower
        or
        "restriccion" in lower
        or
        "restricci" in lower
    )


def is_domain_interval_like(
    message
):

    lower = (
        message
        or
        ""
    ).lower()

    return (
        "infty" in lower
        or
        "\\infty" in lower
        or
        "∞" in lower
        or
        "infinito" in lower
        or
        (
            "," in lower
            and
            (
                "[" in lower
                or
                "(" in lower
            )
        )
    )


def is_function_domain_context(
    turns,
    message
):

    if is_function_domain_intent(
        message
    ):
        return True

    if is_domain_interval_like(
        message
    ):
        return True

    if not turns:
        return False

    return (
        turns[-1].get(
            "pedagogical_state"
        )
        ==
        "consulta_dominio"
    )


def is_function_validation_message(
    message
):

    lower = (
        message
        or
        ""
    ).lower()

    return (
        "f(" in lower
        or
        "f (" in lower
        or
        "resultado" in lower
        or
        "respuesta" in lower
        or
        "evalu" in lower
        or
        "sustit" in lower
        or
        "reemplaz" in lower
    )


def _legacy_detect_context_switch(
    message
):

    lower = (
        message
        or
        ""
    ).lower()

    wants_change = (
        "ahora" in lower
        or
        "cambiar" in lower
        or
        "cambiemos" in lower
        or
        "estudiemos" in lower
        or
        "quiero estudiar" in lower
        or
        "quiero practicar" in lower
    )

    if not wants_change:
        return None

    if "algebra" in lower:
        return "algebra"

    if (
        "precalculo" in lower
        or
        "precÃ¡lculo" in lower
    ):
        return "precalculo"

    if (
        "limite" in lower
        or
        "lÃ­mite" in lower
        or
        "limites" in lower
        or
        "lÃ­mites" in lower
    ):
        return "limits"

    topic = detect_text_topic(
        message
    )

    if topic:
        return topic

    return None


def is_new_exercise_intent(
    message
):

    lower = (
        message
        or
        ""
    ).lower()

    return (
        "tengo" in lower
        or
        "nueva" in lower
        or
        "nuevo" in lower
        or
        "otra" in lower
        or
        "otro" in lower
        or
        "sistema" in lower
        or
        "resolvamos" in lower
        or
        "hagamos" in lower
        or
        "ecuacion" in lower
        or
        "funcion" in lower
        or
        "funciones" in lower
    )


def is_explicit_exercise_switch(
    message
):

    lower = (
        message
        or
        ""
    ).lower()

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


def detect_context_switch(
    message
):

    lower = (
        message
        or
        ""
    ).lower()

    wants_change = (
        "ahora" in lower
        or
        "cambiar" in lower
        or
        "cambiemos" in lower
        or
        "estudiemos" in lower
        or
        "quiero estudiar" in lower
        or
        "quiero practicar" in lower
    )

    if not wants_change:
        return None

    if "algebra" in lower:
        return "algebra"

    if "prec" in lower:
        return "precalculo"

    if "limite" in lower or "limites" in lower:
        return "limits"

    topic = detect_text_topic(
        message
    )

    if topic:
        return topic

    return None


def classify_message_intent(
    message
):

    lower = (
        message
        or
        ""
    ).lower()

    study_topic = detect_context_switch(
        message
    )

    if study_topic:
        return {
            "kind": "topic_change",
            "topic": study_topic,
        }

    if is_function_domain_intent(
        message
    ):
        return {
            "kind": "function_domain",
            "topic": "functions",
        }

    new_exercise = (
        "tengo" in lower
        or
        "nueva" in lower
        or
        "nuevo" in lower
        or
        "otra" in lower
        or
        "otro" in lower
        or
        "sistema" in lower
        or
        "resolvamos" in lower
        or
        "hagamos" in lower
        or
        "ecuacion" in lower
        or
        "funcion" in lower
        or
        "funciones" in lower
    )

    if new_exercise:
        return {
            "kind": "new_exercise",
            "topic": detect_text_topic(
                message
            ),
        }

    return {
        "kind": "step",
        "topic": detect_text_topic(
            message
        ),
    }


def topic_from_intent(
    intent
):

    topic = (
        intent
        or
        {}
    ).get(
        "topic"
    )

    if topic in (
        "functions",
        "trigonometry_basics",
    ):
        return topic

    return None


def print_topic_info(topic_data):

    if not topic_data:
        return

    print("\nSistema curricular:")

    print(
        f"- Tema: "
        f"{topic_data['name']}"
    )

    print(
        f"- Dificultad: "
        f"{topic_data['difficulty']}"
    )

    print(
        f"- Skills: "
        f"{', '.join(topic_data['skills'])}"
    )

    print("")


def is_local_system_isolation_attempt(
    parser,
    previous_step,
    current_step,
):

    if not previous_step or not current_step:
        return False

    try:

        previous_parsed = parser.parse(
            previous_step
        )

        current_parsed = parser.parse(
            current_step
        )

        previous_expr = previous_parsed.sympy_expr
        current_expr = current_parsed.sympy_expr

        if isinstance(previous_expr, list):
            return False

        if isinstance(current_expr, list):
            return False

        if not (
            hasattr(previous_expr, "lhs")
            and
            hasattr(current_expr, "lhs")
        ):
            return False

        previous_symbols = previous_expr.free_symbols
        current_symbols = current_expr.free_symbols

        if len(previous_symbols) != 1:
            return False

        symbol = next(
            iter(previous_symbols)
        )

        return (
            current_expr.lhs == symbol
            and
            symbol in current_symbols
            and
            not current_expr.rhs.free_symbols
        )

    except Exception:
        return False


def should_remember_step(
    topic,
    state_result,
    current_step,
):

    if not state_result.mathematically_valid:
        return False

    if topic == "functions":
        return False

    if topic in (
        "linear_system",
        "nonlinear_system",
    ):

        return state_result.pedagogical_state in (
            "avance_valido",
            "solucion_parcial_sistema",
        )

    return True


def main():

    parser = MathParser()

    tracker = AlgebraStateTracker()

    tutor = TutorSocratico()

    topic_detector = TopicDetector()

    topic_resolver = TopicResolver()

    active_equation = None

    previous_step = None

    active_topic = None

    active_topic_data = None

    turns = []


    exercise_completed = False

    print("\n=== Chat integrado algebra + tutor ===")

    print(
        "Escribe una ecuacion para iniciar, "
        "por ejemplo: 2x + 5 = 0"
    )

    print(
        "Luego escribe tus pasos uno por uno."
    )

    print(
        "Comandos: "
        "salir, estado, reiniciar, "
        "precalculo\n"
    )

    while True:

        message = input(
            "Estudiante: "
        ).strip()

        if not message:
            continue

        intent = classify_message_intent(
            message
        )

        ####################################################
        # SALIR
        ####################################################

        if message.lower() == "salir":
            break

        ####################################################
        # REINICIAR
        ####################################################

        if message.lower() == "reiniciar":

            active_equation = None

            previous_step = None

            active_topic = None

            active_topic_data = None

            turns = []

            tracker.history = []

            exercise_completed = False

            print(
                "Sistema: sesion reiniciada."
            )

            continue

        ####################################################
        # ESTADO
        ####################################################

        if message.lower() == "estado":

            print(
                f"Ecuacion activa: "
                f"{active_equation or 'ninguna'}"
            )

            print(
                f"Paso anterior: "
                f"{previous_step or 'ninguno'}"
            )

            print(
                f"Topic activo: "
                f"{active_topic or 'ninguno'}"
            )

            print(
                "Ejercicio completado: "
                f"{'si' if exercise_completed else 'no'}"
            )

            print_topic_info(
                active_topic_data
            )

            continue

        ####################################################
        # NUEVO EJERCICIO
        ####################################################

        if message.lower() in (
            "otro",
            "otro ejercicio"
        ):

            active_equation = None

            previous_step = None

            active_topic = None

            active_topic_data = None

            tracker.history = []

            exercise_completed = False

            response = tutor.responder(

                mensaje=(
                    "El estudiante quiere practicar "
                    "otro ejercicio."
                ),

                memoria=build_memory(turns),

                estado="EXPLORAR",

                pedagogical_state="",

                ecuacion="",
            )

            turns.append({

                "student":
                message,

                "pedagogical_state":
                "solicitud_nuevo_ejercicio",

                "tutor":
                response,
            })

            print(
                f"Tutor: "
                f"{response}\n"
            )

            continue

        ####################################################
        # PRECALCULO
        ####################################################

        if message.lower() in (
            "precalculo",
            "precálculo",
            "limites",
            "límites"
        ):

            active_equation = None

            previous_step = None

            active_topic = None

            active_topic_data = None

            tracker.history = []

            exercise_completed = False

            response = tutor.responder(

                mensaje=(
                    "Quiero cambiar "
                    "a un tema de precalculo, "
                    "por ejemplo limites."
                ),

                memoria=build_memory(turns),

                estado="EXPLORAR",

                pedagogical_state="",

                ecuacion="",
            )

            turns.append({

                "student":
                message,

                "pedagogical_state":
                "cambio_tema_precalculo",

                "tutor":
                response,
            })

            print(
                "Sistema: "
                "cambiando a exploracion "
                "de precalculo."
            )

            print(
                f"Tutor: "
                f"{response}\n"
            )

            continue

        ####################################################
        # CAMBIO EXPLICITO DE CONTEXTO
        ####################################################

        context_switch = intent.get(
            "topic"
        )

        if (
            intent["kind"] == "topic_change"
            and
            active_equation is not None
        ):

            active_equation = None

            previous_step = None

            active_topic = None

            active_topic_data = None

            tracker.history = []

            turns = []

            exercise_completed = False

            active_topic = topic_from_intent(
                intent
            )

            active_topic_data = topic_resolver.resolve(
                active_topic
            )

            response = tutor.responder(

                mensaje=message,

                memoria=build_memory(
                    turns
                ),

                estado="EXPLORAR",

                pedagogical_state="cambio_contexto",

                ecuacion="",
            )

            turns.append({

                "student":
                message,

                "pedagogical_state":
                "cambio_contexto",

                "tutor":
                response,
            })

            print(
                "Sistema: "
                f"cambio de contexto={context_switch}"
            )

            print(
                f"Tutor: "
                f"{response}\n"
            )

            continue

        ####################################################
        # PARSER
        ####################################################

        parsed = parser.parse(
            message
        )

        topic_id = topic_detector.detect(
            parsed
        )

        if topic_id is None:

            topic_id = detect_text_topic(
                message
            )

        topic_data = topic_resolver.resolve(
            topic_id
        )

        if (
            active_equation is None
            and
            topic_id is not None
        ):

            active_topic = topic_id

            active_topic_data = topic_data

        if topic_id is None:

            print(
                "Sistema: "
                "topic no detectado."
            )

        ####################################################
        # INICIO DE EJERCICIO
        ####################################################

        if active_equation is None:

            if (
                parsed.success
                and
                parsed.sympy_expr is not None
            ):

                active_equation = (
                    parsed.extracted_math
                )

                previous_step = (
                    parsed.extracted_math
                )

                exercise_completed = False

                active_topic = topic_id

                active_topic_data = topic_data

                if active_topic_data:

                    print(
                        "Sistema: "
                        f"topic detectado="
                        f"{active_topic_data['name']}"
                    )

                response = tutor.responder(

                    mensaje=message,

                    memoria=build_memory(
                        turns
                    ),

                    estado=specialize_exercise_state(
                        "EJERCICIO",
                        active_topic,
                    ),

                    pedagogical_state="",

                    ecuacion=active_equation,
                )

                turns.append({

                    "student":
                    message,

                    "pedagogical_state":
                    "inicio_ejercicio",

                    "tutor":
                    response,
                })

                print(
                    f"Tutor: "
                    f"{response}\n"
                )

                print_topic_info(
                    active_topic_data
                )

                continue

            # Si el estudiante mencionó un tema,
            # pasar el topic detectado como contexto
            explorar_mensaje = message

            context_topic = (
                topic_id
                or
                active_topic
            )

            if context_topic:

                explorar_mensaje = (
                    f"[tema detectado: {context_topic}] "
                    f"{message}"
                )

            response = tutor.responder(

                mensaje=explorar_mensaje,

                memoria=build_memory(
                    turns
                ),

                estado="EXPLORAR",

                pedagogical_state="",

                ecuacion="",
            )

            turns.append({

                "student":
                message,

                "pedagogical_state":
                "sin_ejercicio",

                "tutor":
                response,
            })

            print(
                f"Tutor: "
                f"{response}\n"
            )

            continue

        ####################################################
        # PARSE FALLIDO — texto conversacional
        ####################################################

        if not parsed.success:

            if (
                (
                    intent["kind"] == "function_domain"
                    or
                    is_function_domain_context(
                        turns,
                        message
                    )
                )
                and
                active_topic == "functions"
                and
                active_equation
            ):

                response = tutor.responder(

                    mensaje=message,

                    memoria=build_memory(
                        turns
                    ),

                    estado="EJERCICIO_DOMINIO_FUNCION",

                    pedagogical_state="consulta_dominio",

                    ecuacion=active_equation or "",
                )

                turns.append({

                    "student":
                    message,

                    "pedagogical_state":
                    "consulta_dominio",

                    "tutor":
                    response,
                })

                print(
                    "Sistema: "
                    "estado=EJERCICIO_DOMINIO_FUNCION, "
                    "pedagogico=consulta_dominio"
                )

                print(
                    f"Tutor: "
                    f"{response}\n"
                )

                continue

            if (
                active_topic == "functions"
                and
                active_equation
                and
                not is_function_validation_message(
                    message
                )
            ):

                response = tutor.responder(

                    mensaje=message,

                    memoria=build_memory(
                        turns
                    ),

                    estado="EJERCICIO_FUNCION",

                    pedagogical_state="entrada_no_parseada",

                    ecuacion=active_equation or "",
                )

                turns.append({

                    "student":
                    message,

                    "pedagogical_state":
                    "entrada_no_parseada",

                    "tutor":
                    response,
                })

                print(
                    "Sistema: "
                    "estado=EJERCICIO_FUNCION, "
                    "pedagogico=entrada_no_parseada"
                )

                print(
                    f"Tutor: "
                    f"{response}\n"
                )

                continue

            if (
                active_topic in (
                    "functions",
                    "trigonometry_basics",
                )
                and
                active_equation
            ):

                state_result = tracker.analyze_step(
                    (
                        active_equation
                        if active_topic == "functions"
                        else previous_step
                    ),
                    message,
                    topic=active_topic,
                )

                conversation_state = (
                    choose_conversation_state(
                        state_result.pedagogical_state,
                        topic=active_topic,
                    )
                )

                conversation_state = specialize_exercise_state(
                    conversation_state,
                    active_topic,
                )

                response = tutor.responder(

                    mensaje=message,

                    memoria=build_memory(
                        turns
                    ),

                    estado=conversation_state,

                    pedagogical_state=(
                        state_result.pedagogical_state
                    ),

                    ecuacion=active_equation or "",
                )

                turns.append({

                    "student":
                    message,

                    "pedagogical_state":
                    state_result.pedagogical_state,

                    "tutor":
                    response,
                })

                if (
                    state_result.pedagogical_state
                    ==
                    "solucion_final"
                ):

                    exercise_completed = True

                print(
                    "Sistema: "
                    f"estado={conversation_state}, "
                    f"pedagogico="
                    f"{state_result.pedagogical_state}, "
                    f"transformacion="
                    f"{state_result.transformation}"
                )

                print(
                    f"Tutor: "
                    f"{response}\n"
                )

                continue

            # Si el mensaje es texto sin matemáticas,
            # responder en modo conversacional, no como ejercicio
            estado_parse = (
                "EJERCICIO"
                if active_equation
                else "EXPLORAR"
            )

            estado_parse = specialize_exercise_state(
                estado_parse,
                active_topic,
            )

            response = tutor.responder(

                mensaje=message,

                memoria=build_memory(
                    turns
                ),

                estado=estado_parse,

                pedagogical_state="entrada_no_parseada",

                ecuacion=active_equation or "",
            )

            turns.append({

                "student":
                message,

                "pedagogical_state":
                "entrada_no_parseada",

                "tutor":
                response,
            })

            print(
                f"Tutor: "
                f"{response}\n"
            )

            continue

        ####################################################
        # ANALISIS ALGEBRAICO
        ####################################################

        current_step = (
            parsed.extracted_math
        )

        if (
            active_equation is not None
            and
            intent["kind"] == "new_exercise"
            and
            parsed.success
            and
            current_step != previous_step
            and
            (
                exercise_completed
                or
                is_explicit_exercise_switch(
                    message
                )
            )
        ):

            active_equation = current_step

            previous_step = current_step

            exercise_completed = False

            active_topic = topic_id

            active_topic_data = topic_data

            turns = []

            response = tutor.responder(

                mensaje=message,

                memoria=build_memory(
                    turns
                ),

                estado=specialize_exercise_state(
                    "EJERCICIO",
                    active_topic,
                ),

                pedagogical_state="inicio_ejercicio",

                ecuacion=active_equation,
            )

            turns.append({

                "student":
                message,

                "pedagogical_state":
                "inicio_ejercicio",

                "tutor":
                response,
            })

            print(
                "Sistema: "
                "nuevo ejercicio detectado automaticamente."
            )

            print(
                f"Tutor: "
                f"{response}\n"
            )

            print_topic_info(
                active_topic_data
            )

            continue

        validation_previous_step = previous_step
        using_local_system_context = False

        if active_topic == "functions":

            validation_previous_step = active_equation

        elif active_topic in (
            "linear_system",
            "nonlinear_system",
        ):

            using_local_system_context = (
                is_local_system_isolation_attempt(
                    parser,
                    previous_step,
                    current_step,
                )
            )

            validation_previous_step = (
                previous_step
                if using_local_system_context
                else active_equation
            )

        state_result = (
            tracker.analyze_step(

                validation_previous_step,

                (
                    message
                    if active_topic == "functions"
                    else current_step
                ),

                topic=active_topic,
            )
        )

        if (
            using_local_system_context
            and
            state_result.pedagogical_state
            ==
            "solucion_final"
        ):

            state_result.pedagogical_state = (
                "solucion_parcial_sistema"
            )

        conversation_state = (
            choose_conversation_state(
                state_result.pedagogical_state,
                topic=active_topic,
            )
        )

        conversation_state = specialize_exercise_state(
            conversation_state,
            active_topic,
        )

        ####################################################
        # RESPUESTA TUTOR
        ####################################################

        response = tutor.responder(

            mensaje=message,

            memoria=build_memory(
                turns
            ),

            estado=conversation_state,

            pedagogical_state=(
                state_result.pedagogical_state
            ),

            ecuacion=active_equation,
        )

        turns.append({

            "student":
            message,

            "pedagogical_state":
            state_result.pedagogical_state,

            "tutor":
            response,
        })

        ####################################################
        # UPDATE STEP
        ####################################################

        if should_remember_step(
            active_topic,
            state_result,
            current_step,
        ):

            previous_step = current_step

        ####################################################
        # EJERCICIO COMPLETADO
        ####################################################

        if (
            state_result.pedagogical_state
            ==
            "solucion_final"
        ):

            exercise_completed = True

        ####################################################
        # DEBUG
        ####################################################

        print(
            "Sistema: "
            f"estado={conversation_state}, "
            f"pedagogico="
            f"{state_result.pedagogical_state}, "
            f"transformacion="
            f"{state_result.transformation}"
        )

        print(
            f"Tutor: "
            f"{response}\n"
        )

        print_topic_info(
            active_topic_data
        )

        ####################################################
        # SIGUIENTE EJERCICIO
        ####################################################

        if exercise_completed:

            print(
                "Sistema: "
                "ejercicio completado. "
                "Escribe 'precalculo' para cambiar "
                "de tema o ingresa una nueva ecuacion.\n"
            )


if __name__ == "__main__":

    main()
