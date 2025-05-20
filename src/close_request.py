import discord

from src.closed import close_ticket
from src.utils import C, R, error_embed, create_embed, get_member, is_mod_or_admin
from src.database import db
from src.utils import logger


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
        if not ticket:
            await interaction.response.send_message(
                embed=error_embed(R.ticket_not_found),
                ephemeral=True
            )
            logger.error("close_request",
                         f"Ticket {str(interaction.channel.id)} not found in the database when trying to accept close request.")
            return

        val, err = is_mod_or_admin(interaction.user)
        if err:
            await interaction.response.send_message(
                embed=error_embed(err),
                ephemeral=True
            )
            logger.error(
                "close_request", f"Error checking permissions for ticket {str(interaction.channel.id)}: {err}")
            return
        if not val:
            await interaction.response.send_message(
                embed=error_embed(
                    R.ticket_close_request_accept_no_permission),
                ephemeral=True
            )
            return

        # Edit the original message to remove buttons
        await interaction.message.edit(view=None)
        await close_ticket(interaction)

    @discord.ui.button(label=R.ticket_close_request_decline, style=discord.ButtonStyle.danger, custom_id="decline_close_request")
    async def decline(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Declines the ticket close request.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction that triggered the button click.
        """
        ticket = db.get_ticket(str(interaction.channel.id))
        if not ticket:
            await interaction.response.send_message(
                embed=error_embed(R.ticket_not_found),
                ephemeral=True
            )
            logger.error("close_request",
                         f"Ticket {str(interaction.channel.id)} not found in the database when trying to decline close request.")
            return

        # Updated permission check using is_mod_or_admin
        user_is_mod_admin, err = is_mod_or_admin(interaction.user)
        if err:
            await interaction.response.send_message(
                embed=error_embed(err),
                ephemeral=True
            )
            logger.error(
                "close_request", f"Error checking mod/admin permissions for decline ticket {str(interaction.channel.id)}: {err}")
            return

        if not user_is_mod_admin:
            await interaction.response.send_message(
                embed=error_embed(
                    R.ticket_close_request_decline_no_permission),
                ephemeral=True
            )
            logger.error(
                "close_request", f"User {interaction.user.name} (ID: {interaction.user.id}) is not a mod/admin.")
            return

        creator_id = ticket["user_id"]
        creator, err = get_member(interaction.guild, creator_id)
        if err:
            await interaction.response.send_message(
                embed=error_embed(err),
                ephemeral=True
            )
            logger.error(
                "close_request", f"Error getting ticket creator {creator_id}: {err}")
            return

        # Edit the original message to remove buttons
        await interaction.message.edit(view=None)
        await interaction.channel.send(
            embed=create_embed(R.ticket_close_request_declined_msg %
                               creator.mention, color=C.warning_color),
        )
