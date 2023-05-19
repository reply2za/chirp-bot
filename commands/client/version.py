

from lib.logger import logger
from lib.MessageEventLocal import MessageEventLocal

with open("pyproject.toml", "r") as f:
    version = None
    for line in f.readlines():
        if "version" in line:
            version = line.split("=")[1].strip().replace('"', "")
            break
    if version is None:
        logger.error("version not found in pyproject.toml")

async def execute(event: MessageEventLocal):
    # get the version number from the pyproject.toml file
    await event.message.channel.send(f"version: {version}")
