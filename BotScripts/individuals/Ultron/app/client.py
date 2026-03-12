import discord
from discord.ext import commands

from BotScripts.shared.runtime import conversation_governor
from BotScripts.individuals.Ultron.utils.logger import logger



class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

        self.conversation_governor = conversation_governor

    async def setup_hook(self):
        logger.info("Ultron setup_hook starting")
        await self.load_extension("BotScripts.individuals.Ultron.cogs.general")
        await self.load_extension("BotScripts.individuals.Ultron.cogs.admin")
        logger.info("Ultron extensions loaded")

    async def on_ready(self):
        logger.info("Ultron connected as %s (%s)", self.user, self.user.id)


def create_bot():
    logger.info("Creating Ultron bot instance")
    return MyBot()


async def start_bot(token: str):
    if not token:
        raise RuntimeError("ULTRON_TOKEN is missing or empty")

    logger.info("Starting Ultron bot")
    bot = create_bot()
    await bot.start(token)