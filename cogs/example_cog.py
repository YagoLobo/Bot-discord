from discord.ext import commands

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ivan(self, ctx):
        await ctx.send('Arrasou!')

async def setup(bot):
    await bot.add_cog(ExampleCog(bot))