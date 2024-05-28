import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Carregar todos os Cogs
initial_extensions = [
    'cogs.example_cog'
]

async def main():
    # Carregar todas as extensões (Cogs)
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

    # Verificar se o token está presente
    if not config.TOKEN:
        print("O token do bot não foi configurado. Por favor, defina o token em config.py.")
        return

    # Rodar o bot somente se o token estiver presente
    await bot.start(config.TOKEN)

if __name__ == '__main__':
    import asyncio
    import sys
    import traceback

    asyncio.run(main())