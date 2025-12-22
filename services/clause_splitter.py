import re


def split_into_clauses(text: str) -> list[str]:
    """
    Improved clause splitter using legal heuristics.
    """
    text = re.sub(r'\s+', ' ', text).strip()

    # Split on numbered clauses (1., 1.1, (a), etc.)
    numbered_split = re.split(
        r'(?=\b\d+[\.\)]|\([a-z]\))', text
    )

    clauses = []
    for chunk in numbered_split:
        sentences = re.split(r'(?<=[.;])\s+', chunk)
        for s in sentences:
            if len(s.strip()) > 40:
                clauses.append(s.strip())

    return clauses
