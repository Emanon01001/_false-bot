from discord.ext import commands
import configparser

CONFIG_FILE_PATH = 'config.ini'
CONFIG_SECTION = 'Extensions'

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH, encoding='utf-8')

class MyBot(commands.Bot):
    
    async def process_commands(self, message):
        if message.author.bot:
            return
        
        ctx = await self.get_context(message)
            
        if not await self.check_commands(ctx):
            return
        await self.invoke(ctx)
        
    async def setup_hook(self):
        for _ , value in config.items(CONFIG_SECTION):
            await bot.load_extension(value)
        
        
bot = MyBot(command_prefix="!")
    
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)
        
@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}")
    
    channel_id = 1209093614219563019
    channel = bot.get_channel(channel_id)
    
    if channel:
        await channel.send("Bot is ready")
    else:
        print("Channe not found.")
       
@bot.event     
async def check_commands(ctx):
    allowed_user_id = [1046049644569960561, 586342618456129552]
    return ctx.author.id == allowed_user_id[0] or allowed_user_id[1]
    
bot.run(config['Token']['token_1'])