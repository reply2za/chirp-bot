from dotenv import load_dotenv
import json
import os
import sys
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from lib.logger import logger
from logging import Logger

load_dotenv()
intents = discord.Intents.all()

if not os.path.isfile(f"{os.path.realpath(os.path.dirname('main.py'))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname('main.py'))}/config.json") as file:
        config = json.load(file)

bot = Bot(
    command_prefix=commands.when_mentioned_or(config["prefix"]),
    intents=intents,
    help_command=None,
)
# add the config to the bot, so it can be accessed from anywhere
bot.config = config
# initialize the logger
bot.logger: Logger = logger


class _ProcessManager:
    def __init__(self):
        self._is_dev = os.getenv('DEV') == 'true'
        self._is_active = False
        return

    def is_dev_mode(self):
        return self._is_dev

    def is_active(self):
        return self._is_active

    def set_active(self, is_active: bool):
        self._is_active = is_active
        return

    def set_dev_mode(self, is_dev: bool):
        self._is_dev = is_dev
        return

    def get_config(self):
        return config

    def is_owner(self, id: str) -> bool:
        return id in process_manager.get_config()['owners']


process_manager = _ProcessManager()