import asyncio
import random
import time
from collections import defaultdict, deque

import discord
from discord.ext import commands

from BotScripts.individuals.Boyd.features.helpers import (
    build_dynamic_entities,
    canonical_speaker_name,
    contains_direct_address,
    contains_trigger_topic,
    dedupe_parts,
    is_allowed_bot_author,
    is_reply_to_bot_message,
    looks_like_command_message,
    looks_like_followup,
    member_variants,
    recent_context_text,
    remember_message,
    soften_name_overuse,
)
from BotScripts.individuals.Boyd.features.llm import generate_boyd_reply_sync
from BotScripts.individuals.Boyd.features.rambler import Rambler
from BotScripts.individuals.Boyd.utils.logger import logger
from BotScripts.shared.text_cleaner import sanitize_name_for_llm


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rambler = Rambler()
        self.delayed_triggers = deque(maxlen=40)

        self.ramble_history = defaultdict(lambda: deque(maxlen=6))

        self.spam_window_seconds = 12
        self.spam_threshold = 3

        self.channel_reply_cooldowns = defaultdict(float)
        self.user_reply_cooldowns = defaultdict(float)

        self.auto_channel_cooldown = 25
        self.auto_user_cooldown = 20

        self.pending_followups: dict[int, dict[str, float | int]] = {}
        self.recent_messages = defaultdict(lambda: deque(maxlen=8))

    @commands.command()
    async def hello(self, ctx):
        logger.info("%s used %s", ctx.author, ctx.message.content)
        await ctx.send("Hello!")

    @commands.command()
    async def ramble(self, ctx):
        logger.info("%s used %s", ctx.author, ctx.message.content)

        dynamic_entities, favored_entities = build_dynamic_entities(
            ctx.guild,
            ctx.author,
            include_bots=False,
        )

        force_dynamic_entity = random.random() < 0.75

        if self._is_spamming(ctx.author.id):
            logger.info("%s triggered ramble spam safeguard", ctx.author)
            parts = self.rambler.spam_response()

            for part in parts:
                async with ctx.typing():
                    await asyncio.sleep(random.uniform(0.3, 0.8))
                await ctx.send(part)

            await asyncio.sleep(random.uniform(0.6, 1.2))

            if random.random() < 0.5:
                parts = dedupe_parts(
                    self.rambler.ramble_parts(
                        dynamic_entities=dynamic_entities,
                        favored_entities=favored_entities,
                        force_dynamic_entity=True,
                    )[:2]
                )

                for part in parts:
                    async with ctx.typing():
                        await asyncio.sleep(random.uniform(0.3, 0.9))
                    await ctx.send(part)
                    await asyncio.sleep(random.uniform(0.2, 0.6))
            return

        parts = dedupe_parts(
            self.rambler.ramble_parts(
                dynamic_entities=dynamic_entities,
                favored_entities=favored_entities,
                force_dynamic_entity=force_dynamic_entity,
            )
        )

        for part in parts:
            async with ctx.typing():
                await asyncio.sleep(random.uniform(0.4, 1.2))
            await ctx.send(part)
            await asyncio.sleep(random.uniform(0.2, 0.8))

    @commands.command()
    async def accuse(self, ctx, member: commands.MemberConverter):
        logger.info("%s used %s", ctx.author, ctx.message.content)

        dynamic_entities, _ = build_dynamic_entities(
            ctx.guild,
            ctx.author,
            include_bots=True,
        )

        forced_variants = member_variants(member)
        non_mention_variants = [
            v for v in forced_variants if not v["text"].startswith("<@")
        ]
        forced_entity = random.choice(non_mention_variants or forced_variants)

        parts = self.rambler.accuse_parts(
            forced_entity=forced_entity,
            dynamic_entities=dynamic_entities,
            suspect_member_id=member.id,
        )

        for part in parts:
            async with ctx.typing():
                await asyncio.sleep(random.uniform(0.4, 1.0))
            await ctx.send(part)
            await asyncio.sleep(random.uniform(0.2, 0.7))

    @commands.command()
    async def suspicion(self, ctx, member: commands.MemberConverter = None):
        target = member or ctx.author
        score = self.rambler.get_suspicion(target.id)
        await ctx.send(f"{target.display_name} suspicion score: {score}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearsuspicion(self, ctx, member: commands.MemberConverter):
        self.rambler.clear_suspicion(member.id)
        logger.info("%s cleared suspicion for %s", ctx.author, member)
        await ctx.send(f"Cleared suspicion for {member.display_name}.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearsuspicionall(self, ctx):
        self.rambler.clear_suspicion()
        logger.info("%s cleared all suspicion memory", ctx.author)
        await ctx.send("Cleared all suspicion memory.")

    def _is_spamming(self, user_id: int) -> bool:
        now = time.time()
        history = self.ramble_history[user_id]
        history.append(now)
        recent_count = sum(1 for ts in history if now - ts <= self.spam_window_seconds)
        return recent_count >= self.spam_threshold

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

    def remember_delayed_trigger(self, message: discord.Message) -> None:
        text = message.content.strip()
        if not text:
            return

        self.delayed_triggers.append(
            {
                "channel_id": message.channel.id,
                "author_id": message.author.id,
                "author_name": canonical_speaker_name(self.bot.user, message.author),
                "content": text,
                "created_at": time.time(),
            }
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        remember_message(self.recent_messages, self.bot.user, message)

        try:
            if not message.content:
                return

            text = message.content.lower().strip()

            if (
                    not message.author.bot
                    and message.guild
                    and contains_trigger_topic(text)
            ):
                self.remember_delayed_trigger(message)

            should_reply, reason = self._should_auto_reply(message)
            if not should_reply:
                return

            if reason == "trigger" and self._auto_reply_on_cooldown(message):
                return

            target_name = sanitize_name_for_llm(
                canonical_speaker_name(self.bot.user, message.author)
            )
            suspicion = self.rambler.get_suspicion(message.author.id)

            self._mark_auto_reply(message)

            if reason == "trigger":
                dynamic_entities = member_variants(message.author)
                favored_entities = [v["text"] for v in dynamic_entities]

                parts = dedupe_parts(
                    self.rambler.ramble_parts(
                        dynamic_entities=dynamic_entities,
                        favored_entities=favored_entities,
                        force_dynamic_entity=True,
                    )[:2]
                )

                if parts:
                    async with message.channel.typing():
                        await asyncio.sleep(random.uniform(0.4, 1.0))
                    sent = await message.reply("\n".join(parts), mention_author=False)
                    remember_message(self.recent_messages, self.bot.user, sent)
                return

            quotes = self.rambler.ramble_parts()[:1]
            context_text = recent_context_text(
                self.recent_messages,
                message.channel.id,
                limit=6,
            )

            async with message.channel.typing():
                reply = await asyncio.to_thread(
                    generate_boyd_reply_sync,
                    target_name,
                    suspicion,
                    message.content,
                    quotes,
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
            logger.exception("Boyd auto-reply failed: %s", e)
        finally:
            await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(General(bot))