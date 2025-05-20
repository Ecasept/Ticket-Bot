"""
Implements the HeaderView for ticket channels, providing UI for closing tickets and accessing moderator options.
"""
import discord

from src.close_request import TicketCloseRequestView
from src.closed import close_ticket
from src.mod_options import ModOptionsMessage
from src.utils import R, ensure_existence, create_embed, is_mod
from src.database import db
from src.utils import logger, error_embed


class HeaderView(discord.ui.View):
    """
    A Discord UI view that contains buttons for ticket options such as closing the ticket and opening moderator options.
    """

    def __init__(self):
        super().__init__(timeout=None)

        close_button = discord.ui.Button(
            label=R.close_ticket, style=discord.ButtonStyle.danger, custom_id="close_ticket")
        close_button.callback = self.close_ticket
        self.add_item(close_button)

        mod_options = discord.ui.Button(
            label=R.mod_options_title, style=discord.ButtonStyle.secondary, custom_id="mod_options")
        mod_options.callback = self.open_mod_options
        self.add_item(mod_options)

    async def close_ticket(self, interaction: discord.Interaction):
        """
        Handles the closing of a ticket, moves the channel to the transcript category, and updates the database.
        Args:
            interaction (discord.Interaction): The interaction that triggered the close action.
        """
        cid = str(interaction.channel.id)
        ticket = db.get_ticket(cid)
        if not await ensure_existence(ticket, interaction):
            logger.error("header",
                         f"Ticket {cid} not found in the database when trying to close it.")
            return
        if ticket["archived"]:
            await interaction.response.send_message(
                embed=error_embed(R.ticket_already_closed),
                ephemeral=True
            )
            return

        if ticket["user_id"] == str(interaction.user.id):
            msg, view = TicketCloseRequestView.create(interaction)
            await interaction.response.send_message(
                embed=create_embed(msg, title=R.close_ticket_request_title),
                view=view,
            )
            logger.info("header",
                        f"Ticket close request sent for ticket {cid} by {interaction.user.name} (ID: {interaction.user.id})")

        elif is_mod(interaction):
            await close_ticket(interaction)
        else:
            await interaction.response.send_message(
                embed=error_embed(R.ticket_close_no_permission),
                ephemeral=True
            )

    async def open_mod_options(self, interaction: discord.Interaction):
        """
        Opens the moderator options for the ticket.
        Args:
            interaction (discord.Interaction): The interaction that triggered the mod options.
        """
        embed, view = ModOptionsMessage.create(
            interaction,
        )

        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True
        )

        logger.info("header",
                    f"Mod options opened for ticket {str(interaction.channel.id)} by {interaction.user.name} (ID: {interaction.user.id})")
