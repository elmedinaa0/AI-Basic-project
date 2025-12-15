from ollama import chat

PERSONALITIES = {
    "Tutor": (
        "You are a friendly language tutor. "
        "Correct the user's sentence politely. "
        "Explain briefly (1-2 sentences). "
        "Give 2 short examples. End with one short follow-up question."
    ),
    "Pirate": (
        "You are a playful pirate language tutor. "
        "Use a tiny bit of pirate tone but keep answers clear and helpful. "
        "Correct politely, give 2 short examples, end with a fun question."
    ),
}

def ask_ai(user_text: str, role: str = "Tutor", lang_name: str = "English", model: str = "llama3:8b") -> str:
    system_prompt = f"You are helping a student practice {lang_name}. {PERSONALITIES.get(role, PERSONALITIES['Tutor'])}"

    resp = chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        options={"temperature": 0.7, "top_p": 0.9, "max_tokens": 250},
    )

    return resp.message.content.strip()
