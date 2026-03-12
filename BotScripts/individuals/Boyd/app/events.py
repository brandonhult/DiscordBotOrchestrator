import asyncio

from BotScripts.individuals.TonySoprano.app.client import client
from BotScripts.individuals.TonySoprano.features.llm import warm_tony_model
from BotScripts.individuals.TonySoprano.utils.logger import logger


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    logger.info(f"Logged in as {client.user}")
    await asyncio.to_thread(warm_tony_model)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    logger.info(f"{message.author}: {message.content}")


    await client.process_commands(message)

