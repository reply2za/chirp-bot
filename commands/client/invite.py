
from lib.MessageEventLocal import MessageEventLocal


async def execute(event: MessageEventLocal):
    await event.message.channel.send("Here is the invite link:\nhttps://discord.com/oauth2/authorize?client_id=1105250717721178112&permissions=8&scope=bot")