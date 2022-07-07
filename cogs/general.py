"""General purpose cog"""

import random
import time
from constants import HELP_MSG, JOKE_COOLDOWN, KILL_COOLDOWN
from discord import Message
from discord.ext.commands import Cog, command, Context, Bot
from collections import defaultdict


class C_General(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.remove_command("help")
        self.kill_attempt = defaultdict(lambda: float("-inf"))
        self.last_joke = float("-inf")

    @Cog.listener()
    async def on_ready(self):
        print(f"Running as {self.bot.user.name}")
        self.kill_token = "".join(
            [chr(random.randint(65, 90)) for _ in range(10)]
        )
        print(f"Kill with !c kill {self.kill_token}")

    @command()
    async def kill(self, ctx: Context):
        msg = ctx.message.content
        if time.time() - self.kill_attempt[ctx.message.author.id] < KILL_COOLDOWN:
            await ctx.reply(f"Please wait {KILL_COOLDOWN}s between kill attempts")
        elif msg.endswith(self.kill_token):
            await ctx.reply("Cya!")
            quit()
        else:
            await ctx.reply(f"Invalid token, retry in {KILL_COOLDOWN}s")
            self.kill_attempt[ctx.message.author.id] = time.time()

    @command()
    async def help(self, ctx: Context):
        await ctx.send(HELP_MSG)


def setup(bot: Bot):
    bot.add_cog(C_General(bot))
