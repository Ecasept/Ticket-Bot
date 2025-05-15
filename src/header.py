"""
Implements the HeaderView for ticket channels, providing UI for closing tickets and accessing moderator options.
"""
import discord

from src.mod_options import ModOptionsMessage
from src.utils import R, get_transcript_category
from src.database import db
from src.utils import logger


class HeaderView(discord.ui.View):
    """
    A Discord UI view that contains buttons for ticket options such as closing the ticket and opening moderator options.
    """
    view_id: str = "ticket_options"

    def __init__(self):
        super().__init__(timeout=None)

        close_button = discord.ui.Button(
            label=R.close_ticket, style=discord.ButtonStyle.danger, custom_id="close_ticket")
        close_button.callback = self.close_ticket
        self.add_item(close_button)

        mod_options = discord.ui.Button(
            label=R.mod_options, style=discord.ButtonStyle.secondary, custom_id="mod_options")
        mod_options.callback = self.open_mod_options
        self.add_item(mod_options)

    async def close_ticket(self, interaction: discord.Interaction):
        """
        Handles the closing of a ticket, moves the channel to the transcript category, and updates the database.
        Args:
            interaction (discord.Interaction): The interaction that triggered the close action.
        """
        # Change category
        category = await get_transcript_category(interaction.guild)
        await interaction.channel.edit(category=category)

        db.delete_ticket(str(interaction.channel.id))

        await interaction.edit(
            content=R.ticket_closed_msg,
            view=None
        )
        logger.info("header",
                    f"Ticket {str(interaction.channel.id)} closed by {interaction.user.name} (ID: {interaction.user.id})")

    async def open_mod_options(self, interaction: discord.Interaction):
        """
        Opens the moderator options for the ticket.
        Args:
            interaction (discord.Interaction): The interaction that triggered the mod options.
        """
        msg, view = ModOptionsMessage.create(
            interaction,
        )

        await interaction.response.send_message(
            content=msg,
            view=view,
            ephemeral=True
        )

        logger.info("header",
                    f"Mod options opened for ticket {str(interaction.channel.id)} by {interaction.user.name} (ID: {interaction.user.id})")
