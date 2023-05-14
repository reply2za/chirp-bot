
from lib.MessageEventLocal import MessageEventLocal
import subprocess

BASH_CMD = "git stash && git pull && pm2 restart chirp-bot"
async def execute(event: MessageEventLocal):
    await event.message.channel.send("updating...")
    print('running bash command: ', BASH_CMD)
    process = subprocess.Popen(BASH_CMD, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print('output: ', output)
    print('error: ', error)

