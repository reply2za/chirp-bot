import discord

from lib.ServerManager import Server


class MessageEventLocal:
        def __init__(self, bot, server: Server, message: discord.Message, statement: str, args: list):
            self.server = server
            self.message = message
            self.bot = bot
            self.statement = statement
            # the args are the words after the command
            self.args = args
            self.data = {}