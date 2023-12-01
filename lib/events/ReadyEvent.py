from lib.events.AEvent import AEvent
import discord
from lib.ProcessManager import process_manager, bot
import platform
import os


config = process_manager.get_config()

class _ReadyEvent(AEvent):
    def __init__(self):
        super().__init__()
        @bot.event
        async def on_ready() -> None:
            await self.execute([None])


    async def enabled_action(self, args: list):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='~help'))
        bot.logger.info(f"discord.py API version: {discord.__version__}")
        bot.logger.info(f"Python version: {platform.python_version()}")
        bot.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        bot.logger.info(f"Logged in as {bot.user.name}")
        bot.logger.info(
            f"prefix is {config['prefix'] if process_manager.is_dev_mode() == False else config['dev_prefix']}")


ready_event = _ReadyEvent()