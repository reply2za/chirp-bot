from lib.MessageEventLocal import MessageEventLocal
from lib.ProcessManager import process_manager
import os
from lib.utils import version


async def execute(event: MessageEventLocal):
    process_status_txt = f'{("active" if process_manager.is_active() else "inactive")}: {str(os.getpid())} (v{version})'
    message = await event.message.channel.send(process_status_txt)
    gear_emoji = "⚙️"
    await message.add_reaction(gear_emoji)
    def check(reaction, user):
        return str(reaction.emoji) == gear_emoji and user not in event.bot.config['owners']
    
    try:
        reaction, user = await event.bot.wait_for('reaction_add', timeout=60.0, check=check)
    except:
        return
    else:
        await event.message.channel.send(f'{user} reacted with {reaction}!')
        process_manager.set_active(not process_manager.is_active())
        await message.edit(content=str(os.getpid()) + ":" +  "active" if process_manager.is_active() else "inactive")
        await message.remove_reaction(reaction, user)

