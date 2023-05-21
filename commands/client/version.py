
from lib.MessageEventLocal import MessageEventLocal
from lib.utils import version


async def execute(event: MessageEventLocal):
    # get the version number from the pyproject.toml file
    await event.message.channel.send(f"version: {version}")
