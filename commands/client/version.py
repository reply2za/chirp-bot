

from lib.MessageEventLocal import MessageEventLocal


async def execute(event: MessageEventLocal):
    # get the version number from the pyproject.toml file
    with open("pyproject.toml", "r") as f:
        for line in f.readlines():
            if "version" in line:
                version = line.split("=")[1].strip().replace('"', "")
                break
    await event.message.channel.send(f"version: {version}")


