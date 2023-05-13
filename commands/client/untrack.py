from lib.MessageEventLocal import MessageEventLocal


async def execute(event: MessageEventLocal):
    if len(event.args) < 1:
        await event.message.channel.send(f"*provide a voice channel name to untrack `(example: {event.server.prefix}untrack general)`*")
        return
    # get all voice channels in the guild/server
    voice_channels = event.message.guild.voice_channels
    for voice_channel in voice_channels:
        if voice_channel.name.lower() == event.args[0].lower():
            was_successful = event.server.untrack_voice_channel(str(voice_channel.id))
            if was_successful:
                await event.message.channel.send(f"Untracked `{voice_channel.name}`")
            else:
                await event.message.channel.send(f"failed to untrack {voice_channel.name}")
            return
    await event.message.channel.send(f"could not find voice channel {event.args[0]}")

