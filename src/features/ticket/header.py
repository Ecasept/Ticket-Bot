"""
Implements the HeaderView for ticket channels, providing UI for closing tickets and accessing moderator options.
"""
import discord

from .close_request import TicketCloseRequestView
from .closed import close_ticket
from .mod_options import ModOptionsMessage
from src.utils import create_embed, is_mod_or_admin, logger, handle_error
from src.database import db
from src.res import R
from src.error import Ce, We


class HeaderView(discord.ui.View):
    """
    A Discord UI view that contains buttons for ticket options such as closing the ticket and opening moderator options.
    """

    def __init__(self):
        super().__init__(timeout=None)

        close_button = discord.ui.Button(
            label=R.close_ticket, style=discord.ButtonStyle.danger, custom_id="close_ticket",
            emoji=discord.PartialEmoji(name=R.close_emoji))
        close_button.callback = self.close_ticket
        self.add_item(close_button)

        mod_options = discord.ui.Button(
            label=R.mod_options_title, style=discord.ButtonStyle.secondary, custom_id="mod_options",
            emoji=discord.PartialEmoji(name=R.mod_options_emoji))
        mod_options.callback = self.open_mod_options
        self.add_item(mod_options)

    async def close_ticket(self, interaction: discord.Interaction):
        """
        Handles the closing of a ticket, moves the channel to the transcript category, and updates the database.
        Args:
            interaction (discord.Interaction): The interaction that triggered the close action.
        """
        cid = str(interaction.channel.id)
        ticket = db.ticket.get(cid)
        if not ticket:
            await handle_error(interaction, Ce(R.ticket_not_found))
            return

        if ticket.archived:
            await handle_error(interaction, We(R.ticket_already_closed))
            return

        is_mod_admin, err = is_mod_or_admin(interaction.user)
        if err:
            await handle_error(interaction, err)
            return

        if is_mod_admin:
            # If the user is a mod or admin, close the ticket directly
            await close_ticket(interaction)
        elif ticket.user_id == str(interaction.user.id):
            # If the user is the ticket owner, send a close request
            msg, view = TicketCloseRequestView.create(interaction)
            await interaction.response.send_message(
                embed=create_embed(msg, title=R.close_ticket_request_title),
                view=view,
            )
            logger.info("close request sent", interaction)
        else:
            # If the user is neither a mod nor the ticket owner, send an error message
            await handle_error(interaction, We(R.ticket_close_no_permission))

    async def open_mod_options(self, interaction: discord.Interaction):
        """
        Opens the moderator options for the ticket.
        Args:
            interaction (discord.Interaction): The interaction that triggered the mod options.
        """
        embed, view = await ModOptionsMessage.create(
            interaction,
        )

        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True
        )

        logger.info("mod options opened", interaction)
