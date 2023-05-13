import discord

from lib.MessageEventLocal import MessageEventLocal

async def execute(event: MessageEventLocal):
    embed = discord.Embed(
        title="Commands",
        description=f"""
        `track [voice-channel]` - tracks a voice channel and sends a notification when the first person joins
        `untrack [voice-channel]` - untracks a voice channel
        """
        ,
        color=0x00FF00,
    )
    
    await event.message.channel.send(embed=embed)

