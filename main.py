"""Main script for my discord bot"""

# Imports
import os
import time
import re
import asyncio
import json

from dotenv import load_dotenv
from discord.ext import commands

# Constants
COMMANDS = ["help", "hello_world", "wilbur", "reminder"]
COMM_STR = ", ".join(f"`{comm}`" for comm in COMMANDS)

# Setup environment and bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL = int(os.getenv("CHANNEL"))

bot = commands.Bot(command_prefix="!!")
bot.remove_command("help")

# Setup reminders
with open("reminders.json", "r") as f:
    global reminders
    reminders = json.load(f)


# My functions
def log(type_: str, **kwargs):
    """For logging events
    Common type_s:
        - connected, command, message sent, error, reply, reminder set, halting
    Common kwargs:
        - author, message
    """

    lst = [f"type: {type_}"]
    for key in kwargs:
        lst.append(f"{key}: {kwargs[key]}")

    with open("log.txt", "a") as f:
        f.write(f"{time.strftime('%m/%d/%Y@%H:%M:%S')} | {', '.join(lst)}\n")


async def backupReminders():
    with open("reminders.json", "w") as f:
        json.dump(reminders, f)


# Bot events
@bot.event
async def on_ready():
    """Invoked when bot connects to discord, and is ready"""
    log("connected")

    # TODO: CHANGE!!!
    channel = bot.get_channel(CHANNEL)
    message = "I'm back!"
    await channel.send(message)
    log("message sent", message=message)

    backupTimer = 0
    # For reminders
    while True:
        # Backup every 5ish mins
        if backupTimer > 300:
            await backupReminders()
            backupTimer = 0

        for rem, i in zip(reminders, range(len(reminders))):
            if time.gmtime() >= time.struct_time(rem[0]):
                # Send then delete
                message = f"Reminder: {rem[1]}"
                await channel.send(message)

                del reminders[i]

                log("message sent", message=message)

        backupTimer += 20
        await asyncio.sleep(20)


@bot.event
async def on_message(message):
    """Just a lil' inside joke"""
    await bot.process_commands(message)

    if re.search(r"kids", message.content) and not message.author.bot:
        await message.reply("Joe likes kids")
        log("reply", author=message.author, message="Joe likes kids")


@bot.event
async def on_command_error(ctx, error):
    """Handles errors"""
    log("error", error=error, author=ctx.author.name + ctx.author.discriminator)
    await ctx.send(error)


# Bot commands
@bot.command("help")
async def helpMsg(ctx):
    """Displays help message"""
    log("command", author=ctx.author.name + ctx.author.discriminator, message=ctx.message.content)
    message = f"""
    Prefix: `!!`
    Display this message: `help`
    All commands: {COMM_STR}
    
    Made by: redders02#8850
    More information on https://github.com/Reddersc022/Discord_Bot
"""
    await ctx.send(message)
    log("message sent", message="help message")


@bot.command("hello_world")
async def helloWorld(ctx):
    """Simple hello world command"""
    log("command", author=ctx.author.name + ctx.author.discriminator, message=ctx.message.content)
    message = f"Hello, {ctx.author}!"

    await ctx.send(message)
    log("message sent", message=message)


@bot.command("wilbur")
async def playWilbur(ctx):
    """Gets rhythm to play the following playlist"""
    log("command", author=ctx.author.name + ctx.author.discriminator, message=ctx.message.content)
    message = f"!play https://www.youtube.com/watch?v=M9jSeLeHZI0&list=PLToII9A82qUbBMDaeyDWBYYQPNbWoJYgc"

    await ctx.send(message)
    log("message sent", message=message)


@bot.command("reminder")
async def reminder(ctx, *args):
    """Sets reminder. Usage: !!reminder dd-mm-yy hh:mm:ss message"""
    log("command", author=ctx.author.name + ctx.author.discriminator, message=ctx.message.content)

    if args[0] == "help":
        message = "Usage: `!!reminder dd-mm-yyyy hh:mm:ss message`"
        await ctx.send(message)
        log("message sent", message=message)

    # Not help
    else:
        reminders.append((time.strptime(" ".join(args[:2]), "%d-%m-%Y %H:%M:%S"), " ".join(args[2:])))
        log("reminder set", time=" ".join(args[:2]))


@bot.command("kill")
async def kill(ctx):
    """Halts execution"""
    log("command", author=ctx.author.name + ctx.author.discriminator, message=ctx.message.content)
    if any(map(lambda x: x.name == "murderer", ctx.author.roles)):
        await backupReminders()

        message = "Dying..."
        await ctx.send(message)
        log("message sent", message=message)
        log("halting")
        await exit()
    else:
        message = "You can't kill me!"
        await ctx.send(message)
        log("message sent", message=message)


# Let's go!
bot.run(TOKEN)
