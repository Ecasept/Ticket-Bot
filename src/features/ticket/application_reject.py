import discord
from src.utils import get_member, handle_error, create_embed, logger
from src.res import R
from src.constants import C


class ApplicationRejectModal(discord.ui.Modal):
    """
    A modal for collecting the rejection reason when rejecting an application.
    """

    def __init__(self, user_id: str):
        super().__init__(title=R.reject_application_modal_title)
        self.user_id = user_id

        self.reason = discord.ui.InputText(
            label=R.reject_application_reason_label,
            placeholder=R.reject_application_reason_placeholder,
            required=False,
            style=discord.InputTextStyle.short
        )
        self.add_item(self.reason)

    async def callback(self, interaction: discord.Interaction):
        """
        Handle the modal submission and reject the application with the provided reason.
        Args:
            interaction (discord.Interaction): The interaction from the modal submission.
        """
        # Get the user who submitted the application
        user, err = get_member(interaction.guild, self.user_id)
        if err:
            await handle_error(interaction, err)
            return

        # Send update message in the ticket channel
        await interaction.response.defer(ephemeral=True)

        reason = self.reason.value
        if reason:
            rejection_message = R.application_rejected_with_reason_msg % (
                user.mention, reason)
        else:
            rejection_message = R.application_rejected_msg % user.mention

        await interaction.channel.send(
            embed=create_embed(rejection_message, color=C.error_color),
        )

        logger.info(
            f"Application rejected for {user.name} (ID: {user.id}) with reason: {self.reason.value}", interaction)


async def reject_application(interaction: discord.Interaction, user_id: str):
    """
    Show a modal to collect rejection reason and reject a user's application.
    Args:
        interaction (discord.Interaction): The interaction that triggered the rejection.
        user_id (str): The ID of the user whose application is being rejected.
    """
    modal = ApplicationRejectModal(user_id)
    await interaction.response.send_modal(modal)
