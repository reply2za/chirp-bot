

from lib.MessageEventLocal import MessageEventLocal
from lib.utils import trim_voice_channel_name


async def execute(event: MessageEventLocal):
    if not event.message.guild:
        await event.message.channel.send("This command can only be used in a server")
        return
    if len(event.args) < 1:
        await event.message.channel.send(f"*provide a voice channel name to track `(example: {event.server.prefix}track general)`*")
        return
    voice_channels = event.message.guild.voice_channels
    voice_channel_found = False
    tracked_voice_channels_str = ''
    # the voice channel name to look for and track
    vc_to_track = ''
    for arg in event.args:
        vc_to_track += f"{arg} "
    for voice_channel in voice_channels:
        voice_channel_trimmed = trim_voice_channel_name(voice_channel.name)
        if voice_channel_trimmed.lower() == vc_to_track.lower():
            if event.server.tracked_voice_channels.get(str(voice_channel.id)):
                await event.message.channel.send(f"`{voice_channel_trimmed}` is already being tracked")
                return
            event.server.track_voice_channel(str(voice_channel.id), str(event.message.channel.id))
            await event.message.channel.send(f"tracking `{voice_channel_trimmed}`")
            tracked_voice_channels_str += voice_channel_trimmed
            voice_channel_found = True
            break
    if voice_channel_found:
        await event.message.channel.send(f'notifications will be sent to this channel for `{tracked_voice_channels_str}`')
    else:
        await event.message.channel.send(f"*could not find a voice channel named `{vc_to_track}`*")