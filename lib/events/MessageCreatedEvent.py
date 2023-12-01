import discord

from lib.MessageEventLocal import MessageEventLocal
from lib.ProcessManager import process_manager, bot
from lib.ServerManager import Server, servers
from lib.events.AEvent import AEvent
from lib.services.CommandService import commandService


class _MessageCreatedEvent(AEvent):

    def __init__(self):
        super().__init__()
        @bot.event
        async def on_message(message: discord.Message) -> None:
            await self.execute([message])


    async def enabled_action(self, args: list):
        message = args[0]
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if not process_manager.is_active():
            if not process_manager.is_owner(message.author.id):
                return
        if process_manager.is_dev_mode():
            if message.author.id not in process_manager.get_config()['owners']:
                return
            elif message.content.startswith(process_manager.get_config()['dev_prefix']):
                message.content = message.content.replace(process_manager.get_config()['dev_prefix'], process_manager.get_config()['prefix'])
            else:
                return
        user_server = servers.get_server(str(message.guild.id))
        if user_server is None:
            bot.logger.info(f"creating server for {message.guild.id}")
            user_server = Server(message.guild.id, process_manager.get_config()["prefix"], {})
            servers.add_server(user_server)
        if not message.content.startswith(user_server.prefix):
            return
        args = message.content.split(" ")
        statement = args[0][len(user_server.prefix) :]
        args.pop(0)
        if not process_manager.is_active():
            if not process_manager.is_owner(message.author.id):
                return
            if statement != "boot":
                return
        await commandService.execute_command(MessageEventLocal(bot, user_server, message, statement, args))



message_created_event = _MessageCreatedEvent()

