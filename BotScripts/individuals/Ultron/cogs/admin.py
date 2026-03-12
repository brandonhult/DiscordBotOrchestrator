from discord.ext import commands
from BotScripts.individuals.Ultron.utils.logger import logger

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ping(self, ctx):
        logger.info("%s used %s", ctx.author, ctx.message.content)
        await ctx.send("Pong!")

    @commands.command()
    @commands.is_owner()
    async def purge(self, ctx, amount: int = 50):
        """Delete a number of messages from the channel"""

        logger.info(f"{ctx.author} purged {amount} messages in #{ctx.channel}")

        deleted = await ctx.channel.purge(limit=amount + 1)

        confirmation = await ctx.send(f"Deleted {len(deleted) - 1} messages.")
        await confirmation.delete(delay=3)

async def setup(bot):
    await bot.add_cog(Admin(bot))