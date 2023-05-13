from lib.MessageEventLocal import MessageEventLocal
from lib.utils import trim_voice_channel_name


async def execute(event: MessageEventLocal):
    if not event.message.guild:
        await event.message.channel.send("This command can only be used in a server")
        return
    if len(event.args) < 1:
        await event.message.channel.send(f"*provide a voice channel name to untrack `(example: {event.server.prefix}untrack general)`*")
        return
    voice_channel_to_untrack = ''
    for arg in event.args:
        voice_channel_to_untrack += f"{arg} "
    voice_channels = event.message.guild.voice_channels
    was_successful = False
    for voice_channel in voice_channels:
        voice_channel_trimmed = trim_voice_channel_name(voice_channel.name)
        if voice_channel_trimmed.lower() == voice_channel_to_untrack.lower():
            was_successful = event.server.untrack_voice_channel(str(voice_channel.id))
            if was_successful:
                await event.message.channel.send(f"Untracked `{voice_channel_trimmed}`")
                return
            else:
                await event.message.channel.send(f"failed to untrack {voice_channel_trimmed}")
                return
    await event.message.channel.send(f"*could not find `{voice_channel_to_untrack}`*")

