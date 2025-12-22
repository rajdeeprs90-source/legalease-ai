import re

RISK_RULES = {
    "Termination": {
        "patterns": [
            r"terminate at any time",
            r"sole discretion",
            r"without cause",
            r"immediate termination"
        ],
        "risk": "High"
    },
    "Liability": {
        "patterns": [
            r"limitation of liability",
            r"not liable",
            r"no liability",
            r"exclude liability"
        ],
        "risk": "Medium"
    },
    "Indemnity": {
        "patterns": [
            r"indemnify",
            r"hold harmless"
        ],
        "risk": "High"
    },
    "Auto-Renewal": {
        "patterns": [
            r"automatically renew",
            r"auto[- ]renewal",
            r"renewal term"
        ],
        "risk": "Medium"
    },
    "Data Sharing": {
        "patterns": [
            r"share personal data",
            r"third[- ]party partners",
            r"data may be shared"
        ],
        "risk": "Medium"
    }
}

def analyze_clause_with_rules(clause: str) -> dict:
    """
    Analyze a single clause using predefined risk rules.
    """
    clause_lower = clause.lower()
    matches = []

    for category, rule in RISK_RULES.items():
        for pattern in rule["patterns"]:
            if re.search(pattern, clause_lower):
                matches.append({
                    "category": category,
                    "risk": rule["risk"],
                    "pattern": pattern
                })

    if not matches:
        return {
            "risk_level": "Low",
            "categories": [],
            "matched_patterns": []
        }

    highest_risk = "Medium"
    if any(m["risk"] == "High" for m in matches):
        highest_risk = "High"

    return {
        "risk_level": highest_risk,
        "categories": list({m["category"] for m in matches}),
        "matched_patterns": matches
    }
