from core.classification.structure_detector import (
    classify_equation_type,
    classify_structure,
    count_equations,
    count_variables,
    detect_equation_type,
    extract_variables,
    get_equations,
    has_shared_variables,
    is_linear,
    is_system,
    unique_equations,
)


STRUCTURE_TO_TOPIC = {
    "single_linear_equation": "single_linear_equation",
    "single_nonlinear_equation": "single_nonlinear_equation",
    "linear_system": "linear_system",
    "nonlinear_system": "nonlinear_system",
    "factoring_expression": "polynomials",
    "function_expression": "functions",
    "inequality_expression": "inequalities",
    "trigonometric_expression": "trigonometry_basics",
}


class TopicDetector:

    def detect(
        self,
        parsed_result
    ):

        structure = classify_structure(
            parsed_result
        )

        if not structure:
            return None

        return STRUCTURE_TO_TOPIC.get(
            structure
        )

