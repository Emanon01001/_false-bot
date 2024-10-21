import subprocess
from discord.ext import commands
import asyncio

class NetWorkSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx, host=None):
        """
        Botの応答時間を計測します
        """
        
        if host is None:
            rpl = await ctx.send("↓↓↓")

            msgtime = ctx.message.created_at.timestamp()
            rpltime = rpl.created_at.timestamp()

            ping_sec = rpltime - msgtime
            ping_ms = ping_sec * 1000
            ping_ms_str = "%.2f" % ping_ms
            latency_ms = self.bot.latency * 1000
            latency_ms_str = "%.2f" % latency_ms

            await rpl.edit(
                content="結果\n"
                f"Message: {ping_ms_str}ms\n"
                f"Latency: {latency_ms_str}ms\n"
            )

        else:
            message = await ctx.send(f"`{host}`へPingを実行します")
            p = await asyncio.create_subprocess_exec(
                "ping", "-c", "3", host, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            stdout, stderr = await p.communicate()
            unix_ping = stdout.decode() + stderr.decode()

            await message.edit(content="`" * 3 + "\n" + unix_ping + "`" * 3)
            
async def setup(bot):
    await bot.add_cog(NetWorkSystem(bot))