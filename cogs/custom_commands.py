"""Custom Command Cog"""

import random
import time
import json
from typing import Dict
from discord import Message
from discord.ext.commands import Cog, command, Context, Bot
from collections import defaultdict


class C_Custom_Commands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        with open("commands.json") as f:
            self.commands: Dict[str, str] = json.load(f)

    async def __format_reply(self, s: str, ctx: Message) -> str:
        _msg = ctx.content.split()[1:]
        return s.format(
            **{i: j for i, j in enumerate(_msg)},
            **{
                "author": ctx.author.display_name,
            }
        )

    @Cog.listener()
    async def on_message(self, ctx: Message):
        if ctx.author != self.bot.user:
            start = ctx.content.split()[0]
            if start in self.commands.keys():
                await ctx.channel.send(self.__format_reply(self.commands[start], ctx))

    @command(aliases=("editcom",))
    async def addcom(self, ctx: Message):
        _msg = ctx.content.split()
        self.commands[_msg[0]] = _msg[1:]

    @command()
    async def delcom(self, ctx: Message):
        if ctx.content.split()[0] in self.commands:
            del self.commands[ctx.content.split()[0]]


def setup(bot: Bot):
    bot.add_cog(C_Custom_Commands(bot))
