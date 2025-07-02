import discord
from discord.ext import tasks
from .closed import ClosedView, close_channel, close_ticket
from database.database import db
from src.utils import create_embed, logger, handle_error
import datetime
from src.res import C, R
from src.error import Ce, We


class NochFragenMessage(discord.ui.View):
    """
    View for handling the "noch fragen" (any more questions) message.
    """

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

        if (ticket := db.get_ticket(interaction.channel.id)) is None:
            await handle_error(interaction, Ce(R.ticket_not_found))
            return
        if ticket.user_id != str(interaction.user.id):
            await handle_error(interaction, We(R.noch_fragen_no_permission))
            return
        if ticket.close_at is None:
            await handle_error(interaction, We(R.ticket_no_close_time))
            return

        await interaction.response.defer()
        await interaction.followup.send(
            embed=create_embed(R.noch_fragen_delete_msg, color=C.error_color),
            ephemeral=True
        )
        await close_ticket(interaction)
        await interaction.edit_original_response(view=None)
        logger.info("closed ticket after user confirmation", interaction)

    @discord.ui.button(label=R.no_questions_cancel, style=discord.ButtonStyle.primary, custom_id="noch_fragen_cancel", emoji=discord.PartialEmoji(name=R.noch_fragen_cancel_emoji))
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Button callback to handle the cancel button click.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction context.
        """
        if (ticket := db.get_ticket(interaction.channel.id)) is None:
            await handle_error(interaction, Ce(R.ticket_not_found))
            return
        if ticket.user_id != str(interaction.user.id):
            await handle_error(interaction, We(R.noch_fragen_no_permission))
            return
        if ticket.close_at is None:
            await handle_error(interaction, We(R.ticket_no_close_time))
            return

        await interaction.response.edit_message(view=None)

        # Tell the user that the ticket will not be closed
        await interaction.channel.send(
            embed=create_embed(R.noch_fragen_cancel_msg % interaction.user.mention, color=C.success_color))

        db.update_ticket(interaction.channel.id, close_at=None)
        logger.info("cancelled noch fragen after user request", interaction)


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
    await interaction.channel.send(
        embed=embed,
        view=view,
    )
    logger.info("noch fragen message sent", interaction)


def setup_noch_fragen(bot: discord.Bot):
    """
    Setup the automatic ticket closing task for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """
    @tasks.loop(minutes=5)
    async def delete_noch_fragen():
        """
        Background task that automatically closes overdue tickets.
        """
        now = datetime.datetime.now()
        overdue_ids = db.get_overdue_tickets(now)
        for id in overdue_ids:
            channel = bot.get_channel(int(id))
            if channel is None:
                logger.error(We(f"Channel {id} not found, skipping deletion."))
                continue  # Continue to next id if channel not found
            err = await close_channel(channel)
            if err:
                logger.error(err)
                continue  # Skip database update if closing channel failed

            # If close_channel was successful
            db.update_ticket(id, close_at=None, archived=True)
            embed, view = ClosedView.create(R.noch_fragen_closed_msg)
            await channel.send(
                embed=embed,
                view=view
            )
            logger.info(f"Closed channel {id} due to overdue noch fragen.")

    delete_noch_fragen.start()
