import importlib
import os

from lib.MessageEventLocal import MessageEventLocal

class CommandService:
    """
    This class handles the loading and execution of commands.
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.client_commands = {}
        self.admin_commands = {}
    
    def load_commands(self):
        """
        This function loads all commands from the commands directory.
        Each file name (.py) should match the name of the command.
        The commands directory supports one level of subdirectories, which allow for aliases.
        For subdirectories within the commands folder, the name of the subdirectory must be the name of the command, and the name of the file is the name of the alias.
        """
        self.load_specific_commands('./commands/client', self.client_commands)
        self.load_specific_commands('./commands/admin', self.admin_commands)
        
    def load_specific_commands(self, sub_directory, command_dict):
        #replace all slashes with dots
        module_prefix = sub_directory.replace('/', '.')[2:]
        try:
            os.listdir(sub_directory)
        except:
            self.bot.logger.error(f'Could not find directory {sub_directory}')
            return
        self.bot.logger.info(f'Loading commands from {sub_directory}')
        for filename in os.listdir(sub_directory):
            if os.path.isdir(f'{sub_directory}/{filename}'):
                # load subdirectories
                command_name = filename
                filename = f'{filename}.py'
                try:
                    module_name = f'{module_prefix}.{command_name}.{command_name}'
                    module = importlib.import_module(module_name)
                except:
                    self.bot.logger.warning(f'Skipping directory {command_name}')
                    continue
                has_command = False
                command_function = None
                for name, func in module.__dict__.items():
                    if callable(func) and name == 'execute':
                        has_command = True
                        command_function = func
                        command_dict[command_name] =  func
                if not has_command:
                    self.bot.logger.error(f'No command found for directory {command_name}')
                    continue
                for inner_filename in os.listdir(f'{sub_directory}/{command_name}'):
                    # within subdirectories, load aliases
                    if inner_filename.endswith('.py') and inner_filename != filename:
                        alias_name = inner_filename[:-3]
                        inner_module_name = f'{module_prefix}.{command_name}.{alias_name}'
                        module = importlib.import_module(inner_module_name)
                        command_dict[alias_name] =  command_function
            elif filename.endswith('.py'):
                # load root files
                module_name = f'{module_prefix}.{filename[:-3]}'
                module = importlib.import_module(module_name)
                for name, func in module.__dict__.items():
                    if callable(func) and name == 'execute':
                        command_dict[filename[:-3]] = func
            else:
                self.bot.logger.warning('Unexpected file {filename} in commands directory') 
    
    def get_command(self, event: MessageEventLocal):
        # if author is admin, return admin command
        # else return client command
        if event.statement in self.admin_commands and event.message.author.id in self.bot.config['owners']:
            return self.admin_commands[event.statement]
        else:
            return self.client_commands[event.statement]
    
    def __after_command_completion__(self, event: MessageEventLocal) -> None:
        """
        The code in this method is executed every time a normal command has been *successfully* executed.

        :param context: The context of the command that has been executed.
        """
        if event.message.guild is not None:
            self.bot.logger.info(
                f"Executed {event.statement} command in {event.message.guild.name} (ID: {event.message.guild.id}) by {event.message.author} (ID: {event.message.author.id})"
            )
        else:
            self.bot.logger.info(
                f"Executed {event.statement} command by {event.message.author} (ID: {event.message.author.id}) in DMs"
            )
    
    async def execute_command(self, event: MessageEventLocal):
        try: 
            command = self.get_command(event)
            if command is not None:
                res = await command(event)
                # self.__after_command_completion__(event)
                return res
        except Exception as e:
            if (not isinstance(e, KeyError)):
                self.bot.logger.error(f"Error while executing command {event.statement}: {e}")

        