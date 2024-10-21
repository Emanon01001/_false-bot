import asyncio
import random
import discord
from discord.ext import commands
import yt_dlp
from pytube import Playlist
from urllib.parse import urlparse

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class AudioSystem(commands.Cog):
    def __init__(self, bot):
        self.loop = asyncio.get_event_loop()
        self.bot = bot
        
    
    @commands.command()
    async def leave(self, ctx):
        if not ctx.voice_client:
            await ctx.send("I am not connected to a voice channel.")
            return
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, url):
        
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send("You need to be in a voice channel to use this command.")
            return
        
        channel = ctx.author.voice.channel
        voice_client = ctx.voice_client
        
        if voice_client is None:
            voice_client = await channel.connect()
        else:
            if voice_client.channel != channel:
                await voice_client.move_to(channel)
        
        if "list" in url and "RD" in url:
            ydl_opts = {
                'extract_flat': True,
                'quiet': True,
                'force_generic_extractor': True,
                'dump_single_json': True,
                'simulate': True,
                'playlistend': 26
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=False)
                mix_urls = [entry['url'] for entry in result['entries']]
                for i in range(0, 100):
                    source = await YTDLSource.from_url(mix_urls[i], loop=self.loop, stream=True)
                    voice_client.play(source)
                    while voice_client.is_playing() or voice_client.is_paused():
                        await asyncio.sleep(1)
                    
        elif "list" in url or youtube_url(url):
            url_list = []
            playlist = Playlist(url)
            video_url = playlist.video_urls
            for urls in video_url:
                url_list.append(urls)
                source = await YTDLSource.from_url(urls, loop=self.loop, stream=True)
                voice_client.play(source)
                while voice_client.is_playing() or voice_client.is_paused():
                    await asyncio.sleep(1)
        else:
            source = await YTDLSource.from_url(url, loop=self.loop, stream=True)
            voice_client.play(source)
            while voice_client.is_playing() or voice_client.is_paused():
                await asyncio.sleep(1)
                
    @commands.command()
    async def test(self, ctx):
        embed = discord.Embed(title="Hi!!")
        await ctx.send(embed=embed)
            
    @commands.command()
    async def pause(self, ctx):
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.pause()
            await ctx.send("Paused.")
        elif voice_client.is_paused():
            await ctx.send("Paused.")
        else:
            await ctx.send("Nothing is playing")
            
    @commands.command()
    async def resume(self, ctx):
        voice_client = ctx.voice_client
        if voice_client.is_paused():
            voice_client.resume()
            await ctx.send("Resumed.")
        else:
            await ctx.send("Nothing is playing.")
            
    @commands.command()
    async def skip(self, ctx):
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Skipped the current song.")
        else:
            await ctx.send("There is no song playing to skip.")

def youtube_url(url):
    url_p = urlparse(url)
    if "youtube" in url_p.hostname:
        return True
    else:
        return False
    
async def setup(bot):
    await bot.add_cog(AudioSystem(bot))