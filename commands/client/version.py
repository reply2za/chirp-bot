

from lib.MessageEventLocal import MessageEventLocal


async def execute(event: MessageEventLocal):
    await event.message.channel.send("version: 1.0.4")


