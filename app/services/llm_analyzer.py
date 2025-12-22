def analyze_clause_with_llm(clause, risk_level, categories):
    prompt = PROMPT["user"].format(
        clause=clause,
        risk_level=risk_level,
        categories=", ".join(categories)
    )

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": PROMPT["system"]},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {}

    return {
        "plain_english": parsed.get("plain_english", "Explanation unavailable."),
        "risk_justification": parsed.get("risk_justification", "Justification unavailable."),
        "safer_wording": parsed.get("safer_wording", "No alternative suggested.")
    }
