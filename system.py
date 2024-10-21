import asyncio
from discord.ext import commands
import configparser
import sys

CONFIG_FILE_PATH = 'config.ini'
CONFIG_SECTION = 'Extensions'

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

class System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx):
        for _ , value in config.items(CONFIG_SECTION):
            await self.bot.reload_extension(value)
            
        await ctx.send("Reloading complete.")
        
    @commands.command()
    async def stop_bot(self, ctx):
        await ctx.send("Stop the BOT.")
        sys.exit()
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            message = await ctx.send("そのコマンドは存在しません。")
            await asyncio.sleep(2)
            await message.delete()
    
            
async def setup(bot):
    await bot.add_cog(System(bot))