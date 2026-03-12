from BotScripts.individuals.TonySoprano.app.client import client
from BotScripts.individuals.TonySoprano.utils.logger import logger

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    logger.info(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    logger.info(f"{message.author}: {message.content}")

    mention = f'<@!{client.user.id}>'
    if mention in message.content:
        await message.channel.send("You mentioned me")

    await client.process_commands(message)