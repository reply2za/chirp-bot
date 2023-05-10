import discord

from lib.MessageEventLocal import MessageEventLocal

async def execute(event: MessageEventLocal):
    embed = discord.Embed(
        title="Help",
        description="Here is a list of all commands and their usage.",
        color=0x00FF00,
    )
    
    await event.message.channel.send(embed=embed)

