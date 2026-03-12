from discord.ext import commands
from BotScripts.individuals.TonySoprano.utils.logger import logger

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        logger.info(f"{ctx.author} used !ping")
        await ctx.send("Pong!")

async def setup(bot):
    await bot.add_cog(Admin(bot))