from lib.MessageEventLocal import MessageEventLocal


async def execute(event: MessageEventLocal):
    if not event.message.guild:
        await event.message.channel.send("This command can only be used in a server")
        return
    if len(event.args) < 1:
        await event.message.channel.send(f"*provide a voice channel name to untrack `(example: {event.server.prefix}untrack general)`*")
        return
    for arg in event.args:
        voice_channels = event.message.guild.voice_channels
        was_successful = False
        for voice_channel in voice_channels:
            if voice_channel.name.lower() == arg.lower():
                was_successful = event.server.untrack_voice_channel(str(voice_channel.id))
                if was_successful:
                    await event.message.channel.send(f"Untracked `{voice_channel.name}`")
                    break
                else:
                    await event.message.channel.send(f"failed to untrack {voice_channel.name}")
                    break
        if not was_successful:
            await event.message.channel.send(f"*could not find `{arg}`*")

