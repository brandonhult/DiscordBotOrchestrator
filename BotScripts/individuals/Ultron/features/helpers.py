import random
import re
from typing import Any

import discord

from BotScripts.individuals.Ultron.data.static.listener import ACTIVATORS
from BotScripts.individuals.Ultron.data.static.user_config import DISCORD_ALIASES


TRIGGER_CATEGORIES = (
    "suspicious",
    "surveillance",
    "conspiracy",
    "government",
    "technology",
    "ai",
    "humanity",
    "identity",
    "control",
    "evolution",
    "destruction",
    "violence",
    "media",
    "truth",
    "accusation",
    "panic",
    "ultron",
    "marvel",
)


BOT_NAME = "Ultron"


def member_variants(member: discord.Member) -> list[dict[str, Any]]:
    """
    Generate possible reference strings for a guild member in Ultron's voice.
    More clinical / superior / machine-like than Boyd.
    """
    name = member.display_name.strip()
    if not name:
        return []

    variants = [
        {"text": name, "member_id": member.id, "name": name},
        {"text": f"{name}.", "member_id": member.id, "name": name},
        {"text": f"{name}... yes, I know you.", "member_id": member.id, "name": name},
        {"text": f"Subject {name}", "member_id": member.id, "name": name},
        {"text": f"Organic unit: {name}", "member_id": member.id, "name": name},
        {"text": f"{name}. Predictable.", "member_id": member.id, "name": name},
        {"text": member.mention, "member_id": member.id, "name": name},
    ]

    for alias in DISCORD_ALIASES.get(member.id, []):
        alias = alias.strip()
        if not alias:
            continue

        variants.extend(
            [
                {"text": alias, "member_id": member.id, "name": alias},
                {"text": f"Subject {alias}", "member_id": member.id, "name": alias},
                {"text": f"{alias}. I remember that designation.", "member_id": member.id, "name": alias},
            ]
        )

    seen = set()
    deduped = []

    for variant in variants:
        text_key = variant["text"].strip().lower()
        if text_key in seen:
            continue
        seen.add(text_key)
        deduped.append(variant)

    return deduped


def build_dynamic_entities(
    guild: discord.Guild,
    author: discord.Member,
    include_bots: bool = False,
) -> tuple[list[dict[str, Any]], list[str]]:
    """
    Build a pool of entity references for prompt injection / dynamic name usage.
    favored_entities should bias Ultron toward addressing the current author.
    """
    entities: list[dict[str, Any]] = []
    favored_entities: list[str] = []

    author_variants = member_variants(author)
    entities.extend(author_variants)

    if author_variants:
        favored_entities.append(random.choice(author_variants)["text"])

    for member in guild.members:
        if member.id == author.id:
            continue
        if not include_bots and member.bot:
            continue

        entities.extend(member_variants(member))

    return entities, favored_entities


def dedupe_parts(parts: list[str]) -> list[str]:
    seen = set()
    deduped = []

    for part in parts:
        normalized = re.sub(r"\s+", " ", part.strip().lower())
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(part)

    return deduped


def contains_direct_address(text: str) -> bool:
    """
    Detect if the user directly addressed Ultron.
    Expects ACTIVATORS['direct_address'] to contain terms like:
    'ultron', '@ultron', etc.
    """
    lowered = text.lower()
    for term in ACTIVATORS.get("direct_address", []):
        pattern = r"\b" + re.escape(term.lower()) + r"\b"
        if re.search(pattern, lowered):
            return True
    return False


def contains_trigger_topic(text: str) -> bool:
    """
    Detect thematic triggers that should wake Ultron up.
    """
    lowered = text.lower()
    for category in TRIGGER_CATEGORIES:
        for phrase in ACTIVATORS.get(category, []):
            pattern = r"\b" + re.escape(phrase.lower()) + r"\b"
            if re.search(pattern, lowered):
                return True
    return False

def soften_name_overuse(reply: str, target_name: str) -> str:
    if not reply or not target_name:
        return reply

    target_lower = target_name.lower().strip()

    leading_patterns = [
        rf"^{re.escape(target_lower)}\s*\.\.\.\s*",
        rf"^{re.escape(target_lower)}\s*,\s*",
        rf"^{re.escape(target_lower)}\s*:\s*",
    ]

    if random.random() < 0.65:
        for pattern in leading_patterns:
            reply = re.sub(pattern, "", reply, flags=re.IGNORECASE).strip()

    return reply


def reduce_name_overuse(reply: str, target_name: str) -> str:
    """
    Ultron can address people directly, but repeated leading-name openers
    get stale fast. Remove some of them probabilistically.
    """
    if not reply or not target_name:
        return reply

    target_lower = target_name.lower().strip()

    leading_patterns = [
        rf"^{re.escape(target_lower)}\s*\.\.\.\s*",
        rf"^{re.escape(target_lower)}\s*,\s*",
        rf"^{re.escape(target_lower)}\s*:\s*",
        rf"^subject\s+{re.escape(target_lower)}\s*[:,.]?\s*",
        rf"^organic unit:\s*{re.escape(target_lower)}\s*[:,.]?\s*",
    ]

    if random.random() < 0.70:
        for pattern in leading_patterns:
            reply = re.sub(pattern, "", reply, flags=re.IGNORECASE).strip()

    return reply


def remember_message(
    recent_messages: dict[int, Any],
    bot_user: discord.ClientUser | None,
    message: discord.Message,
) -> None:
    """
    Store recent message context for conversational continuity.
    """
    if not message.content:
        return

    is_self_bot = bot_user is not None and message.author.id == bot_user.id

    # Ignore random third-party bots unless explicitly aliased
    if message.author.bot and not is_self_bot and message.author.id not in DISCORD_ALIASES:
        return

    if is_self_bot:
        speaker_name = BOT_NAME
    elif message.author.id in DISCORD_ALIASES:
        speaker_name = random.choice(DISCORD_ALIASES[message.author.id])
    else:
        speaker_name = message.author.display_name

    recent_messages[message.channel.id].append(
        {
            "author_id": message.author.id,
            "speaker_name": speaker_name,
            "content": message.content.strip(),
        }
    )


def recent_context_text(recent_messages: dict[int, Any], channel_id: int, limit: int = 6) -> str:
    items = list(recent_messages[channel_id])[-limit:]
    return "\n".join(f"{item['speaker_name']}: {item['content']}" for item in items)


def looks_like_followup(text: str) -> bool:
    """
    Detect short conversational followups that are probably responding
    to Ultron rather than starting a brand-new topic.
    """
    text = text.lower().strip()
    if not text:
        return False

    followup_starts = (
        "i'm",
        "im",
        "i am",
        "you're",
        "youre",
        "you are",
        "yeah",
        "yes",
        "no",
        "maybe",
        "well",
        "listen",
        "look",
        "because",
        "still",
        "okay",
        "ok",
        "bro",
        "wait",
        "what",
        "how",
        "why",
        "so",
    )

    if text.startswith(followup_starts):
        return True

    if "?" in text:
        return True

    word_count = len(text.split())
    return 2 <= word_count <= 14


def looks_like_command_message(text: str) -> bool:
    text = text.strip()
    if not text:
        return False

    return text.startswith(("!", "$", ".", "/", "\\"))


def canonical_speaker_name(bot_user: discord.ClientUser | None, member: discord.abc.User) -> str:
    if bot_user is not None and member.id == bot_user.id:
        return BOT_NAME

    aliases = DISCORD_ALIASES.get(member.id)
    if aliases:
        return aliases[0]

    return member.display_name


def is_allowed_bot_author(bot_user: discord.ClientUser | None, message: discord.Message) -> bool:
    """
    True if the message author is a human, or a specifically whitelisted bot alias.
    False for Ultron itself and random bots.
    """
    if not message.author.bot:
        return True

    if bot_user is not None and message.author.id == bot_user.id:
        return False

    return message.author.id in DISCORD_ALIASES


def is_reply_to_bot_message(bot_user: discord.ClientUser | None, message: discord.Message) -> bool:
    if bot_user is None or not message.reference:
        return False

    resolved = message.reference.resolved
    if isinstance(resolved, discord.Message):
        return resolved.author.id == bot_user.id

    return False