from dotenv import load_dotenv
load_dotenv()
from lib.ProcessManager import process_manager, bot
import os
from lib.services.EventService import load_events
from lib.services.CommandService import commandService
from lib.ServerManager import servers
from lib.SheetDatabase import sheet_database

# Note: If you see the error below then that means that you are missing an async or await
# TypeError: object NoneType can't be used in 'await' expression

# load data
servers.deserialize_servers(sheet_database.get_data())

# load commands
commandService.load_commands(bot)

# load events
load_events()

if process_manager.is_dev_mode():
    bot.logger.info("Running in development mode")
else:
    bot.logger.info("Running in production mode")

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
