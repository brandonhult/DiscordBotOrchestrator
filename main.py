import asyncio
import os
from plistlib import load
from dotenv import load_dotenv
from BotScripts.shared.runtime import conversation_governor
from BotScripts.individuals.Ultron.app.client import start_bot as start_ultron
from BotScripts.individuals.TonySoprano.app.client import start_bot as start_tony
from BotScripts.individuals.Boyd.app.client import start_bot as start_boyd


load_dotenv()
ULTRON_TOKEN = os.getenv("ULTRON_TOKEN")
TONY_TOKEN = os.getenv("TONY_TOKEN")
BOYD_TOKEN = os.getenv("BOYD_TOKEN")


async def main():
    await asyncio.gather(
        start_ultron(ULTRON_TOKEN),
        start_tony(TONY_TOKEN),
        start_boyd(BOYD_TOKEN),
    )


if __name__ == "__main__":
    asyncio.run(main())
