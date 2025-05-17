import discord

from src.closed import close_ticket
from src.utils import R, ensure_assignee
from src.utils import logger, error_embed
from src.database import db
from src.utils import get_support_role
from src.utils import ensure_existence


class TicketCloseRequestView(discord.ui.View):
    @staticmethod
    def create(interaction: discord.Interaction) -> tuple[str, discord.ui.View]:
        """
        Factory method to create the ticket close request message and view for a given interaction.
        Args:
            interaction (discord.Interaction): The interaction context.
        Returns:
            tuple[str, discord.ui.View]: The message and the view to display.
        """
        view = TicketCloseRequestView()
        msg = R.ticket_close_request_msg % interaction.user.mention
        return msg, view

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=R.ticket_close_request_accept, style=discord.ButtonStyle.success, custom_id="accept_close_request")
    async def accept(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Accepts the ticket close request.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction that triggered the button click.
        """
        ticket = db.get_ticket(str(interaction.channel.id))
        if not await ensure_existence(ticket, interaction):
            logger.error("header",
                         f"Ticket {str(interaction.channel.id)} not found in the database when trying to accept close request.")
            return

        assignee_id = ticket["assignee_id"]
        if not await ensure_assignee(assignee_id, interaction, R.ticket_close_request_accept_no_permission):
            logger.error("header",
                         f"User without permission tried to accept close request for ticket {str(interaction.channel.id)}.")
            return

        await close_ticket(interaction)
        await interaction.message.delete()

    @discord.ui.button(label=R.ticket_close_request_decline, style=discord.ButtonStyle.danger, custom_id="decline_close_request")
    async def decline(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Declines the ticket close request.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction that triggered the button click.
        """
        ticket = db.get_ticket(str(interaction.channel.id))
        if not await ensure_existence(ticket, interaction):
            logger.error("header",
                         f"Ticket {str(interaction.channel.id)} not found in the database when trying to decline close request.")
            return
        assignee_id = ticket["assignee_id"]
        if assignee_id != None and assignee_id != str(interaction.user.id):
            await interaction.response.send_message(
                embed=error_embed(
                    R.ticket_close_request_decline_no_permission),
                ephemeral=True
            )
            return
        if assignee_id == None and get_support_role(interaction.guild) not in interaction.user.roles:
            await interaction.response.send_message(
                embed=error_embed(
                    R.ticket_close_request_decline_no_permission),
                ephemeral=True
            )
            return

        await interaction.message.delete()
        await interaction.channel.send(
            content=R.ticket_close_request_declined_msg % interaction.user.mention,
        )
