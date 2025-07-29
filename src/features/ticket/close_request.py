import discord


from .closed import close_ticket
from src.utils import create_embed, get_member, handle_error, verify_mod_or_admin, logger
from src.database import db
from src.constants import C
from src.res import R
from src.error import Ce, We
from src.res.utils import LateView, late, button


class TicketCloseRequestView(LateView):
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

    @late(lambda: button(label=R.ticket_close_request_accept, style=discord.ButtonStyle.success, custom_id="accept_close_request"))
    async def accept(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Accepts the ticket close request.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction that triggered the button click.
        """

        if not await verify_mod_or_admin(interaction, We(R.ticket_close_request_accept_no_permission)):
            return

        # Edit the original message to remove buttons
        await interaction.message.edit(view=None)
        await close_ticket(interaction)
        logger.info(f"close request accepted", interaction)

    @late(lambda: button(label=R.ticket_close_request_decline, style=discord.ButtonStyle.danger, custom_id="decline_close_request"))
    async def decline(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Declines the ticket close request.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction that triggered the button click.
        """
        ticket = db.ticket.get(str(interaction.channel.id))
        if not ticket:
            await handle_error(interaction, Ce(R.ticket_not_found))
            return

        if not await verify_mod_or_admin(interaction, We(R.ticket_close_request_decline_no_permission)):
            return

        creator_id = ticket.user_id
        creator, err = get_member(interaction.guild, creator_id)
        if err:
            await handle_error(interaction, err)
            return

        # Edit the original message to remove buttons
        await interaction.message.edit(view=None)
        await interaction.channel.send(
            embed=create_embed(R.ticket_close_request_declined_msg %
                               creator.mention, color=C.warning_color),
        )
        logger.info(
            f"close request from {creator.name} (ID: {creator.id}) declined", interaction)