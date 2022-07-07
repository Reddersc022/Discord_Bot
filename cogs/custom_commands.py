"""Custom Command Cog"""

import random
import time
import json
from discord import Message
from typing import Dict
from discord.ext.commands import Cog, command, Context, Bot
from collections import defaultdict


class C_Custom_Commands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        with open("commands.json") as f:
            self.commands: Dict[str, str] = json.load(f)

    def __format_reply(self, s: str, m: Message) -> str:
        _msg = m.content.split()[1:]
        return s.format(
            **{i: j for i, j in enumerate(_msg)},
            **{
                "author": m.author.display_name,
            }
        )

    @Cog.listener()
    async def on_message(self, msg: Message):
        if msg.author != self.bot.user:
            start = msg.content.split()[0]
            if start in self.commands.keys():
                await msg.channel.send(self.__format_reply(self.commands[start], msg))

    @command(aliases=("editcom",))
    async def addcom(self, ctx: Context):
        msg: Message = ctx.message
        _msg = msg.content.split()
        self.commands[_msg[0]] = _msg[1:]

    @command()
    async def delcom(self, ctx: Context):
        msg: Message = ctx.message
        if msg.content.split()[0] in self.commands:
            del self.commands[msg.content.split()[0]]


def setup(bot: Bot):
    bot.add_cog(C_Custom_Commands(bot))
