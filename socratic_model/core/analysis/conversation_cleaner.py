import re


CONVERSATIONAL_PREFIXES = [
    "tengo",
    "creo que",
    "pienso que",
    "la ecuacion es",
    "la ecuacion",
    "seria",
    "obtengo",
    "me da",
    "el resultado es",
    "queda",
    "nos queda",
]

MATH_FUNCTIONS = {"sin", "cos", "tan", "log", "exp"}


_TERM = (
    r'(?:'
    r'\([0-9a-zA-Z\+\-\*/\^\s]+\)'
    r'|-?\d+(?:\.\d+)?'
    r'|-?\d*[a-zA-Z]{1,2}(?:\^[0-9]+)?'
    r')'
)

_SIDE = (
    rf'{_TERM}'
    rf'(?:\s*[\+\-\*/]\s*{_TERM})*'
)

_COMPACT_EQ = re.compile(
    rf'({_SIDE}\s*(?:<=|>=|<|>|=)\s*{_SIDE})'
)


def extract_equation_from_text(text: str) -> str | None:
    """
    Extracts the cleanest compact equation from conversational text.
    """
    candidates = []

    for match in _COMPACT_EQ.finditer(text):

        candidate = match.group(1).strip()

        candidate = re.sub(
            r'^[A-Za-z]{2}\s+(?=[-+]?\d)',
            '',
            candidate
        ).strip()

        candidates.append(
            candidate
        )

    if not candidates:
        return None

    def score(candidate):
        identifiers = re.findall(
            r'\b[A-Za-z]{2,}\b',
            candidate
        )

        word_penalty = len([
            identifier
            for identifier in identifiers
            if identifier not in MATH_FUNCTIONS
        ])

        return (
            -word_penalty,
            candidate.rfind("="),
            len(candidate),
        )

    return max(candidates, key=score)


def clean_conversational_text(text: str) -> str:
    cleaned = text.strip()
    lowered = cleaned.lower()

    for prefix in CONVERSATIONAL_PREFIXES:
        if lowered.startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            lowered = cleaned.lower()
            break

    if "\n" in cleaned:
        return cleaned

    if cleaned.count("=") > 1 or "sistema" in lowered:
        return cleaned

    word_count = len(cleaned.split())

    if word_count >= 4:
        candidate = extract_equation_from_text(cleaned)

        if candidate and len(candidate) < len(cleaned) * 0.9:
            return candidate

    return cleaned
