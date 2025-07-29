"""
Category management commands for ticket categories.
Provides /category create, list, edit, and remove commands with button/selection based UI.
"""
import discord
from src.res import RD, RL
from .create import handle_create_category
from .edit import handle_edit_categories
from .remove import handle_remove_category


def setup_category_command(bot: discord.Bot):
    """
    Setup the category command group for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """
    category = discord.SlashCommandGroup(
        name=RD.command.category.name,
        name_localizations=RL.command.category.name,
        description=RD.command.category.desc,
        description_localizations=RL.command.category.desc,
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @category.command(
        name=RD.command.category.create.name,
        name_localizations=RL.command.category.create.name,
        description=RD.command.category.create.desc,
        description_localizations=RL.command.category.create.desc
    )
    @discord.default_permissions(administrator=True)
    async def category_create(ctx: discord.ApplicationContext):
        """
        Create a new ticket category with modal input.
        Args:
            ctx (discord.ApplicationContext): The command context.
        """
        # Use shared handler that includes modal creation
        await handle_create_category(ctx.interaction)

    @category.command(
        name=RD.command.category.edit.name,
        name_localizations=RL.command.category.edit.name,
        description=RD.command.category.edit.desc,
        description_localizations=RL.command.category.edit.desc
    )
    @discord.default_permissions(administrator=True)
    async def category_edit(ctx: discord.ApplicationContext):
        """
        Edit an existing ticket category.
        Args:
            ctx (discord.ApplicationContext): The command context.
        """
        # Use shared handler from category.py
        await handle_edit_categories(ctx.interaction)

    @category.command(
        name=RD.command.category.remove.name,
        name_localizations=RL.command.category.remove.name,
        description=RD.command.category.remove.desc,
        description_localizations=RL.command.category.remove.desc
    )
    @discord.default_permissions(administrator=True)
    async def category_remove(ctx: discord.ApplicationContext):
        """
        Remove a ticket category with confirmation.
        Args:
            ctx (discord.ApplicationContext): The command context.
        """
        # Use shared handler from remove.py
        await handle_remove_category(ctx.interaction)

    bot.add_application_command(category)
