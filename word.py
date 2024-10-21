from discord.ext import commands
import deepl

API_KEY = "4e3f366c-7910-fdc4-f222-c8829a16c9b6:fx"

class Word(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def trans(self, ctx, language, word):
        translator = deepl.Translator(API_KEY)
        result = translator.translate_text(word, source_lang=language, target_lang='EN')
        await ctx.send(result)
        
    @commands.command()
    async def やれ(self, ctx):
        for n in range(50):
            await ctx.send("*^^*")
        
        
async def setup(bot):
    await bot.add_cog(Word(bot))
        