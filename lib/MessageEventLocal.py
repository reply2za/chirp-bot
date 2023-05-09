import discord


class MessageEventLocal:
        def __init__(self, bot, message: discord.Message, prefix: str, statement: str, args: list):
            self.prefix = prefix
            self.message = message
            self.bot = bot
            self.statement = statement
            # the args are the words after the command
            self.args = args
            self.data = {}