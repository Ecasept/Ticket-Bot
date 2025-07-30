"""
Main ticket command that provides a menu interface.
"""
import discord
from src.res import R, RD, RL
from src.utils import logger
from src.features.ticket_menu.ticket_menu import send_ticket_menu

from src.custom_bot import CustomBot


def setup_ticket_command(bot: CustomBot):
    """
    Setup the main ticket command for the bot.
    Args:
        bot (CustomBot): The Discord bot instance.
    """

    @bot.slash_command(
        name=RD.command.ticket.name,
        name_localizations=RL.command.ticket.name,
        description=RD.command.ticket.desc,
        description_localizations=RL.command.ticket.desc
    )
    @discord.default_permissions(administrator=True)
    async def ticket_command(interaction: discord.Interaction):
        """
        Open the ticket menu with various command options.
        Args:
            interaction (discord.Interaction): The interaction context.
        """
        await send_ticket_menu(interaction)
        logger.info("Ticket command executed", interaction)
