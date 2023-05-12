import json
from dotenv import load_dotenv
load_dotenv()
import json
import os
import platform
import sys
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from lib.logger import init_logger
from lib.CommandService import CommandService
from lib.MessageEventLocal import MessageEventLocal
from lib.ServerManager import Server, servers
from lib.SheetDatabase import sheet_database



is_dev = os.getenv('DEV') == 'true'

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

intents = discord.Intents.all()

bot = Bot(
    command_prefix=commands.when_mentioned_or(config["prefix"]),
    intents=intents,
    help_command=None,
)
# add the config to the bot so it can be accessed from anywhere
bot.config = config
# initialize the logger
init_logger(bot)

# load data
servers.deserialize_servers(sheet_database.get_data())

@bot.event
async def on_ready() -> None:
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info("-------------------")

@bot.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix

    :param message: The message that was sent.
    """
    if is_dev and message.author.id not in config['owners']:
        return
    user_server = servers.get_server(str(message.guild.id))
    if user_server is None:
        print('creating server...')
        prefix = config["prefix"]
        user_server = Server(message.guild.id, config["prefix"], [])
        servers.add_server(user_server)
        print('setting data...')
        sheet_database.set_data(servers.serialize_servers())
    if not message.content.startswith(user_server.prefix):
        return
    args = message.content.split(" ")
    statement = args[0][len(user_server.prefix) :]
    args.pop(0)
    await commandService.execute_command(MessageEventLocal(bot, user_server, message, statement, args))


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error.

    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            description="You are missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to execute this command!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(
            description="I am missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to fully perform this command!",
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B,
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        raise error


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if is_dev:
        return
    if after.channel is not None and member.guild.id == 1102635525170544731 and len(after.channel.members) < 2:
        update_channel = await bot.fetch_channel('1105276246025318451')
        await update_channel.send(f'{member.name} has joined {after.channel.name}')


commandService = CommandService(bot)
commandService.load_commands()

if is_dev:
    bot.logger.info("Running in development mode")

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
