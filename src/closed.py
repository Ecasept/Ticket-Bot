import discord
from src.utils import C, R, ensure_assignee, ensure_existence, error_embed, get_ticket_category, get_transcript_category, logger, create_embed
from src.database import db


class ClosedView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    def create(interaction: discord.Interaction) -> tuple[str, discord.ui.View]:
        """
        Factory method to create the closed ticket message and view for a given interaction.
        Args:
            interaction (discord.Interaction): The interaction context.
        Returns:
            tuple[str, discord.ui.View]: The message and the view to display.
        """
        view = ClosedView()
        msg = R.ticket_closed_msg % interaction.user.mention
        return msg, view

    @discord.ui.button(label=R.delete_ticket_button, style=discord.ButtonStyle.danger, custom_id="delete_ticket")
    async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Deletes the ticket channel.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction that triggered the button click.
        """
        ticket = db.get_ticket(str(interaction.channel.id))
        if not await ensure_existence(ticket, interaction):
            logger.error("closed",
                         f"Ticket {str(interaction.channel.id)} not found in the database when trying to delete it.")
            return
        if not await ensure_assignee(ticket["assignee_id"], interaction, R.ticket_delete_no_permission):
            logger.error("closed",
                         f"User without permission tried to delete ticket {str(interaction.channel.id)}.")
            return

        await interaction.channel.delete()
        db.delete_ticket(str(interaction.channel.id))
        logger.info("closed",
                    f"Ticket {str(interaction.channel.id)} deleted by {interaction.user.name} (ID: {interaction.user.id})")

    @discord.ui.button(label=R.reopen_ticket_button, style=discord.ButtonStyle.success, custom_id="reopen_ticket")
    async def reopen(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Reopens the ticket.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction that triggered the button click.
        """
        ticket = db.get_ticket(str(interaction.channel.id))
        if not await ensure_existence(ticket, interaction):
            logger.error("closed",
                         f"Ticket {str(interaction.channel.id)} not found in the database when trying to reopen it.")
            return
        if not await ensure_assignee(ticket["assignee_id"], interaction, R.ticket_reopen_no_permission):
            logger.error("closed",
                         f"User without permission tried to reopen ticket {str(interaction.channel.id)}.")
            return

        # Move back to original category
        original_category = await get_ticket_category(interaction)
        await interaction.channel.edit(category=original_category)

        # Update database
        db.update_ticket_archived(str(interaction.channel.id), False)

        # Get user
        user = interaction.guild.get_member(int(ticket["user_id"]))
        if user is None:
            await interaction.response.send_message(embed=error_embed(R.user_not_found_msg), ephemeral=True)
            logger.error(
                "closed", f"User with ID {ticket['user_id']} not found when reopening ticket {interaction.channel.id}")
            return

        # Edit the original message to remove buttons
        await interaction.message.edit(view=None)
        # Send message
        await interaction.channel.send(
            embed=create_embed(R.ticket_reopened_msg %
                               user.mention, color=C.success_color),
        )

        logger.info("closed",
                    f"Ticket {str(interaction.channel.id)} reopened by {interaction.user.name} (ID: {interaction.user.id})")


async def close_ticket(interaction: discord.Interaction):
    """
    Closes the ticket by moving it to the transcript category, updating the database, and responding to the interaction.
    Does not check for permissions.
    Args:
        interaction (discord.Interaction): The interaction that triggered the close action.
    """
    await interaction.response.defer()
    # Change category
    category = await get_transcript_category(interaction)
    await interaction.channel.edit(category=category)

    # Update database
    db.update_ticket_archived(str(interaction.channel.id), True)

    # Send message
    msg, view = ClosedView.create(interaction)
    await interaction.channel.send(
        embed=create_embed(msg),
        view=view
    )
    logger.info("closed",
                f"Ticket {str(interaction.channel.id)} closed by {interaction.user.name} (ID: {interaction.user.id})")
