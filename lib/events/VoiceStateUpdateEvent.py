from lib.ServerManager import servers
from lib.events.AEvent import AEvent
import discord
from lib.ProcessManager import process_manager, bot
import time

# user-id_channel-id : last_joined timestamp
last_joined = {}
# ignore if the user joined again within n seconds
MIN_SECONDS = 15

class _VoiceStateUpdateEvent(AEvent):

    def __init__(self):
        super().__init__()
        @bot.event
        async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
            await self.execute([member, before, after])


    async def enabled_action(self, args: list):
        [member, before, after] = args
        if (process_manager.is_dev_mode() and member.id not in process_manager.get_config()[
            'owners']) or process_manager.is_active() is not True:
            return
        member_channel_id = f'{member.id}_{after.channel.id if after.channel is not None else before.channel.id}'
        # ignore if the user joined again within MIN_SECONDS seconds
        if member_channel_id in last_joined and (time.time() - last_joined.get(member_channel_id) < MIN_SECONDS):
            return
        if after.channel is not None and len(after.channel.members) < 2:
            tracked_channel = servers.get_server(str(member.guild.id)).tracked_voice_channels.get(str(after.channel.id))
            if tracked_channel is not None:
                last_joined[member_channel_id] = time.time()
                update_channel = await bot.fetch_channel(int(tracked_channel['txt_channel_id']))
                await update_channel.send(
                    f'{member.nick if member.nick is not None else member.name} has joined `{after.channel.name}`')


voice_state_update = _VoiceStateUpdateEvent()

