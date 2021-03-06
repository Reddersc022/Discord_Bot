"""Main script for my discord bot"""

# Imports
import os
import time

from dotenv import load_dotenv
from discord.ext import commands

# Constants
COMMANDS = ["help", "hello_world"]
COMM_STR = ", ".join(f"`{comm}`" for comm in COMMANDS)

# Setup environment and bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!!")
bot.remove_command("help")


# My functions
def log(type_: str, **kwargs):
    """For logging events"""

    lst = [f"type: {type_}"]
    for key in kwargs:
        lst.append(f"{key}: {kwargs[key]}")

    with open("log.txt", "a") as f:
        f.write(f"{time.strftime('%m/%d/%Y, %H:%M:%S')} | {', '.join(lst)}\n")


# Bot functions
@bot.command("help")
async def helpMsg(ctx):
    message = f"""
    Prefix: `!!`
    Display this message: `help`
    All commands: {COMM_STR}
    
    Made by: redders02#8850
"""
    await ctx.send(message)
    log("help", author=ctx.author.name + ctx.author.discriminator)


@bot.command("hello_world")
async def helloWorld(ctx):
    """Simple hello world command"""
    message = f"Hello, {ctx.author}!"

    await ctx.send(message)
    log("message sent", message=message, author=ctx.author.name + ctx.author.discriminator)


@bot.event
async def on_command_error(ctx, error):
    """Catches errors"""
    await ctx.send(error)
    log("error", error=error, author=ctx.author.name + ctx.author.discriminator)


# Let's go!
log("started")
bot.run(TOKEN)
