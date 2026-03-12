import asyncio
import random
import time

import discord

from BotScripts.individuals.Boyd.features.helpers import remember_message
from BotScripts.individuals.Boyd.utils.logger import logger


class Scheduler:
    def __init__(self, bot):
        self.bot = bot

        # Wake up every hour and decide whether Boyd says something.
        self.check_interval_seconds = 3600

        # Chance Boyd speaks on each check.
        self.speak_chance = 0.20

        # If Boyd speaks, chance he uses a delayed reaction to something
        # suspicious someone said earlier.
        self.delayed_reaction_chance = 0.50

        # If not using delayed reaction, chance he rambles instead of saying
        # a short paranoid line.
        self.ramble_chance = 0.30

        # Only consider channels with recent human activity.
        self.recent_activity_window_seconds = 7200

        # Avoid posting immediately after a human message.
        self.minimum_silence_seconds = 60

        # Scheduler-specific governor behavior.
        self.scheduler_reply_chance = 0.25
        self.scheduler_dropout_chance = 0.35

    async def run(self):
        logger.info("BOYD scheduler file loaded: %s", __file__)
        await self.bot.wait_until_ready()
        logger.info("Boyd scheduler started")

        while not self.bot.is_closed():
            await asyncio.sleep(self.check_interval_seconds)

            try:
                await self.maybe_speak()
            except Exception as e:
                logger.exception("Boyd scheduler failed: %s", e)

    async def maybe_speak(self):
        logger.info("BOYD scheduler using Boyd message logic")
        if self.bot.user is None:
            return

        if random.random() > self.speak_chance:
            logger.info("Boyd scheduler rolled no message")
            return

        cog = self.bot.get_cog("General")
        if cog is None:
            logger.warning("Boyd scheduler could not find General cog")
            return

        channel = await self.pick_channel()
        if channel is None:
            logger.info("Boyd scheduler found no eligible channel")
            return

        allowed = self.bot.conversation_governor.can_bot_reply(
            channel_id=channel.id,
            bot_id=self.bot.user.id,
            base_chance=self.scheduler_reply_chance,
            is_direct=False,
            is_trigger=False,
        )
        if not allowed:
            logger.info("Boyd scheduler blocked by governor in #%s", channel.name)
            return

        message = None

        # First try delayed paranoia.
        if random.random() < self.delayed_reaction_chance:
            eligible = self.get_eligible_delayed_triggers(cog, channel.id)
            if eligible:
                item = random.choice(eligible)
                message = self.build_delayed_reaction(item)

        # If no delayed reaction was chosen/generated, fall back to either
        # ramble or short paranoid line.
        if not message:
            if random.random() < self.ramble_chance:
                parts = cog.rambler.ramble_parts()[:3]
                message = "\n".join(part for part in parts if part).strip()
            else:
                message = random.choice(
                    [
                        "...No. No, that's not right.",
                        "Did somebody move that?",
                        "I'm getting close...",
                        "Too quiet. That's how they do it.",
                        "I heard something in the walls.",
                        "Somebody said too much earlier.",
                        "You ever get the feeling they're waiting? Watching?",
                        "No, see, that's the problem. Nobody notices.",
                    ]
                )

        if not message:
            logger.info("Boyd scheduler had nothing to send")
            return

        logger.info("Boyd scheduler sending message to #%s: %s", channel.name, message[:120])

        sent = await channel.send(message)

        self.bot.conversation_governor.register_bot_reply(
            channel_id=channel.id,
            bot_id=self.bot.user.id,
            dropout_chance=self.scheduler_dropout_chance,
        )

        remember_message(cog.recent_messages, self.bot.user, sent)

    async def pick_channel(self) -> discord.TextChannel | None:
        candidates: list[discord.TextChannel] = []

        for guild in self.bot.guilds:
            me = guild.me
            if me is None:
                continue

            for channel in guild.text_channels:
                perms = channel.permissions_for(me)
                if not perms.send_messages:
                    logger.info("Skipping #%s: no send permission", channel.name)
                    continue

                try:
                    history = [msg async for msg in channel.history(limit=1)]
                except Exception as e:
                    logger.info("Skipping #%s: history fetch failed: %s", channel.name, e)
                    continue

                if not history:
                    logger.info("Skipping #%s: no message history", channel.name)
                    continue

                last_message = history[0]

                if last_message.author.bot:
                    logger.info(
                        "Skipping #%s: last message was by bot %s",
                        channel.name,
                        last_message.author,
                    )
                    continue

                if self.bot.user and last_message.author.id == self.bot.user.id:
                    logger.info(
                        "Skipping #%s: last message was Boyd himself",
                        channel.name,
                    )
                    continue

                age = (discord.utils.utcnow() - last_message.created_at).total_seconds()

                if age > self.recent_activity_window_seconds:
                    logger.info(
                        "Skipping #%s: last activity too old (%.1fs)",
                        channel.name,
                        age,
                    )
                    continue

                if age < self.minimum_silence_seconds:
                    logger.info(
                        "Skipping #%s: too recent (%.1fs)",
                        channel.name,
                        age,
                    )
                    continue

                candidates.append(channel)
                logger.info(
                    "Eligible channel found: #%s (last message %.1fs ago by %s)",
                    channel.name,
                    age,
                    last_message.author,
                )

        if not candidates:
            return None

        return random.choice(candidates)

    def get_eligible_delayed_triggers(self, cog, channel_id: int) -> list[dict]:
        now = time.time()
        eligible = []

        for item in cog.delayed_triggers:
            if item["channel_id"] != channel_id:
                continue

            age = now - item["created_at"]

            # At least 10 minutes old, at most 6 hours old.
            if 600 <= age <= 21600:
                eligible.append(item)

        return eligible

    def build_delayed_reaction(self, item: dict) -> str:
        author_name = item["author_name"]
        content = item["content"].strip()
        safe_excerpt = content[:80]

        templates = [
            f"{author_name}... that's what it was.",
            f"I keep thinking about what {author_name} said.",
            f"{author_name} said \"{safe_excerpt}\". That's not a normal thing to say.",
            f"No, see, that's how it starts. {author_name} said too much.",
            f"That line from {author_name} is still bothering me.",
            f"{author_name} knew something. I could hear it in the words.",
            f"I didn't like it when {author_name} said \"{safe_excerpt}\".",
        ]

        return random.choice(templates)