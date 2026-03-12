import discord
from discord.ext import commands

from BotScripts.shared.runtime import conversation_governor
from BotScripts.individuals.Boyd.utils.logger import logger
from BotScripts.individuals.Boyd.app.scheduler import Scheduler


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix="$",
            intents=intents,
        )

        self.conversation_governor = conversation_governor

    async def setup_hook(self):
        logger.info("Boyd setup_hook starting")
        await self.load_extension("BotScripts.individuals.Boyd.cogs.general")
        await self.load_extension("BotScripts.individuals.Boyd.cogs.admin")
        logger.info("Boyd extensions loaded")

        self.scheduler = Scheduler(self)
        self.loop.create_task(self.scheduler.run())

    async def on_ready(self):
        logger.info("Boyd connected as %s (%s)", self.user, self.user.id)


def create_bot():
    logger.info("Creating Boyd bot instance")
    return MyBot()


async def start_bot(token: str):
    if not token:
        raise RuntimeError("BOYD_TOKEN is missing or empty")

    logger.info("Starting Boyd bot")
    bot = create_bot()
    await bot.start(token)