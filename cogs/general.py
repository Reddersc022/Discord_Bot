"""General purpose cog"""

import logging
from constants import HELP_MSG
from discord.ext.commands import Cog, command, Context, Bot


class C_General(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.bot.remove_command("help")

    @Cog.listener()
    async def on_ready(self):
        print(f"Running as {self.bot.user.name}")

    @command()
    async def help(self, ctx: Context):
        await ctx.send(HELP_MSG)


def setup(bot: Bot):
    bot.add_cog(C_General(bot))
