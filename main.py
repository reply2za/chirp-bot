from dotenv import load_dotenv
load_dotenv()
import json
import importlib
import os
import platform
import sys
from lib.MessageEventLocal import MessageEventLocal
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context
from lib.logger import init_logger



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

# initialize the logger
init_logger(bot)

"""
Create a bot variable to access the config file in cogs so that you don't need to import it every time.

The config is available using the following code:
- bot.config # In this file
- self.bot.config # In cogs
"""
bot.config = config


@bot.event
async def on_ready() -> None:
    bot.logger.info(f"discord.py API version: {discord.__version__}")
    bot.logger.info(f"Python version: {platform.python_version()}")
    bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    bot.logger.info(f"Logged in as {bot.user.name}")
    bot.logger.info("-------------------")


@bot.event
async def on_message(incomingMessage: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix

    :param message: The message that was sent.
    """
    prefix = config["prefix"]
    # determine if the message prefix matches the config prefix
    if not incomingMessage.content.startswith(prefix):
        return
    # split the message content into a list of words
    args = incomingMessage.content.split(" ")
    # remove the prefix from the first word
    statement = args[0][len(prefix) :]
    # remove the first word from the list of words
    args.pop(0)
    try: 
        command = commandService.get_command(statement)
        if command is not None:
            await command(MessageEventLocal(incomingMessage, incomingMessage, prefix, statement, args))
    except Exception as e:
        if (not isinstance(e, KeyError)):
            bot.logger.error(f"Error while executing command {statement}: {e}")


@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed.

    :param context: The context of the command that has been executed.
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    if context.guild is not None:
        bot.logger.info(
            f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
        )
    else:
        bot.logger.info(
            f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
        )


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

class CommandService:
    def __init__(self, bot):
        self.bot = bot
        self.commands = {}
    
    def load_commands(self):
        """
        This function loads all commands from the commands directory.
        Each file name (.py) should match the name of the command.
        The commands directory supports one level of subdirectories, which allow for aliases.
        For subdirectories within the commands folder, the name of the subdirectory must be the name of the command, and the name of the file is the name of the alias.
        """
        for filename in os.listdir('./commands'):
            bot.logger.info(f'Loading commands ')
            if os.path.isdir(f'./commands/{filename}'):
                # load subdirectories
                command_name = filename
                filename = f'{filename}.py'
                try:
                    module_name = f'commands.{command_name}.{command_name}'
                    module = importlib.import_module(module_name)
                except:
                    bot.logger.warning(f'Skipping directory {command_name}')
                    continue
                has_command = False
                command_function = None
                for name, func in module.__dict__.items():
                    if callable(func) and name == 'execute':
                        has_command = True
                        command_function = func
                        self.commands.setdefault(command_name, func)
                if not has_command:
                    bot.logger.error(f'No command found for directory {command_name}')
                    continue
                for inner_filename in os.listdir(f'./commands/{command_name}'):
                    # within subdirectories, load aliases
                    if inner_filename.endswith('.py') and inner_filename != filename:
                        alias_name = inner_filename[:-3]
                        inner_module_name = f'commands.{command_name}.{alias_name}'
                        module = importlib.import_module(inner_module_name)
                        self.commands.setdefault(alias_name, command_function)
            elif filename.endswith('.py'):
                # load root files
                module_name = f'commands.{filename[:-3]}'
                module = importlib.import_module(module_name)
                for name, func in module.__dict__.items():
                    if callable(func) and name == 'execute':
                        self.commands.setdefault(filename[:-3], func)
            else:
                bot.logger.warning('Unexpected file {filename} in commands directory') 
    def get_command(self, command_name):
        return self.commands[command_name]

commandService = CommandService(bot)
commandService.load_commands()
    




@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if after.channel != None and after.channel.guild.id == '1102635525170544731' and len(after.channel.members) < 2:
        update_channel = await bot.fetch_channel('1105276246025318451')
        await update_channel.send(f'{member.name} has joined {after.channel.name}')


bot.run(os.getenv('DISCORD_BOT_TOKEN'))