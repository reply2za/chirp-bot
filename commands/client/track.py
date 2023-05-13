

from lib.MessageEventLocal import MessageEventLocal


async def execute(event: MessageEventLocal):
    if not event.message.guild:
        await event.message.channel.send("This command can only be used in a server")
        return
    if len(event.args) < 1:
        await event.message.channel.send(f"*provide a voice channel name to track `(example: {event.server.prefix}track general)`*")
        return
    # get all voice channels in the guild/server
    voice_channels = event.message.guild.voice_channels
    # iterate over voice channels to find the one that matches the name provided
    voice_channel_found = False
    tracked_voice_channels_str = ''
    for arg in event.args:
        for voice_channel in voice_channels:
            if voice_channel.name.lower() == arg.lower():
                if event.server.tracked_voice_channels.get(str(voice_channel.id)):
                    await event.message.channel.send(f"`{voice_channel.name}` is already being tracked")
                    break
                event.server.track_voice_channel(str(voice_channel.id), str(event.message.channel.id))
                await event.message.channel.send(f"tracking `{voice_channel.name}`")
                tracked_voice_channels_str += f"{voice_channel.name}, "
                voice_channel_found = True
                break
    if voice_channel_found:
        await event.message.channel.send(f'notifications will be sent to this channel for `{tracked_voice_channels_str[:-2]}`')
    else:
        await event.message.channel.send(f"*could not find a voice channel named `{arg}`*")