import functools
import discord
from src.utils import logger
from src.res import R


class CustomBot(discord.Bot):
    def __init__(self, **options):
        super().__init__(**options)

    def slash_command(self, *cmd_args, **cmd_kwargs):
        parent_slash_command = super().slash_command

        def function_receiver(func):
            @functools.wraps(func)
            async def wrapper(ctx: discord.ApplicationContext, *args, **kwargs):
                """The same as the decorated function, but with additional initialization."""
                await R.init(ctx.guild_id)
                return await func(ctx, *args, **kwargs)
            return parent_slash_command(*cmd_args, **cmd_kwargs)(wrapper)
        return function_receiver


class CustomSlashCommandGroup(discord.SlashCommandGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def command(self, *cmd_args, **cmd_kwargs):
        parent_command = super().command

        def function_receiver(func):
            @functools.wraps(func)
            async def wrapper(ctx: discord.ApplicationContext, *args, **kwargs):
                """The same as the decorated function, but with additional initialization."""
                await R.init(ctx.guild_id)
                return await func(ctx, *args, **kwargs)
            return parent_command(*cmd_args, **cmd_kwargs)(wrapper)
        return function_receiver
