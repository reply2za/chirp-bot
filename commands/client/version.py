

from lib.MessageEventLocal import MessageEventLocal


async def execute(event: MessageEventLocal):
    print("version")
    await event.message.channel.send("version: 1.0.1")


