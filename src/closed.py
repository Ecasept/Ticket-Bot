import discord
from src.utils import get_member, get_ticket_category, get_transcript_category, logger, create_embed, handle_error, verify_mod_or_admin
from src.database import db
from src.res import C, R
from src.error import Ce, UserNotFoundError, We, Error


class ClosedView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    def create(message: str) -> tuple[discord.Embed, discord.ui.View]:
        """
        Factory method to create the closed ticket message and view.
        Args:
            message (str): The message to display in the closed ticket embed.
        Returns:
            tuple[discord.Embed, discord.ui.View]: The embed and the view to display.
        """
        view = ClosedView()
        embed = create_embed(message, color=C.error_color)
        return embed, view

    @discord.ui.button(label=R.delete_ticket_button, style=discord.ButtonStyle.secondary, custom_id="delete_ticket", emoji=discord.PartialEmoji(name=R.delete_emoji))
    async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Deletes the ticket channel.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction that triggered the button click.
        """
        # Check if the user has permission to delete the ticket

        if not await verify_mod_or_admin(interaction, We(R.ticket_delete_no_permission)):
            return

        await interaction.channel.delete()
        db.delete_ticket(str(interaction.channel.id))
        logger.info("ticket deleted", interaction)

    @discord.ui.button(label=R.reopen_ticket_button, style=discord.ButtonStyle.secondary, custom_id="reopen_ticket", emoji=discord.PartialEmoji(name=R.reopen_emoji))
    async def reopen(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Reopens the ticket.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction that triggered the button click.
        """
        # Move back to original category
        original_category, err = await get_ticket_category(interaction.guild)
        if err:
            await handle_error(interaction, err)
            return
        ticket = db.get_ticket(str(interaction.channel.id))
        if ticket is None:
            await handle_error(interaction, Ce(R.ticket_not_found))
            return
        user, err = get_member(interaction.guild, ticket.user_id)
        if err and err.iserr(UserNotFoundError):
            pass  # User not found, but don't block reopening the ticket
        elif err:
            await handle_error(interaction, err)
            return
        else:
            await interaction.channel.set_permissions(user, read_messages=True)

        await interaction.channel.edit(category=original_category)

        # Update database
        db.update_ticket(str(interaction.channel.id), archived=False)

        # Edit the original message to remove buttons
        await interaction.message.edit(view=None)
        # Send message
        await interaction.channel.send(
            embed=create_embed(R.ticket_reopened_msg %
                               interaction.user.mention, color=C.success_color),
        )
        logger.info("ticket reopened", interaction)


async def close_channel(channel: discord.TextChannel) -> Error | None:
    """
    Close a ticket channel by moving it to the transcript category and updating permissions.
    Args:
        channel (discord.TextChannel): The ticket channel to close.
    Returns:
        Error | None: An error if one occurred, None if successful.
    """
    # Change category
    category, err = await get_transcript_category(channel.guild)
    if err:
        return err
    await channel.edit(category=category)
    # Change permissions
    ticket = db.get_ticket(str(channel.id))
    if ticket is None:
        return Ce(R.ticket_not_found)
    user, err = get_member(channel.guild, ticket.user_id)
    if err and err.iserr(UserNotFoundError):
        pass  # User not found, but don't block closing the ticket
    elif err:
        return err
    else:
        await channel.set_permissions(user, read_messages=False)
    return None


async def close_ticket(interaction: discord.Interaction):
    """
    Closes the ticket by moving it to the transcript category, updating the database, and responding to the interaction.
    Does not check for permissions.
    Args:
        interaction (discord.Interaction): The interaction that triggered the close action.
    """
    if not interaction.response.is_done():
        await interaction.response.defer()

    # Change channel
    err = await close_channel(interaction.channel)
    if err:
        await handle_error(interaction, err)
        return

    # Update database
    db.update_ticket(str(interaction.channel.id), archived=True, close_at=None)

    msg = R.ticket_closed_msg % interaction.user.mention
    # Send message
    embed, view = ClosedView.create(msg)
    await interaction.channel.send(
        embed=embed,
        view=view
    )
    logger.info("ticket closed", interaction)
