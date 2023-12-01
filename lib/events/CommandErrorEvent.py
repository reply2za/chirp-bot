import discord
from lib.ProcessManager import bot
from discord.ext.commands import Context
from lib.events.AEvent import AEvent
from discord.ext import commands

class _CommandErrorEvent(AEvent):

    def __init__(self):
        super().__init__()
        @bot.event
        async def on_command_error(context: Context, error) -> None:
            await self.execute([context, error])


    async def enabled_action(self, i: list):
            context = i[0]
            error = i[1]
            """
            The code in this event is executed every time a normal valid command catches an error.

            :param context: The context of the normal command that failed executing.
            :param error: The error that has been faced.
            """
            if isinstance(error, commands.CommandOnCooldown):
                minutes, seconds = divmod(error.retry_after, 60)
                hours, minutes = divmod(minutes, 60)
                hours = hours % 24
                embed = discord.Embed(
                    description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)
            elif isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    description="You are missing the permission(s) `"
                                + ", ".join(error.missing_permissions)
                                + "` to execute this command!",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)
            elif isinstance(error, commands.BotMissingPermissions):
                embed = discord.Embed(
                    description="I am missing the permission(s) `"
                                + ", ".join(error.missing_permissions)
                                + "` to fully perform this command!",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)
            elif isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    title="Error!",
                    # We need to capitalize because the command arguments have no capital letter in the code.
                    description=str(error).capitalize(),
                    color=0xE02B2B,
                )
                await context.send(embed=embed)
            elif isinstance(error, commands.CommandNotFound):
                pass
            else:
                raise error



command_error_event = _CommandErrorEvent()