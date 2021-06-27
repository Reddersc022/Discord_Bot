"""Main script for my discord bot"""

# Imports
import time
import asyncio
import json

from discord.ext import commands

# Constants
COMMANDS = ["help", "hello_world", "wilbur", "reminder"]
COMM_STR = ", ".join(f"`{comm}`" for comm in COMMANDS)

# Setup environment and bot
with open("vars.json", "r") as f:
    data = json.load(f)

TOKEN = data["TOKEN"]
CHANNELS = data["CHANNELS"]

bot = commands.Bot(command_prefix="!!")
bot.remove_command("help")

# Setup reminders
with open("reminders.json", "r") as f:
    global reminders
    reminders = json.load(f)


# My functions
def log(type_: str, **kwargs):
    """For logging events
    Common `type_`s:
        - connected, command, message sent, error, reply, reminder set, halting
    Common `kwargs`:
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

    message = "Hi, I'm Charlie's bot, my prefix is `!!`.\nType !!help for more info"

    for ch in CHANNELS:
        channel = bot.get_channel(ch)
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
                channel = bot.get_channel(rem[2])
                await channel.send(message)

                del reminders[i]

                log("message sent", message=message)

        backupTimer += 20
        await asyncio.sleep(20)


@bot.event
async def on_message(message):
    """Just a lil' inside joke"""
    await bot.process_commands(message)

    if "kids" in message.content.lower() and not message.author.bot:
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
    message = f"copy-paste:`!play https://www.youtube.com/watch?v=M9jSeLeHZI0&list=PLToII9A82qUbBMDaeyDWBYYQPNbWoJYgc`"

    await ctx.send(message)
    log("message sent", message=message)


@bot.command("minecraft")
async def playWilbur(ctx):
    """Gets rhythm to play the following playlist"""
    log("command", author=ctx.author.name + ctx.author.discriminator, message=ctx.message.content)
    message = f"copy-paste:`!play https://open.spotify.com/playlist/0LLmofiC0ikfWpHZkafJdD?si=7034dd070e654b13`"

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
        reminders.append((time.strptime(" ".join(args[:2]), "%d-%m-%Y %H:%M:%S"), " ".join(args[2:]), ctx.channel.id))
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
