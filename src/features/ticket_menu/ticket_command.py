"""
Main ticket command that provides a menu interface.
"""
import discord
from src.res import R
from src.utils import logger
from src.features.ticket_menu.ticket_menu import send_ticket_menu


def setup_ticket_command(bot: discord.Bot):
    """
    Setup the main ticket command for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """

    @bot.slash_command(name="ticket", description=R.ticket_desc)
    @discord.default_permissions(administrator=True)
    async def ticket_command(interaction: discord.Interaction):
        """
        Open the ticket menu with various command options.
        Args:
            interaction (discord.Interaction): The interaction context.
        """
        await send_ticket_menu(interaction)
        logger.info("Ticket command executed", interaction)
