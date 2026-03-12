from discord.ext import commands
from BotScripts.individuals.Boyd.utils.logger import logger

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        logger.info("%s used %s", ctx.author, ctx.message.content)
        await ctx.send("Pong!")

async def setup(bot):
    await bot.add_cog(Admin(bot))