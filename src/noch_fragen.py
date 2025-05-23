import discord
from discord.ext import tasks
from src.closed import close_channel
from src.database import db
from src.utils import create_embed, error_embed, logger, R, C
import datetime


class NochFragenMessage(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    def create(interaction: discord.Interaction) -> tuple[discord.Embed, discord.ui.View]:
        """
        Factory method to create the noch fragen message and view for a given interaction.
        Args:
            interaction (discord.Interaction): The interaction context.
        Returns:
            tuple[discord.Embed, discord.ui.View]: The embed and the view to display.
        """
        view = NochFragenMessage()
        embed = create_embed(R.noch_fragen_msg % C.ticket_close_time,
                             color=C.success_color, title=R.noch_fragen_title)
        return embed, view

    @discord.ui.button(label=R.no_questions, style=discord.ButtonStyle.success, custom_id="noch_fragen_delete_ticket", emoji=discord.PartialEmoji(name=R.noch_fragen_delete_emoji))
    async def no_questions_left(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Button callback to handle the noch fragen button click.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction context.
        """

        ticket = db.get_ticket(interaction.channel.id)
        if ticket is None:
            await interaction.response.send_message(
                embed=error_embed(R.ticket_not_found),
                ephemeral=True
            )
            logger.error(
                "noch_fragen", f"Ticket {interaction.channel.id} not found in database.")
            return
        if ticket.user_id != str(interaction.user.id):
            await interaction.response.send_message(
                embed=error_embed(R.noch_fragen_no_permission),
                ephemeral=True
            )
            logger.error(
                "noch_fragen", f"User {interaction.user.id} does not have permission to close ticket {interaction.channel.id}.")
            return
        if ticket.close_at is None:
            await interaction.response.send_message(
                embed=error_embed(R.ticket_no_close_time),
                ephemeral=True
            )
            logger.error(
                "noch_fragen", f"Ticket {interaction.channel.id} has no close time.")
            return

        await interaction.channel.send(
            embed=create_embed(R.noch_fragen_delete_msg % interaction.user.mention, color=C.success_color))
        err = await close_channel(interaction.channel)
        if err:
            await interaction.response.send_message(
                embed=error_embed(err),
                ephemeral=True
            )
            logger.error(
                "noch_fragen", f"Error closing channel {interaction.channel.id}: {err}")
            return
        await interaction.response.edit_message(view=None)
        db.update_ticket(interaction.channel.id, close_at=None, archived=True)
        logger.info(
            "noch_fragen", f"Closed ticket {interaction.channel.id} after user confirmation.")

    @discord.ui.button(label=R.no_questions_cancel, style=discord.ButtonStyle.primary, custom_id="noch_fragen_cancel", emoji=discord.PartialEmoji(name=R.noch_fragen_cancel_emoji))
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Button callback to handle the cancel button click.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction context.
        """
        ticket = db.get_ticket(interaction.channel.id)
        if ticket is None:
            await interaction.response.send_message(
                embed=error_embed(R.ticket_not_found),
                ephemeral=True
            )
            logger.error(
                "noch_fragen", f"Ticket {interaction.channel.id} not found in database.")
            return
        if ticket.user_id != str(interaction.user.id):
            await interaction.response.send_message(
                embed=error_embed(R.noch_fragen_no_permission),
                ephemeral=True
            )
            logger.error(
                "noch_fragen", f"User {interaction.user.id} does not have permission to close ticket {interaction.channel.id}.")
            return
        if ticket.close_at is None:
            await interaction.response.send_message(
                embed=error_embed(R.ticket_no_close_time),
                ephemeral=True
            )
            logger.error(
                "noch_fragen", f"Ticket {interaction.channel.id} has no close time.")
            return

        await interaction.response.edit_message(view=None)

        # Tell the user that the ticket will not be closed
        await interaction.channel.send(
            embed=create_embed(R.noch_fragen_cancel_msg, color=C.success_color))

        db.update_ticket(interaction.channel.id, close_at=None)
        logger.info(
            "noch_fragen", f"Cancelled closing ticket {interaction.channel.id} after user confirmation.")


async def create_noch_fragen(interaction: discord.Interaction):
    """
    Creates the noch fragen message and view for a given interaction.
    Args:
        interaction (discord.Interaction): The interaction context.
    """
    embed, view = NochFragenMessage.create(interaction)
    now = datetime.datetime.now()
    close_time = now + datetime.timedelta(hours=C.ticket_close_time)
    db.update_ticket(interaction.channel.id, close_at=close_time)
    logger.info(
        "noch_fragen", f"Created noch fragen message for ticket {interaction.channel.id}.")
    await interaction.channel.send(
        embed=embed,
        view=view,
    )


def setup_noch_fragen(bot: discord.Bot):
    @tasks.loop(minutes=5)
    async def delete_noch_fragen():
        now = datetime.datetime.now()
        overdue_ids = db.get_overdue_tickets(now)
        for id in overdue_ids:
            channel = bot.get_channel(int(id))
            if channel is None:
                logger.error(
                    "noch_fragen", f"Channel {id} not found, skipping deletion.")
                continue  # Continue to next id if channel not found
            err = await close_channel(channel)
            if err:
                logger.error(
                    "noch_fragen", f"Error closing channel {id}: {err}")
                continue  # Skip database update if closing channel failed

            # If close_channel was successful
            db.update_ticket(id, close_at=None, archived=True)
            logger.info(
                "noch_fragen", f"Closed ticket {id} after timeout.")
    delete_noch_fragen.start()
