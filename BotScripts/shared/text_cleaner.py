import re
import unicodedata

def sanitize_name_for_llm(name: str) -> str:
    if not name:
        return "someone"

    # Normalize unicode
    name = unicodedata.normalize("NFKC", name)

    # Remove emoji / symbols / weird decorative chars, keep letters/numbers/basic punctuation/spaces
    name = re.sub(r"[^\w\s'\-]", "", name, flags=re.UNICODE)

    # Collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()

    return name or "someone"