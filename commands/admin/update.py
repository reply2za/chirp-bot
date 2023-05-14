
from lib.MessageEventLocal import MessageEventLocal
import subprocess

BASH_CMD = "git stash && git pull && pm2 restart chirp-bot"
async def execute(event: MessageEventLocal):
    await event.message.channel.send("updating...")
    process = subprocess.Popen(BASH_CMD.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print('output: ', output)
    print('error: ', error)

