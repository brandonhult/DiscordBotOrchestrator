import asyncio
import time
from collections import defaultdict, deque

import discord
from discord.ext import commands

from BotScripts.individuals.TonySoprano.features.helpers import (
    canonical_speaker_name,
    contains_direct_address,
    contains_trigger_topic,
    is_allowed_bot_author,
    is_reply_to_bot_message,
    looks_like_command_message,
    looks_like_followup,
    member_variants,
    recent_context_text,
    remember_message,
    soften_name_overuse,
)
from BotScripts.individuals.TonySoprano.features.llm import generate_tony_reply_sync
from BotScripts.individuals.TonySoprano.utils.logger import logger
from BotScripts.shared.text_cleaner import sanitize_name_for_llm

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_window_seconds = 12
        self.spam_threshold = 3

        self.channel_reply_cooldowns = defaultdict(float)
        self.user_reply_cooldowns = defaultdict(float)

        self.auto_channel_cooldown = 25
        self.auto_user_cooldown = 20

        self.pending_followups: dict[int, dict[str, float | int]] = {}
        self.recent_messages = defaultdict(lambda: deque(maxlen=8))

    # Hello
    @commands.command()
    async def hello(self, ctx):
        logger.info("%s used %s", ctx.author, ctx.message.content)
        await ctx.send("Hey how ya doin?")

    # Goodbye
    @commands.command()
    async def goodbye(self, ctx):
        logger.info("%s used %s", ctx.author, ctx.message.content)
        await ctx.send("Alright")

    # Goodbye
    @commands.command()
    async def mob(self, ctx):
        logger.info("%s used %s", ctx.author, ctx.message.content)
        await ctx.send("The what?! You mean the waste management business.")

    def _set_pending_followup(
            self,
            message: discord.Message,
            turns_left: int = 1,
            ttl_seconds: float = 15.0,
    ) -> None:
        self.pending_followups[message.channel.id] = {
            "user_id": message.author.id,
            "expires_at": time.time() + ttl_seconds,
            "turns_left": turns_left,
        }

    def _has_pending_followup(self, message: discord.Message) -> bool:
        state = self.pending_followups.get(message.channel.id)
        if not state:
            return False

        if time.time() > state["expires_at"]:
            self.pending_followups.pop(message.channel.id, None)
            return False

        return state["user_id"] == message.author.id and state["turns_left"] > 0

    def _consume_pending_followup(self, message: discord.Message) -> None:
        state = self.pending_followups.get(message.channel.id)
        if not state:
            return

        state["turns_left"] -= 1
        if state["turns_left"] <= 0:
            self.pending_followups.pop(message.channel.id, None)

    def _should_auto_reply(self, message: discord.Message) -> tuple[bool, str | None]:
        if not message.guild:
            return False, None

        if not message.content:
            return False, None

        if not is_allowed_bot_author(self.bot.user, message):
            return False, None

        if self.bot.user and message.author.id == self.bot.user.id:
            return False, None

        text = message.content.lower().strip()

        if looks_like_command_message(text):
            return False, None

        if self.bot.user and self.bot.user in message.mentions:
            return True, "direct"

        if contains_direct_address(text):
            return True, "direct"

        if is_reply_to_bot_message(self.bot.user, message):
            return True, "followup"

        if not message.author.bot and self._has_pending_followup(message) and looks_like_followup(text):
            self._consume_pending_followup(message)
            return True, "followup"

        if message.author.bot and contains_trigger_topic(text):
            return True, "followup"

        if contains_trigger_topic(text):
            return True, "trigger"

        return False, None

    def _auto_reply_on_cooldown(self, message: discord.Message) -> bool:
        now = time.time()

        channel_last = self.channel_reply_cooldowns[message.channel.id]
        user_last = self.user_reply_cooldowns[message.author.id]

        if now - channel_last < self.auto_channel_cooldown:
            return True

        if now - user_last < self.auto_user_cooldown:
            return True

        return False

    def _mark_auto_reply(self, message: discord.Message) -> None:
        now = time.time()
        self.channel_reply_cooldowns[message.channel.id] = now
        self.user_reply_cooldowns[message.author.id] = now

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        remember_message(self.recent_messages, self.bot.user, message)

        try:
            should_reply, reason = self._should_auto_reply(message)
            if not should_reply:
                return

            if reason == "trigger" and self._auto_reply_on_cooldown(message):
                return

            target_name = sanitize_name_for_llm(
                canonical_speaker_name(self.bot.user, message.author)
            )

            self._mark_auto_reply(message)

            if reason == "trigger":
                dynamic_entities = member_variants(message.author)
                favored_entities = [v["text"] for v in dynamic_entities]
                return

            context_text = recent_context_text(
                self.recent_messages,
                message.channel.id,
                limit=6,
            )

            async with message.channel.typing():
                reply = await asyncio.to_thread(
                    generate_tony_reply_sync,
                    target_name,
                    message.content,
                    context_text,
                    reason,
                )

            reply = soften_name_overuse(reply, target_name)

            sent = await message.reply(reply, mention_author=False)
            remember_message(self.recent_messages, self.bot.user, sent)

            turns_left = 2 if "?" in reply else 1
            self._set_pending_followup(
                message,
                turns_left=turns_left,
                ttl_seconds=15.0,
            )

        except Exception as e:
            logger.exception("Tony auto-reply failed: %s", e)

async def setup(bot):
    await bot.add_cog(General(bot))