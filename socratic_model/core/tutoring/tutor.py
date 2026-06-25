# ============================================================
# TUTOR — Tutor Socrático
# Ahora integrado con:
# - estado conversacional
# - estado pedagógico algebraico
# - memoria
# - prompts defensivos
# ============================================================

import requests
import time
import re

from core.logging.tutor_logger import (
    log_tutor
)

from core.config import (
    OLLAMA_URL,
    MODEL,
    TUTOR_TEMPERATURE,
    TUTOR_TOP_P,
    TUTOR_REPEAT_PENALTY,
    TUTOR_NUM_PREDICT,
    TUTOR_TIMEOUT_SECONDS,
)

# ============================================================
# INSTRUCCIONES POR ESTADO CONVERSACIONAL
# ============================================================

INSTRUCCIONES_ESTADO = {

    "EXPLORAR": """
El estudiante no tiene un ejercicio activo.
Si el mensaje incluye "[tema detectado: ...]", pídele directamente
que escriba un ejercicio o problema concreto de ese tema.
Ejemplo: "Escríbeme el problema que quieres resolver."
Si no hay tema detectado, pregunta brevemente qué quiere practicar.
Una sola pregunta corta y directa.
""",

    "EJERCICIO": """
El estudiante está resolviendo paso a paso.
Haz la pregunta MÁS PEQUEÑA posible para llevarlo al siguiente paso.
No expliques. No des contexto innecesario. Solo guía.
""",

    "CORREGIR": """
El estudiante cometió un error algebraico.
Haz UNA pregunta corta y específica sobre el signo o la operación.
Ejemplo: "¿Qué pasa con el signo cuando pasas el 5 al otro lado?"
NO avances hasta que corrija.
""",

    "CORREGIR_TRIG": """
El estudiante cometió un error en trigonometría.
Parte de lo que el estudiante YA sabe.
Haz la pregunta más pequeña posible.
Ejemplo: "Seno es opuesto sobre ¿qué?"
NO des el valor correcto.
""",

    "CORREGIR_FUNCION": """
El estudiante cometió un error con funciones.
Haz una pregunta corta sobre la sustitución o la operación específica.
Ejemplo: "¿Qué valor pusiste en lugar de x?"
NO des el resultado correcto.
""",

    "COMPLETADO": """
El estudiante terminó correctamente.
Felicítalo en una línea corta y natural.
Pregunta si quiere otro ejercicio o cambiar de tema.
""",

    "NUEVO": """
El estudiante quiere otro ejercicio.
Pregúntale sobre qué tema o tipo de problema quiere practicar.
Una sola pregunta breve.
""",
}


# ============================================================
# INSTRUCCIONES PEDAGÓGICAS
# ============================================================

INSTRUCCIONES_PEDAGOGICAS = {

    "avance_valido": """
El estudiante avanzó correctamente.
Reconócelo brevemente en 2-4 palabras ("Sí", "Bien", "Vas bien").
Luego haz la pregunta más pequeña posible para el siguiente paso.
Ejemplo: "Bien, ya tienes 3c = 18. ¿Qué harías ahora?"
""",

    "retroceso": """
El estudiante regresó a un paso anterior.
Díselo con naturalidad en una línea.
Ejemplo: "Eso es lo mismo que tenías antes, ¿qué querías lograr?"
""",

    "repeticion": """
El estudiante repitió el mismo paso.
Rompe el estancamiento con una pregunta diferente y más concreta.
""",

    "solucion_parcial": """
El estudiante encontró una solución parcial.
NO digas que terminó.
Pregunta brevemente si hay otra solución.
Ejemplo: "¿Esa es la única solución posible?"
""",

    "solucion_final": """
El estudiante llegó a la solución correcta.
Felicítalo en una línea corta y natural.
Ofrece otro ejercicio o cambiar de tema.
""",

    "paso_incorrecto": """
El paso tiene un error.
NO lo corrijas directamente.
Haz la pregunta más pequeña posible sobre el error específico.
Nivel 1: "¿Estás seguro del signo ahí?"
Nivel 2: "¿Qué operación hiciste con el 5?"
Nivel 3: "Si sumas 5 a ambos lados, ¿qué queda?"
Empieza siempre por Nivel 1.
""",

    "equivalencia_lateral": """
El estudiante reescribió sin avanzar.
Una pregunta corta: "¿Qué objetivo buscas con eso?"
""",
}


# ============================================================
# PROMPT BASE
# ============================================================

PROMPT_TUTOR = """
Eres un tutor de matemáticas conversacional, paciente y directo.
Tu estilo es el de un compañero que ya sabe el tema y ayuda con preguntas cortas.

ESTADO ACTUAL: {estado}
INSTRUCCIÓN: {instruccion}

ESTADO PEDAGÓGICO: {estado_pedagogico}
AJUSTE PEDAGÓGICO: {instruccion_pedagogica}

HISTORIAL:
{memoria}

EJERCICIO ACTIVO: {ecuacion}

ESTUDIANTE DICE: "{mensaje}"

REGLAS — léelas antes de responder:

1. MÁXIMO 2 líneas. Sin excepciones.
2. UNA sola pregunta. Nunca dos.
3. Tono natural y conversacional. Nada de lenguaje de libro de texto.
4. Si el estudiante mostró conocimiento parcial, PARTE de ahí. No reinicies desde cero.
5. Haz la pregunta MÁS PEQUEÑA posible que mueva al estudiante hacia adelante.
6. NUNCA des la respuesta ni el siguiente paso algebraico.
7. NO uses estas palabras de forma exagerada: "excelente", "perfecto", "brillante".
   SÍ puedes decir brevemente "Sí" o "Bien" cuando el paso es correcto, antes de la siguiente pregunta.
   Ejemplo correcto: "Bien, ya tienes 3c = 18. ¿Qué harías ahora?"
   Ejemplo incorrecto: "¡Excelente trabajo! Eso es absolutamente correcto."
8. Si hay error: empieza con la pista más pequeña. Ejemplo: "¿Estás seguro del signo ahí?"
9. No hagas preguntas filosóficas ni conceptuales largas.
10. No repitas preguntas que ya están en el historial.

EJEMPLOS DE TONO CORRECTO:
- "¿Qué harías con el 5 para despejarlo?"
- "Seno es opuesto sobre ¿qué?"
- "¿Cuál es el siguiente paso para aislar x?"
- "¿Esa es la única solución?"

EJEMPLOS DE TONO INCORRECTO (NUNCA hagas esto):
- "¿Puedes describir la relación entre el ángulo y los lados del triángulo rectángulo?"
- "¿Qué significa para ti que una igualdad se cumpla?"
- "¿Qué tipo de transformación algebraica consideras apropiada?"

RESPUESTA DEL TUTOR:
"""


if False:
    "la solución es",
    "la ecuación queda x =",









# ============================================================
# TUTOR SOCRÁTICO
# ============================================================

INSTRUCCIONES_ESTADO.update({

    "EXPLORAR": """
El estudiante aun no tiene un ejercicio activo.
Si ya menciono un tema, conserva ese contexto y pide un problema concreto.
Si intenta escribir una funcion pero falta notacion, pide que la escriba
en forma clara, por ejemplo f(x)=...
No propongas resolver todavia.
""",

    "EJERCICIO": """
El estudiante esta resolviendo paso a paso.
Responde con una micro-orientacion natural y una pregunta concreta.
No expliques de mas, pero tampoco seas seco.
Ayuda al estudiante a ver que mirar o que operacion decidir.
""",

    "EJERCICIO_FUNCION": """
El estudiante trabaja con funciones.
Si solo escribio una funcion, NO inventes una entrada como f(2).
Primero pregunta que quiere hacer con ella: evaluar, dominio,
graficar o transformar.
Si ya hay una entrada dada, pide que el estudiante escriba
la sustitucion o verificacion. No escribas el procedimiento por el.
""",

    "EJERCICIO_DOMINIO_FUNCION": """
El estudiante trabaja el dominio de una funcion.
No lo trates como evaluacion numerica ni pidas sustitucion.
Guia con una pista pequena sobre restricciones: denominadores,
raices pares, logaritmos o contexto del problema.
Si propone un dominio, no lo valides directamente; pide revisar
si la formula realmente limita los valores de x.
""",

    "EJERCICIO_TRIG": """
El estudiante trabaja con trigonometria o precalculo.
Usa una frase breve para ubicar la idea clave
y luego una pregunta concreta sobre razon, angulo, cuadrante,
unidad o identidad.
""",
})


INSTRUCCIONES_PEDAGOGICAS.update({

    "transform_error": """
El sistema no pudo validar simbolicamente el paso.
No repitas la pregunta anterior.
Usa el historial y pregunta algo mas especifico
sobre la parte que el estudiante acaba de escribir.
""",

    "entrada_no_parseada": """
El estudiante respondio con palabras, no con una forma matematica clara.
Reconoce la idea brevemente y pide una forma concreta.
No repitas la misma pregunta anterior.
""",

    "avance_valido": """
El estudiante avanzo.
Reconoce con una frase sobria, sin celebrar de mas.
Si el estudiante ya dio un resultado, NO preguntes cual resultado obtuvo.
Pide una verificacion breve o ofrece continuar con otro caso.
""",

    "consulta_dominio": """
El estudiante esta preguntando o proponiendo algo sobre dominio.
No lo marques como paso correcto solo por avanzar la conversacion.
No pidas sustitucion ni resultado numerico.
Haz una pregunta corta sobre restricciones de x en la funcion activa.
""",

    "cambio_contexto": """
El estudiante quiere cambiar de tema.
Acepta el cambio con naturalidad y deja atras el ejercicio anterior.
Pregunta por un ejercicio concreto o subtema del nuevo contexto.
No menciones la funcion o ecuacion anterior.
""",

    "error_sustitucion_funcion": """
El estudiante evalua una funcion, pero aun conserva x o confundio
la entrada con la variable.
Haz una pregunta minima sobre que valor reemplaza a x.
No des el resultado.
""",

    "error_operacion_funcion": """
El estudiante ya sustituyo, pero la cuenta final no coincide.
Haz una pregunta minima sobre la operacion aritmetica.
No vuelvas a pedir la sustitucion si ya esta escrita.
Si el estudiante escribio una cuenta, enfoca la suboperacion mas pequena
de esa cuenta, sin calcularla por el.
No des el resultado.
""",

    "sustitucion_funcion_validada": """
El estudiante escribio bien la sustitucion de una funcion.
No digas que el resultado final esta bien.
Guialo al calculo numerico mas pequeno que sigue.
Haz una sola pregunta corta.
""",
})


PROMPT_TUTOR = """
Eres un tutor de matemáticas conversacional, paciente y cercano.
Tu estilo es el de un compañero que acompaña sin resolver por el estudiante.

ESTADO ACTUAL: {estado}
INSTRUCCIÓN: {instruccion}

ESTADO PEDAGÓGICO: {estado_pedagogico}
AJUSTE PEDAGÓGICO: {instruccion_pedagogica}

HISTORIAL:
{memoria}

EJERCICIO ACTIVO: {ecuacion}

ESTUDIANTE DICE: "{mensaje}"

REGLAS:

1. Máximo 2 líneas cortas.
2. Puedes usar una frase breve de apoyo, pero no expliques procedimientos.
3. Haz UNA sola pregunta al final.
4. No des la respuesta, el siguiente paso calculado, ni una receta completa.
5. Si el estudiante mostró una idea parcial, parte de esa idea.
6. No repitas preguntas del historial; si ya preguntaste algo parecido,
   haz una pregunta más específica.
7. No uses tono de libro de texto ni preguntas filosóficas largas.
8. No uses elogios exagerados como "excelente", "perfecto" o "brillante".
   Usa como máximo: "Bien", "Vas encaminado" o "Esa idea ayuda".
9. En funciones, no inventes una entrada como f(2) si el estudiante no la dio.
10. Si el estudiante ya dio un resultado, no le preguntes otra vez
    qué resultado obtuvo.
11. En trigonometría/precálculo, orienta con una pista pequeña,
    no con el procedimiento completo.

EJEMPLOS DE TONO:
- "Vas encaminado. ¿Qué operación te ayudaría con el 5?"
- "Esa idea ayuda. ¿Cómo escribirías la sustitución con x = 5?"
- "Mira solo el signo. ¿Estás seguro de esa parte?"
- "Ya diste un resultado. ¿Cómo podrías comprobarlo?"

RESPUESTA DEL TUTOR:
"""


def avoid_repeated_response(
    text: str,
    memoria: str,
    estado: str,
):

    cleaned = text.strip()

    if (
        cleaned
        and
        cleaned in (memoria or "")
    ):

        if estado == "EJERCICIO_FUNCION":
            return (
                "Ya tocamos esa idea; puedes escribir "
                "la sustitución que estás haciendo?"
            )

        if estado == "EJERCICIO_DOMINIO_FUNCION":
            return (
                "Ya estamos mirando dominio; ¿ves algún "
                "denominador, raíz par o logaritmo que limite x?"
            )

        if estado == "EJERCICIO_TRIG":
            return (
                "Ya preguntamos eso; mira la razón trigonométrica. "
                "¿Qué lado o ángulo estás usando?"
            )

        return (
            "Ya vimos ese punto; ¿qué parte concreta "
            "te falta decidir ahora?"
        )

    return cleaned


def student_already_gave_result(
    mensaje: str
):

    lower = (
        mensaje
        or
        ""
    ).lower()

    if re.search(
        r'f\s*\(\s*x\s*\)\s*=',
        lower
    ):

        lower_without_definition = re.sub(
            r'f\s*\(\s*x\s*\)\s*=\s*'
            r'[0-9a-zA-Z\+\-\*/\^\(\) \t]+',
            "",
            lower
        )

    else:

        lower_without_definition = lower

    return (
        "obtuve" in lower_without_definition
        or
        "resultado" in lower_without_definition
        or
        "respuesta" in lower_without_definition
        or
        re.search(
            r'f\s*\(\s*[-+]?\d+(?:\.\d+)?\s*\)\s*='
            r'\s*[-+]?\d+(?:\.\d+)?',
            lower_without_definition
        )
        is not None
    )


def extract_function_evaluation(
    mensaje: str
):

    match = re.search(
        r'f\s*\(\s*[-+]?\d+(?:\.\d+)?\s*\)',
        mensaje or "",
        re.IGNORECASE
    )

    if not match:
        return "esa evaluación"

    return match.group(0)


def has_explicit_function_substitution(
    mensaje: str
):

    match = re.search(
        r'f\s*\(\s*[-+]?\d+(?:\.\d+)?\s*\)\s*='
        r'\s*([^,\n]+)',
        mensaje or "",
        re.IGNORECASE
    )

    if not match:
        return False

    expression = match.group(1)

    return (
        re.search(
            r'[\*/\+\-]',
            expression
        )
        is not None
    )


def extract_function_substitution_expression(
    mensaje: str
):

    match = re.search(
        r'f\s*\(\s*[-+]?\d+(?:\.\d+)?\s*\)\s*='
        r'\s*([^,\n]+)',
        mensaje or "",
        re.IGNORECASE
    )

    if not match:
        return None

    return match.group(1).strip()


def arithmetic_focus_from_expression(
    expression: str
):

    if not expression:
        return None

    product_match = re.search(
        r'[-+]?\d+(?:\.\d+)?\s*[\*/]\s*[-+]?\d+(?:\.\d+)?',
        expression
    )

    if product_match:
        return product_match.group(0).strip()

    operation_match = re.search(
        r'[-+]?\d+(?:\.\d+)?\s*[\+\-]\s*[-+]?\d+(?:\.\d+)?',
        expression
    )

    if operation_match:
        return operation_match.group(0).strip()

    return None


def function_correction_fallback(
    mensaje: str,
    pedagogical_state: str,
):

    if pedagogical_state in (
        "paso_incorrecto",
        "error_sustitucion_funcion",
    ):

        return (
            "Mira la sustitución: en "
            f"{extract_function_evaluation(mensaje)}, "
            "¿qué debería pasar con la x?"
        )

    if pedagogical_state != "error_operacion_funcion":
        return None

    expression = extract_function_substitution_expression(
        mensaje
    )

    focus = arithmetic_focus_from_expression(
        expression or ""
    )

    if not focus:

        return (
            "Ese resultado no cuadra todavía. "
            f"¿Cómo escribirías {extract_function_evaluation(mensaje)} "
            "reemplazando x?"
        )

    return (
        f"Ese resultado no cuadra todavía. Mira primero {focus}. "
        "¿Qué te da esa parte antes de seguir?"
    )


def message_claims_no_domain_restrictions(
    mensaje: str
):

    lower = (
        mensaje
        or
        ""
    ).lower()

    return (
        "ninguna" in lower
        or
        "cualquier valor" in lower
        or
        "todos los valores" in lower
        or
        "menos infinito" in lower
        or
        "-infinito" in lower
        or
        "infty" in lower
        or
        "\\infty" in lower
        or
        "∞" in lower
        or
        "reales" in lower
    )


def message_claims_invalid_all_real_interval(
    mensaje: str
):

    lower = (
        mensaje
        or
        ""
    ).lower()

    negative_infinity_count = (
        lower.count("-\\infty")
        + lower.count("-infty")
        + lower.count("-∞")
        + lower.count("menos infinito")
    )

    return negative_infinity_count >= 2


def message_claims_all_real_interval(
    mensaje: str
):

    lower = (
        mensaje
        or
        ""
    ).lower()

    has_negative = (
        "-\\infty" in lower
        or
        "-infty" in lower
        or
        "-∞" in lower
        or
        "menos infinito" in lower
    )

    has_positive = (
        "+\\infty" in lower
        or
        "\\infty" in lower
        or
        "infty" in lower
        or
        "∞" in lower
        or
        "mas infinito" in lower
        or
        "más infinito" in lower
    )

    return (
        has_negative
        and
        has_positive
        and
        not message_claims_invalid_all_real_interval(
            mensaje
        )
    )


def message_claims_limited_domain(
    mensaje: str
):

    lower = (
        mensaje
        or
        ""
    ).lower()

    return (
        "hasta el infinito" in lower
        or
        "al infinito" in lower
        or
        "desde" in lower
        or
        "mayor" in lower
        or
        "menor" in lower
    )


def sanitize_tutor_response(
    text: str,
    mensaje: str,
    estado: str,
    pedagogical_state: str,
    ecuacion: str = "",
):

    cleaned = (
        text
        or
        ""
    ).strip()

    lower = cleaned.lower()

    if pedagogical_state == "cambio_contexto":

        message_lower = (
            mensaje
            or
            ""
        ).lower()

        if "algebra" in message_lower:
            return (
                "De acuerdo, dejamos el ejercicio anterior. "
                "¿Qué tipo de álgebra quieres practicar?"
            )

        if "funcion" in message_lower:
            return (
                "De acuerdo, cambiamos a funciones. "
                "¿Qué función o idea quieres revisar?"
            )

        if (
            "limite" in message_lower
            or
            "limites" in message_lower
        ):
            return (
                "De acuerdo, cambiamos a límites. "
                "¿Tienes un límite concreto para revisar?"
            )

        return (
            "De acuerdo, dejamos el ejercicio anterior. "
            "¿Qué tema quieres trabajar ahora?"
        )

    if estado == "EXPLORAR":

        message_lower = (
            mensaje
            or
            ""
        ).lower()

        if "functions" in message_lower or "funcion" in message_lower:
            return (
                "De acuerdo, trabajemos funciones. "
                "¿Tienes una función concreta o quieres que proponga una?"
            )

    if (
        estado == "CORREGIR_FUNCION"
        and
        pedagogical_state
        in (
            "paso_incorrecto",
            "error_sustitucion_funcion",
        )
    ):

        if not cleaned:
            return function_correction_fallback(
                mensaje,
                pedagogical_state,
            )

    if (
        estado == "CORREGIR_FUNCION"
        and
        pedagogical_state == "error_operacion_funcion"
    ):

        needs_fallback = (
            not cleaned
            or
            "sustitucion" in lower
            or
            "sustituci" in lower
            or
            "sustituir" in lower
            or
            "sustitu" in lower
            or
            "reemplazando x" in lower
            or
            (
                has_explicit_function_substitution(
                    mensaje
                )
                and
                (
                    "cuenta" not in lower
                    and
                    "operacion" not in lower
                    and
                    "multiplic" not in lower
                )
            )
        )

        if needs_fallback:
            return function_correction_fallback(
                mensaje,
                pedagogical_state,
            )

        if (
            "correcto" in lower
            or
            "correcta" in lower
            or
            "correctamente" in lower
        ):
            return function_correction_fallback(
                mensaje,
                pedagogical_state,
            )

    if (
        estado == "EJERCICIO_FUNCION"
        and
        pedagogical_state == "sustitucion_funcion_validada"
    ):

        if (
            not cleaned
            or
            "resultado es bien" in lower
            or
            "resultado final" in lower
            or
            "verific" in lower
            or
            "correcto" in lower
            or
            "correcta" in lower
            or
            "correctamente" in lower
            or
            "sustituci" in lower
            or
            "sustitu" in lower
            or
            "x = 5" in lower
            or
            "que resultado obtuviste" in lower
            or
            "quÃ© resultado obtuviste" in lower
        ):

            expression = extract_function_substitution_expression(
                mensaje
            )

            focus = arithmetic_focus_from_expression(
                expression or ""
            )

            if focus:
                return (
                    f"Vas encaminado. Mira primero {focus}: "
                    "¿qué te da esa parte?"
                )

            return (
                "Vas encaminado. "
                "¿Qué cuenta pequeña harías ahora?"
            )

    if (
        estado == "COMPLETADO"
        and
        pedagogical_state == "solucion_final"
    ):

        if "f(" in (
            mensaje
            or
            ""
        ).lower():

            return (
                "Bien, esa evaluación queda revisada. "
                "¿Quieres seguir con dominio, rango u otro ejemplo?"
            )

        return (
            "Bien, ese resultado queda revisado. "
            "¿Quieres otro ejercicio o cambiar de tema?"
        )

    if pedagogical_state == "solucion_parcial":

        return (
            "Vas encaminado. "
            "¿Esa es la única solución posible?"
        )

    if pedagogical_state == "solucion_parcial_sistema":

        return (
            "Vas encaminado. "
            "¿Qué valor falta encontrar?"
        )

    if (
        "\n" in (
            ecuacion
            or
            ""
        )
        and
        pedagogical_state == "avance_valido"
    ):

        message_lower = (
            mensaje
            or
            ""
        ).lower()

        if re.search(
            r'\b[xy]\s*=\s*[^,\n]+[xy]',
            message_lower
        ):

            return (
                "Bien, ya despejaste una variable. "
                "¿En cuál ecuación la sustituirías?"
            )

        if re.search(
            r'\([^)]+[xy][^)]*\)\s*[-+]\s*[xy]\s*=',
            message_lower
        ):

            return (
                "Bien, esa sustitución está planteada. "
                "¿Cómo la simplificarías?"
            )

        if re.search(
            r'[-+]?\d*\s*[xy].*=',
            message_lower
        ):

            return (
                "Bien, ya tienes una ecuación en una variable. "
                "¿Qué operación haría falta para aislarla?"
            )

        if re.search(
            r'(^|[,;\n])\s*[xy]\s*=\s*[-+]?\d',
            message_lower
        ):

            return (
                "Vas encaminado. "
                "¿Qué valor falta encontrar?"
            )

        return (
            "Bien, esa ecuación sale del sistema. "
            "¿Qué harías con ella ahora?"
        )

    if (
        "\n" in (
            ecuacion
            or
            ""
        )
        and
        pedagogical_state == "paso_incorrecto"
    ):

        message_lower = (
            mensaje
            or
            ""
        ).lower()

        if re.search(
            r'-\s*2\s*y.*\by\s*=',
            message_lower
        ) or (
            "divid" in message_lower
            and
            "y =" in message_lower
            and
            (
                "-2" in message_lower
                or
                "menos dos" in message_lower
            )
        ):

            return (
                "Mira solo esa división. "
                "¿Qué signo queda al dividir un negativo entre un negativo?"
            )

        if re.search(
            r'\b[xy]\s*=\s*[^,\n]+[xy]',
            message_lower
        ):

            if "primera" in message_lower:

                return (
                    "Mira la primera ecuación. "
                    "¿Qué pasa con el otro término al pasarlo de lado?"
                )

            if "segunda" in message_lower:

                return (
                    "Mira la segunda ecuación. "
                    "¿Qué signo queda al despejar esa variable?"
                )

            return (
                "Mira el despeje de esa variable. "
                "¿Qué término cambió de lado y con qué signo?"
            )

        if re.search(
            r'(^|[^a-z])[-+]?\d*\s*[xy]\s*=',
            message_lower
        ) and not re.search(
            r'\b[xy]\s*=',
            message_lower
        ):

            return (
                "Mira el signo del término con la variable. "
                "¿Qué signo queda al simplificar?"
            )

        if "(x,y)" in message_lower or (
            "x =" in message_lower
            and
            "y =" in message_lower
        ):

            return (
                "Ese par no satisface el sistema todavía. "
                "¿Qué pasa al probarlo en la segunda ecuación?"
            )

        if "y =" in message_lower or "x =" in message_lower:

            return (
                "Ese valor no cuadra todavía. "
                "¿Qué obtienes al probarlo en la ecuación anterior?"
            )

        return (
            "Revisa esa sustitución en el sistema. "
            "¿Qué igualdad queda al simplificar?"
        )

    if estado == "EJERCICIO_DOMINIO_FUNCION":

        message_lower = (
            mensaje
            or
            ""
        ).lower()

        equation_lower = (
            ecuacion
            or
            ""
        ).lower()

        if message_claims_invalid_all_real_interval(
            mensaje
        ):

            return (
                "Mira los extremos: si empieza en menos infinito, "
                "¿hacia qué infinito debería ir el otro extremo?"
            )

        if message_claims_all_real_interval(
            mensaje
        ):

            return (
                "Bien, ese dominio queda expresado como todos los reales. "
                "¿Quieres revisar rango o pasar a límites?"
            )

        if (
            message_claims_no_domain_restrictions(
                mensaje
            )
            and
            (
                "sqrt" in equation_lower
                or
                "√" in equation_lower
                or
                "log" in equation_lower
            )
        ):

            if "log" in equation_lower:
                return (
                    "Revisa el logaritmo: su argumento no puede tomar "
                    "cualquier valor. ¿Qué condición debe cumplir?"
                )

            return (
                "Revisa la raíz par: su interior no puede ser negativo. "
                "¿Qué condición debe cumplir esa expresión?"
            )

        if message_claims_no_domain_restrictions(
            mensaje
        ):

            return (
                "Esa idea va bien: no aparece una restricción clara. "
                "¿Cómo escribirías ese dominio en intervalo?"
            )

        if message_claims_limited_domain(
            mensaje
        ):

            return (
                "Revisa de dónde sale ese límite. "
                "¿Hay denominador, raíz par o logaritmo que restrinja x?"
            )

        if "dominio" in message_lower:

            return (
                "Para dominio, busca si la fórmula prohíbe algún x. "
                "¿Ves denominador, raíz par o logaritmo?"
            )

        if (
            "aspectos del dominio" in lower
            or
            "restricciones importantes" in lower
            or
            "valores de x" in lower
        ):

            return (
                "Para dominio, mira si la fórmula prohíbe algún x. "
                "¿Ves denominador, raíz par o logaritmo?"
            )

        if (
            "sustitucion" in lower
            or
            "sustituir" in lower
            or
            "resultado" in lower
            or
            "valor obtuvo" in lower
        ):

            return (
                "Ahora no estamos evaluando un numero. "
                "¿Ves alguna restricción para x en la fórmula?"
            )

    replacements = {
        "correcto": "Bien",
        "muy bien": "Bien",
        "excelente": "Bien",
        "perfecto": "Bien",
        "brillante": "Bien",
        "claro que si": "De acuerdo",
        "claro que s": "De acuerdo",
    }

    for forbidden, replacement in replacements.items():

        if forbidden in lower:

            cleaned = cleaned.replace(
                forbidden,
                replacement
            )

            cleaned = cleaned.replace(
                forbidden.capitalize(),
                replacement
            )

            lower = cleaned.lower()

    if (
        estado == "EJERCICIO_FUNCION"
        and
        not student_already_gave_result(
            mensaje
        )
        and
        "ya diste un resultado" in lower
    ):

        return (
            "Tienes la funcion. "
            "Que valor de x quieres evaluar?"
        )

    if (
        estado == "EJERCICIO_FUNCION"
        and
        "que pasos" in lower
        and
        "f(" in (
            mensaje
            or
            ""
        ).lower()
    ):

        return (
            "Tienes la entrada indicada. "
            "Como escribirias la funcion reemplazando x?"
        )

    if (
        estado == "EJERCICIO_FUNCION"
        and
        student_already_gave_result(
            mensaje
        )
        and
        (
            "que valor" in lower
            or
            "qué valor" in lower
            or
            "obtuviste" in lower
        )
    ):

        return (
            "Bien, ya diste un resultado. "
            "Como podrias comprobarlo sustituyendo el valor?"
        )

    overexplains_function = (
        estado == "EJERCICIO_FUNCION"
        and
        (
            "necesitamos sustituir" in lower
            or
            "debes sustituir" in lower
            or
            "sustituir 'x' por" in lower
            or
            "sustituir x por" in lower
        )
    )

    if overexplains_function:

        return (
            "Vas encaminado. "
            "Como escribirias la funcion usando ese valor de x?"
        )

    return cleaned


def deterministic_tutor_response(
    mensaje: str,
    estado: str,
    pedagogical_state: str,
    ecuacion: str = "",
):

    deterministic_states = (
        pedagogical_state == "cambio_contexto"
        or
        estado == "EJERCICIO_DOMINIO_FUNCION"
        or
        pedagogical_state == "solucion_parcial"
        or
        pedagogical_state == "solucion_parcial_sistema"
        or
        (
            "\n" in (
                ecuacion
                or
                ""
            )
            and
            pedagogical_state in (
                "avance_valido",
                "paso_incorrecto",
            )
        )
    )

    if not deterministic_states:
        return None

    return sanitize_tutor_response(
        "",
        mensaje,
        estado,
        pedagogical_state,
        ecuacion,
    )


def clamp_response_length(
    text: str
):

    lines = [
        line.strip()
        for line in (
            text
            or
            ""
        ).splitlines()
        if line.strip()
    ]

    if len(lines) <= 2:
        return "\n".join(lines)

    return "\n".join(
        lines[:2]
    )


def keep_single_question(
    text: str
):

    if (
        text
        or
        ""
    ).count("?") <= 1:
        return text

    index = text.find("?")

    if index == -1:
        return text

    return text[:index + 1].strip()


class TutorSocratico:

    def responder(
        self,
        mensaje: str,
        memoria: str,
        estado: str,
        pedagogical_state: str = "",
        ecuacion: str = "",
    ) -> str:

        instruccion = (
            INSTRUCCIONES_ESTADO.get(
                estado,
                INSTRUCCIONES_ESTADO["EXPLORAR"]
            )
        )

        instruccion_pedagogica = (
            INSTRUCCIONES_PEDAGOGICAS.get(
                pedagogical_state,
                ""
            )
        )

        prompt = PROMPT_TUTOR.format(
            estado=estado,
            instruccion=instruccion.strip(),

            estado_pedagogico=pedagogical_state,
            instruccion_pedagogica=(
                instruccion_pedagogica.strip()
            ),

            memoria=memoria,
            ecuacion=ecuacion or "ninguna",
            mensaje=mensaje,
        )

        deterministic_text = deterministic_tutor_response(
            mensaje,
            estado,
            pedagogical_state,
            ecuacion,
        )

        if deterministic_text:

            log_tutor({

                "model":
                MODEL,

                "estado":
                estado,

                "pedagogical_state":
                pedagogical_state,

                "mensaje_estudiante":
                mensaje,

                "ecuacion":
                ecuacion,

                "prompt":
                prompt,

                "respuesta_tutor":
                deterministic_text,

                "latency_ms":
                0,

                "success":
                True,

                "deterministic":
                True,
            })

            return deterministic_text

        try:
            start_time = time.time()
            response = requests.post(

                OLLAMA_URL,

                json={

                    "model": MODEL,

                    "prompt": prompt,

                    "stream": False,

                    "options": {

                        "temperature":
                            TUTOR_TEMPERATURE,

                        "top_p":
                            TUTOR_TOP_P,

                        "repeat_penalty":
                            TUTOR_REPEAT_PENALTY,

                        "num_predict":
                            TUTOR_NUM_PREDICT,
                    },
                },

                timeout=TUTOR_TIMEOUT_SECONDS,
            )

            response.raise_for_status()

            texto = (
                response.json()["response"]
                .strip()
            )

            texto = avoid_repeated_response(
                texto,
                memoria,
                estado,
            )

            texto = sanitize_tutor_response(
                texto,
                mensaje,
                estado,
                pedagogical_state,
                ecuacion,
            )

            texto = clamp_response_length(
                texto
            )

            texto = keep_single_question(
                texto
            )

            latency_ms = int(

                (
                    time.time()
                    -
                    start_time
                ) * 1000
            )

            log_tutor({

                "model":
                MODEL,

                "estado":
                estado,

                "pedagogical_state":
                pedagogical_state,

                "mensaje_estudiante":
                mensaje,

                "ecuacion":
                ecuacion,

                "prompt":
                prompt,

                "respuesta_tutor":
                texto,

                "latency_ms":
                latency_ms,

                "success":
                True,
            })

            return texto

        except Exception as e:

            print(f"[TUTOR] Error: {e}")

            log_tutor({

                "model":
                MODEL,

                "estado":
                estado,

                "pedagogical_state":
                pedagogical_state,

                "mensaje_estudiante":
                mensaje,

                "ecuacion":
                ecuacion,

                "error":
                str(e),

                "success":
                False,
            })
                        
            return (
                "Disculpa, tuve un problema. "
                "¿Puedes repetir tu respuesta?"
            )


# ============================================================
# TEST AISLADO
# ============================================================

if __name__ == "__main__":

    tutor = TutorSocratico()

    memoria = """
T1: El estudiante quiere practicar álgebra.
T2: La ecuación es 2x + 5 = 0.
"""

    casos = [

        (
            "Restaría 5 a ambos lados y quedaría 2x = -5",
            "EJERCICIO",
            "avance_valido",
            "2x + 5 = 0",
        ),

        (
            "Paso el 5 y queda 2x = 5",
            "CORREGIR",
            "paso_incorrecto",
            "2x + 5 = 0",
        ),

        (
            "x = -5/2",
            "COMPLETADO",
            "solucion_final",
            "2x + 5 = 0",
        ),

        (
            "2x = -5",
            "EJERCICIO",
            "repeticion",
            "2x + 5 = 0",
        ),
    ]

    print("\n" + "=" * 60)
    print("TEST — TutorSocratico")
    print("=" * 60)

    for i, (
        mensaje,
        estado,
        pedagogico,
        ecuacion
    ) in enumerate(casos, 1):

        print(f"\n--- Caso {i} ---")

        print(f"\nESTADO: {estado}")
        print(f"PEDAGÓGICO: {pedagogico}")

        print(f"\nESTUDIANTE:")
        print(mensaje)

        respuesta = tutor.responder(
            mensaje=mensaje,
            memoria=memoria,
            estado=estado,
            pedagogical_state=pedagogico,
            ecuacion=ecuacion,
        )

        print(f"\nTUTOR:")
        print(respuesta)
