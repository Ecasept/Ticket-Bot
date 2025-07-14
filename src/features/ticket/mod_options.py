"""
Implements the ModOptionsMessage view for moderator actions on tickets, such as assigning, unassigning, approving, or rejecting applications.
"""
import discord

from .application_reject import reject_application
from .noch_fragen import create_noch_fragen
from src.utils import create_embed, error_to_embed, get_category_name, get_member, is_mod_or_admin, handle_error, mention
from src.database import db
from src.database.ticket import Ticket
from src.utils import logger, format_date
from src.res import C, R
from src.error import Ce, We


class ModOptionsMessage(discord.ui.View):
    """
    A Discord UI view that provides moderator options for ticket management, including assignment and application review.
    """

    def __init__(self, ticket: Ticket, interaction: discord.Interaction):
        super().__init__(timeout=None)

        self.assignee_id = ticket.assignee_id
        self.user_id = ticket.user_id
        self.category = get_category_name(ticket.category_id)

        if self.assignee_id is None:
            # No assignee
            assign_button = discord.ui.Button(
                label=R.assign_ticket, style=discord.ButtonStyle.primary,
                emoji=discord.PartialEmoji(name=R.assign_emoji))
            assign_button.callback = self.assign_ticket
            self.add_item(assign_button)
        elif self.assignee_id == str(interaction.user.id):
            # Assignee is the current user
            unassign_button = discord.ui.Button(
                label=R.unassign_ticket, style=discord.ButtonStyle.secondary,
                emoji=discord.PartialEmoji(name=R.unassign_emoji))
            unassign_button.callback = self.unassign_ticket
            self.add_item(unassign_button)
        else:
            # Assignee is someone else
            unassign_button = discord.ui.Button(
                label=R.unassign_ticket, style=discord.ButtonStyle.secondary,
                disabled=True, emoji=discord.PartialEmoji(name=R.unassign_emoji))
            self.add_item(unassign_button)

        if not ticket.archived and not ticket.close_at:
            noch_fragen_button = discord.ui.Button(
                label=R.noch_fragen_label, style=discord.ButtonStyle.secondary,
                emoji=discord.PartialEmoji(name=R.noch_fragen_emoji))
            noch_fragen_button.callback = self.noch_fragen
            self.add_item(noch_fragen_button)

        if False:
            approve_button = discord.ui.Button(
                row=1,
                label=R.approve_application, style=discord.ButtonStyle.success,
                emoji=discord.PartialEmoji(name=R.approve_application_emoji))
            approve_button.callback = self.approve_application
            self.add_item(approve_button)

            reject_button = discord.ui.Button(
                row=1,
                label=R.reject_application, style=discord.ButtonStyle.danger,
                emoji=discord.PartialEmoji(name=R.reject_application_emoji))
            reject_button.callback = self.reject_application
            self.add_item(reject_button)

    async def noch_fragen(self, interaction: discord.Interaction):
        """
        Create a "noch fragen" (any more questions) message for the ticket.
        Args:
            interaction (discord.Interaction): The interaction that triggered this action.
        """
        await interaction.response.defer()
        await create_noch_fragen(interaction)

    async def assign_ticket(self, interaction: discord.Interaction):
        """
        Assign the ticket to the current user.
        Args:
            interaction (discord.Interaction): The interaction that triggered the assignment.
        """
        await interaction.response.defer()

        new_assigned_id = str(interaction.user.id)

        # Update ticket in database
        db.ticket.update(str(interaction.channel.id),
                         assignee_id=new_assigned_id)

        # Send update message in the ticket channel
        await interaction.channel.send(
            embed=create_embed(R.ticket_assigned_msg %
                               interaction.user.mention, color=C.success_color),
        )

        # Edit mod options message
        embed, view = await ModOptionsMessage.create(interaction)
        await interaction.edit_original_response(
            embed=embed,
            view=view
        )

        logger.info("new assignee", interaction)

    async def unassign_ticket(self, interaction: discord.Interaction):
        """
        Unassign the ticket.
        Args:
            interaction (discord.Interaction): The interaction that triggered the unassignment.
        """
        await interaction.response.defer(ephemeral=True)

        # Update ticket in database
        db.ticket.update(str(interaction.channel.id), assignee_id=None)

        # Send update message in the ticket channel
        await interaction.channel.send(
            embed=create_embed(R.ticket_unassigned_msg),
        )

        # Edit mod options message
        new_embed, new_view = await ModOptionsMessage.create(interaction)
        await interaction.edit_original_response(
            embed=new_embed,
            view=new_view
        )

        logger.info("ticket unassigned", interaction)

    async def approve_application(self, interaction: discord.Interaction):
        """
        Approve a user's application and assign them the support role.
        Args:
            interaction (discord.Interaction): The interaction that triggered the approval.
        """

        # Get the user who submitted the application
        user, err = get_member(interaction.guild, self.user_id)
        if err:
            await handle_error(interaction, err)
            return

        # Send update message in the ticket channel
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send(
            embed=create_embed(R.application_approved_msg %
                               user.mention, color=C.success_color),
        )

        logger.info(
            f"Application approved for {user.name} (ID: {user.id})", interaction)

    async def reject_application(self, interaction: discord.Interaction):
        await reject_application(interaction, self.user_id)

    @staticmethod
    async def create(interaction: discord.Interaction) -> tuple[discord.Embed | None, discord.ui.View | None]:
        """
        Factory method to create the mod options message and view for a given interaction.
        Args:
            interaction (discord.Interaction): The interaction context.
        Returns:
            tuple[discord.Embed | None, discord.ui.View | None]: The message and view for the mod options.
        """

        ticket = db.ticket.get(str(interaction.channel.id))
        if ticket is None:
            err = Ce(R.ticket_not_found_msg)
            logger.error(err, interaction)
            return error_to_embed(err), None

        has_permission, err = is_mod_or_admin(interaction.user)
        if err:
            logger.error(err, interaction)
            return error_to_embed(err), None
        if not has_permission:
            err = We(R.mod_options_no_permission)
            logger.error(err, interaction)
            return error_to_embed(err), None

        assignee_id = ticket.assignee_id
        user_id = ticket.user_id
        archived = ticket.archived
        category = get_category_name(ticket.category_id)
        created_at = ticket.created_at

        if assignee_id is None:
            assignee_mention = R.mod_options_unassigned
        else:
            assignee_mention = mention(assignee_id)

        user_mention = mention(user_id)

        # Create the view
        view = ModOptionsMessage(ticket, interaction)

        # Create the embed
        embed = discord.Embed(
            title=R.mod_options_title,
            color=C.embed_color
        )
        # Add fields based on ticket category
        embed.add_field(
            name=R.mod_options_category,
            value=category,
            inline=True
        )
        embed.add_field(
            name=R.mod_options_user,
            value=user_mention,
            inline=True
        )
        embed.add_field(
            name=R.mod_options_assignee,
            value=assignee_mention,
            inline=True
        )
        embed.add_field(
            name=R.mod_options_created_at,
            value=format_date(created_at),
            inline=True
        )
        embed.add_field(
            name=R.mod_options_archived,
            value=R.mod_options_archived_yes if archived else R.mod_options_archived_no,
            inline=True
        )

        return embed, view
