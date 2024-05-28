import discord
from discord.ext import commands
import yt_dlp as youtube_dl

class YouTubeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def juca(self, ctx, url: str):
        # Verifica se o autor está em um canal de voz
        if ctx.author.voice is None:
            await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
            return

        channel = ctx.author.voice.channel

        # Conecta ao canal de voz
        if ctx.voice_client is None:
            vc = await channel.connect()
            print("Conectado ao canal de voz.")
        else:
            vc = ctx.voice_client
            await vc.move_to(channel)
            print("Movido para o canal de voz.")

        # Opções do youtube-dl
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    info = info['entries'][0]

                # Encontrar URL de áudio
                audio_url = None
                for format in info['formats']:
                    if format.get('acodec') != 'none' and 'url' in format:
                        audio_url = format['url']
                        break

                if not audio_url:
                    await ctx.send("Não foi possível encontrar um URL de áudio válido.")
                    return

                title = info.get('title', 'Audio')
                print(f"URL do áudio: {audio_url}")
                print(f"Título do áudio: {title}")

            # Verificar se o bot já está tocando algo
            if vc.is_playing():
                vc.stop()
                print("Parando áudio anterior.")

            # Toca o áudio no canal de voz
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn'
            }
            vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options), after=lambda e: print(f'Erro: {e}') if e else None)
            print("Áudio sendo tocado.")
            await ctx.send(f'Tocando agora: {title}')
        except Exception as e:
            await ctx.send(f"Ocorreu um erro ao tentar tocar o áudio: {str(e)}")
            print(f"Ocorreu um erro: {str(e)}")

    @commands.command()
    async def parar(self, ctx):
        # Para de tocar e desconecta do canal de voz
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            print("Desconectado do canal de voz.")

async def setup(bot):
    await bot.add_cog(YouTubeCog(bot))