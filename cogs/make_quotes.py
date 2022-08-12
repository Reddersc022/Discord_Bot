"""Cog for forming PDF of pinned messages"""

import random
import time
import datetime
import os
from discord import Message, File
from discord.ext.commands import Cog, command, Context, Bot
from collections import defaultdict


class C_make_quotes(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        with open("cogs/template.tex") as f:
            self.template = f.read()

    @command()
    async def make_quotes_pins(self, ctx: Context):
        message: Message = ctx.message
        tex_fp = f"/tmp/pins{random.random()}"

        with open(f"{tex_fp}.tex", "w") as tex_f:
            tex_f.write(self.template % {"channel": ctx.channel.name})

            msg: Message  # For development
            async for msg in ctx.pins():
                tex_f.write(
                    "\\section*{%s -- %s}\n" % (
                        msg.author.display_name, msg.created_at.strftime(
                            "%d/%m/%Y@%H%M")
                    ) +
                    "\t\\fancyquote{\n" +
                    "\\\n".join([
                        f"\t\t{i}" for i in msg.content.split("\n")
                    ]) +
                    "\t\n}\n"
                )

            tex_f.write("\\end{document}")

        os.system(
            f"xelatex -interaction=nonstopmode -file-line-error -output-directory=/tmp {tex_fp}.tex")
        await message.reply(file=File(f"{tex_fp}.pdf"))

        print(f"Replied to {ctx.author.display_name} with {tex_fp}.pdf")

    @command()
    async def make_quotes_images(self, ctx: Context):
        message: Message = ctx.message
        tex_fp = f"/tmp/images{random.random()}"
        os.system("mkdir /tmp/images")

        with open(f"{tex_fp}.tex", "w") as tex_f:
            tex_f.write(self.template % {"channel": ctx.channel.name})

            msg: Message  # For development
            async for msg in ctx.channel.history(limit=300):
                section_done = False
                if msg.attachments:
                    for a in msg.attachments:
                        if "image" in a.content_type.lower():
                            if not section_done:
                                tex_f.write(
                                    "\\section*{%s}\n" % (
                                        msg.created_at.strftime("%d/%m/%Y@%H%M"))
                                )
                                section_done = True

                            image_fp = f"{random.random()}{a.filename}"
                            with open(f"/tmp/images/{image_fp}", "wb") as image_f:
                                await a.save(image_f)

                            tex_f.write(
                                "\t\\begin{figure}[H]\n"
                                "\t\t\\includegraphics[width=.7\\textwidth]{"
                                f"{image_fp}"
                                "}\n\t\\end{figure}\n"
                            )

            tex_f.write("\\end{document}")

        os.system(
            f"xelatex -interaction=nonstopmode -file-line-error -output-directory=/tmp {tex_fp}.tex")
        await message.reply(file=File(f"{tex_fp}.pdf"))

        print(f"Replied to {ctx.author.display_name} with {tex_fp}.pdf")


def setup(bot: Bot):
    bot.add_cog(C_make_quotes(bot))
