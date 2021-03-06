"""Main script for my discord bot"""

# Imports
import os
import time
import re

from dotenv import load_dotenv
from discord.ext import commands

# Constants
COMMANDS = ["help", "hello_world", "wilbur"]
COMM_STR = ", ".join(f"`{comm}`" for comm in COMMANDS)

# Setup environment and bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!!")
bot.remove_command("help")


# My functions
def log(type_: str, **kwargs):
    """For logging events
    Common type_s:
        - connected, command, message sent, error, reply
    Common kwargs:
        - author, message"""

    lst = [f"type: {type_}"]
    for key in kwargs:
        lst.append(f"{key}: {kwargs[key]}")

    with open("log.txt", "a") as f:
        f.write(f"{time.strftime('%m/%d/%Y@%H:%M:%S')} | {', '.join(lst)}\n")


# Bot events
@bot.event
async def on_ready():
    """Invoked when bot connects to discord"""
    log("connected")


@bot.event
async def on_message(message):
    """Just a lil' inside joke"""
    await bot.process_commands(message)

    if re.search(r"kids", message.content) and not message.author.bot:
        await message.reply("Joe likes kids")
        log("reply", author=message.author, message="Joe likes kids")


# Bot commands
@bot.command("help")
async def helpMsg(ctx):
    """Displays help message"""
    message = f"""
    Prefix: `!!`
    Display this message: `help`
    All commands: {COMM_STR}
    
    Made by: redders02#8850
    More information on https://github.com/Reddersc022/Discord_Bot
"""
    await ctx.send(message)
    log("command", author=ctx.author.name + ctx.author.discriminator, message=ctx.message.content)
    log("message sent", message="help message")


@bot.command("hello_world")
async def helloWorld(ctx):
    """Simple hello world command"""
    message = f"Hello, {ctx.author}!"

    await ctx.send(message)
    log("command", author=ctx.author.name + ctx.author.discriminator, message=ctx.message.content)
    log("message sent", message=message)


@bot.command("wilbur")
async def playWilbur(ctx):
    """Gets rhythm to play the following playlist"""
    message = f"!play https://www.youtube.com/watch?v=M9jSeLeHZI0&list=PLToII9A82qUbBMDaeyDWBYYQPNbWoJYgc"

    await ctx.senf(message)
    log("command", author=ctx.author.name + ctx.author.discriminator, message=ctx.message.content)
    log("message", message=message)


@bot.event
async def on_command_error(ctx, error):
    """Handles errors"""
    await ctx.send(error)
    log("error", error=error, author=ctx.author.name + ctx.author.discriminator)


# Let's go!
bot.run(TOKEN)
