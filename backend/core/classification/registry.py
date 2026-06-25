from core.curriculum.algebra.linear_equations import (
    TOPIC as LINEAR_EQUATIONS
)

from core.curriculum.algebra.systems_of_equations import (
    TOPIC as SYSTEMS
)

from core.curriculum.algebra.polynomials import (
    TOPIC as POLYNOMIALS
)

from core.curriculum.algebra.quadratic_equations import (
    TOPIC as QUADRATICS
)

from core.curriculum.precalculus.functions import (
    TOPIC as FUNCTIONS
)

from core.curriculum.precalculus.trigonometry_basics import (
    TOPIC as TRIGONOMETRY
)


TOPIC_REGISTRY = {

    LINEAR_EQUATIONS["id"]:
        LINEAR_EQUATIONS,

    SYSTEMS["id"]:
        SYSTEMS,

    POLYNOMIALS["id"]:
        POLYNOMIALS,

    QUADRATICS["id"]:
        QUADRATICS,

    FUNCTIONS["id"]:
        FUNCTIONS,

    TRIGONOMETRY["id"]:
        TRIGONOMETRY,
}


def topic_alias(
    topic,
    topic_id,
    name=None,
    concepts=None
):

    aliased = topic.copy()

    aliased["id"] = topic_id

    if name:

        aliased["name"] = name

    if concepts:

        aliased["concepts"] = concepts

    return aliased


TOPIC_REGISTRY.update(
    {
        "single_linear_equation":
            topic_alias(
                LINEAR_EQUATIONS,
                "single_linear_equation",
                "Ecuacion Lineal",
                [
                    "equations",
                    "single_equation",
                    "linear_structure"
                ]
            ),

        "single_nonlinear_equation":
            topic_alias(
                QUADRATICS,
                "single_nonlinear_equation",
                "Ecuacion No Lineal",
                [
                    "equations",
                    "single_equation",
                    "nonlinear_structure"
                ]
            ),

        "linear_system":
            topic_alias(
                SYSTEMS,
                "linear_system",
                "Sistema Lineal",
                [
                    "systems",
                    "linear_system",
                    "simultaneous_constraints"
                ]
            ),

        "nonlinear_system":
            topic_alias(
                SYSTEMS,
                "nonlinear_system",
                "Sistema No Lineal",
                [
                    "systems",
                    "nonlinear_system",
                    "simultaneous_constraints"
                ]
            ),
    }
)
