import json
from logging import Logger
import time
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

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

is_dev = os.getenv('DEV') == 'true'
intents = discord.Intents.all()

bot = Bot(
    command_prefix=commands.when_mentioned_or(config["prefix"]),
    intents=intents,
    help_command=None,
)
# add the config to the bot so it can be accessed from anywhere
bot.config = config
# initialize the logger
bot.logger: Logger = init_logger()

# load data
servers.deserialize_servers(sheet_database.get_data())

@bot.event
async def on_ready() -> None:
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='~help'))
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
    if is_dev:
        if message.author.id not in config['owners']:
            return
        elif message.content.startswith(config['dev_prefix']):
            message.content = message.content.replace(config['dev_prefix'], config['prefix'])
        else:
            return
    user_server = servers.get_server(str(message.guild.id))
    if user_server is None:
        bot.logger.info(f"creating server for {message.guild.id}")
        user_server = Server(message.guild.id, config["prefix"], {})
        servers.add_server(user_server)
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

# user-id_channel-id : last_joined timestamp
last_joined = {}
# ignore if the user joined again within n seconds
MIN_SECONDS = 10
@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if is_dev and member.id not in config['owners']:
        return
    member_channel_id = f'{member.id}_{after.channel.id if after.channel is not None else before.channel.id}'
    # ignore if the user joined again within 30 seconds
    if member_channel_id in last_joined and (time.time() - last_joined.get(member_channel_id) < MIN_SECONDS):
        return
    if after.channel is not None and len(after.channel.members) < 2:
        tracked_channel = servers.get_server(str(member.guild.id)).tracked_voice_channels.get(str(after.channel.id))
        if tracked_channel is not None:
            update_channel = await bot.fetch_channel(int(tracked_channel['txt_channel_id']))
            await update_channel.send(f'{member.nick if member.nick is not None else member.name} has joined {after.channel.name}')
            last_joined[member_channel_id] =  time.time()



commandService = CommandService(bot)
commandService.load_commands()

if is_dev:
    bot.logger.info("Running in development mode")

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
