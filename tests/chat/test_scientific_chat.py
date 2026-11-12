def build_artemis_prompt(user_question: str, context_summary: str) -> dict:
    if not user_question.strip():
        raise ValueError("La question ne peut pas être vide")
    return {
        "role": "user",
        "question": user_question.strip(),
        "context": context_summary.strip()
    }

def test_scientific_chat_payload():
    payload = build_artemis_prompt(
        "Quelle est la tendance thermique sur Libreville ?",
        "Moyenne observée : +1.2°C sur 10 ans."
    )
    assert payload["role"] == "user"
    assert "Libreville" in payload["question"]
    assert "1.2°C" in payload["context"]