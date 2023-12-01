from datetime import datetime

import discord
from discord import User
from lib.MessageEventLocal import MessageEventLocal
from lib.ProcessManager import process_manager
import os
from lib.utils import version


REACT_TIMEOUT = 30

last_message: discord.Message | None = None

async def execute(event: MessageEventLocal):
    global last_message
    message = await event.message.channel.send(get_process_status_txt())
    gear_emoji = "⚙️"
    await message.add_reaction(gear_emoji)
    if last_message:
        await last_message.clear_reactions()
    last_message = message

    def check(reaction, user: User):
        return str(reaction.emoji) == gear_emoji and user.id in event.bot.config['owners']
    date_time = datetime.now()
    async def check_react(reaction=None, user=None):
        elapsed_time = datetime.now().second - date_time.second
        if (elapsed_time > REACT_TIMEOUT):
            await message.clear_reactions()
            return
        try:
            reaction, user = await event.bot.wait_for('reaction_add', timeout=(REACT_TIMEOUT-elapsed_time), check=check)
        except:
            await message.clear_reactions()
            return
        else:
            await event.message.channel.send(f'{user} reacted with {reaction}!')
            process_manager.set_active(not process_manager.is_active())
            await message.edit(content=get_process_status_txt())
            await message.remove_reaction(reaction, user)
            await check_react(reaction, user)
    await check_react()


def get_process_status_txt():
    return f'{("active" if process_manager.is_active() else "inactive")}: {str(os.getpid())} (v{version})' + (' [dev]' if process_manager.is_dev_mode() else '')