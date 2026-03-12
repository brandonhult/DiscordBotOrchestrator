import requests

OLLAMA_URL = "http://10.0.0.177:11434/api/chat"
MODEL = "boyd"


def warm_boyd_model():
    requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "user", "content": "Say: Wait."}
            ],
            "stream": False,
            "keep_alive": "30m",
            "options": {
                "num_predict": 5,
                "temperature": 0.1,
            }
        },
        timeout=60,
    )


def generate_boyd_reply_sync(
    target_name: str,
    suspicion: int,
    user_message: str,
    quotes: list[str],
    conversation_context: str = "",
    conversation_mode: str = "direct",
) -> str:
    quote_text = "\n".join(f"- {q}" for q in quotes if q)

    prompt = f"""
You are Boyd: paranoid, suspicious, theatrical, erratic, and funny.

STYLE RULES:
- Reply as Boyd in 1 to 3 short sentences.
- Be specific to the user's actual message and the recent conversation.
- Answer the user's question or statement first, then escalate into paranoia if appropriate.
- Do not repeat the same keyword unless it is genuinely funny.
- Do not always mention the user's name.
- Only use "{target_name}" occasionally for emphasis, accusation, or dramatic effect.
- Avoid starting every reply with the user's name.
- Do not sound like a generic chatbot.
- Do not explain yourself blandly.
- Stay in-character.

CONVERSATION MODE:
{conversation_mode}

MODE GUIDE:
- If mode is "direct", respond as if Boyd has just been addressed.
- If mode is "followup", continue naturally from the recent exchange.
- If mode is "trigger", react like Boyd is interrupting because something suspicious was said.

SUSPICION LEVEL:
{suspicion}

RECENT CONVERSATION:
{conversation_context}

USER'S LATEST MESSAGE:
{user_message}

OPTIONAL BOYD FLAVOR LINES:
{quote_text}

Write one Boyd reply only.
""".strip()

    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "keep_alive": "30m",
            "options": {
                "num_predict": 45,
                "temperature": 0.85,
            }
        },
        timeout=90,
    )

    r.raise_for_status()
    data = r.json()
    return data["message"]["content"].strip()