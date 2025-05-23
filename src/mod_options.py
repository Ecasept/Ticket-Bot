"""
Implements the ModOptionsMessage view for moderator actions on tickets, such as assigning, unassigning, approving, or rejecting applications.
"""
import discord
from src.noch_fragen import create_noch_fragen
from src.utils import C, R, create_embed, error_embed, get_member, is_mod_or_admin
from src.database import Ticket, db
from src.utils import logger
from src.utils import format_date


class ModOptionsMessage(discord.ui.View):
    """
    A Discord UI view that provides moderator options for ticket management, including assignment and application review.
    """

    def __init__(self, ticket: Ticket, interaction: discord.Interaction):
        super().__init__()

        self.assignee_id = ticket.assignee_id
        self.user_id = ticket.user_id
        self.category = ticket.category

        if self.assignee_id is None:
            # No assignee
            assign_button = discord.ui.Button(
                label=R.assign_ticket, style=discord.ButtonStyle.primary, custom_id="assign_ticket",
                emoji=discord.PartialEmoji(name=R.assign_emoji))
            assign_button.callback = self.assign_ticket
            self.add_item(assign_button)
        elif self.assignee_id == str(interaction.user.id):
            # Assignee is the current user
            unassign_button = discord.ui.Button(
                label=R.unassign_ticket, style=discord.ButtonStyle.secondary, custom_id="unassign_ticket",
                emoji=discord.PartialEmoji(name=R.unassign_emoji))
            unassign_button.callback = self.unassign_ticket
            self.add_item(unassign_button)
        else:
            # Assignee is someone else
            unassign_button = discord.ui.Button(
                label=R.unassign_ticket, style=discord.ButtonStyle.secondary, custom_id="unassign_ticket",
                disabled=True, emoji=discord.PartialEmoji(name=R.unassign_emoji))
            self.add_item(unassign_button)

        if not ticket.archived and not ticket.close_at:
            noch_fragen_button = discord.ui.Button(
                label=R.noch_fragen_label, style=discord.ButtonStyle.secondary, custom_id="noch_fragen",
                emoji=discord.PartialEmoji(name=R.noch_fragen_emoji))
            noch_fragen_button.callback = self.noch_fragen
            self.add_item(noch_fragen_button)

        if self.category == C.cat_application:
            approve_button = discord.ui.Button(
                row=1,
                label=R.approve_application, style=discord.ButtonStyle.success, custom_id="approve_ticket",
                emoji=discord.PartialEmoji(name=R.approve_application_emoji))
            approve_button.callback = self.approve_application
            self.add_item(approve_button)

            reject_button = discord.ui.Button(
                row=1,
                label=R.reject_application, style=discord.ButtonStyle.danger, custom_id="reject_ticket",
                emoji=discord.PartialEmoji(name=R.reject_application_emoji))
            reject_button.callback = self.reject_application
            self.add_item(reject_button)

    async def noch_fragen(self, interaction: discord.Interaction):
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
        db.update_ticket(str(interaction.channel.id),
                         assignee_id=new_assigned_id)

        # Send update message in the ticket channel
        await interaction.channel.send(
            embed=create_embed(R.ticket_assigned_msg %
                               interaction.user.mention, color=C.success_color),
        )

        # Edit mod options message
        embed, view = ModOptionsMessage.create(interaction)
        await interaction.edit_original_response(
            embed=embed,
            view=view
        )

        logger.info("mod_options",
                    f"Ticket {str(interaction.channel.id)} assigned to {interaction.user.name} (ID: {interaction.user.id})"
                    )

    async def unassign_ticket(self, interaction: discord.Interaction):
        """
        Unassign the ticket.
        Args:
            interaction (discord.Interaction): The interaction that triggered the unassignment.
        """
        await interaction.response.defer(ephemeral=True)

        # Update ticket in database
        db.update_ticket(str(interaction.channel.id), assignee_id=None)

        # Send update message in the ticket channel
        await interaction.channel.send(
            embed=create_embed(R.ticket_unassigned_msg),
        )

        # Edit mod options message
        new_embed, new_view = ModOptionsMessage.create(interaction)
        await interaction.edit_original_response(
            embed=new_embed,
            view=new_view
        )

        logger.info("mod_options",
                    f"Ticket {str(interaction.channel.id)} unassigned by {interaction.user.name} (ID: {interaction.user.id})"
                    )

    async def approve_application(self, interaction: discord.Interaction):
        """
        Approve a user's application and assign them the support role.
        Args:
            interaction (discord.Interaction): The interaction that triggered the approval.
        """

        # Get the user who submitted the application
        user, err = get_member(interaction.guild, self.user_id)
        if err:
            await interaction.response.send_message(
                embed=error_embed(err),
                ephemeral=True
            )
            return

        # Send update message in the ticket channel
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send(
            embed=create_embed(R.application_approved_msg %
                               user.mention, color=C.success_color),
        )

        logger.info("mod_options",
                    f"Application approved for {user.name} (ID: {user.id}) by {interaction.user.name} (ID: {interaction.user.id})"
                    )

    async def reject_application(self, interaction: discord.Interaction):
        """
        Reject a user's application.
        Args:
            interaction (discord.Interaction): The interaction that triggered the rejection.
        """
        # Get the user who submitted the application
        user, err = get_member(interaction.guild, self.user_id)
        if err:
            await interaction.response.send_message(
                embed=error_embed(err),
                ephemeral=True
            )
            return

        # Send update message in the ticket channel
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.send(
            embed=create_embed(R.application_rejected_msg %
                               user.mention, color=C.error_color),
        )

        logger.info("mod_options",
                    f"Application rejected for {user.name} (ID: {user.id}) by {interaction.user.name} (ID: {interaction.user.id})"
                    )

    @staticmethod
    def create(interaction: discord.Interaction) -> tuple[discord.Embed, discord.ui.View]:
        """
        Factory method to create the mod options message and view for a given interaction.
        Args:
            interaction (discord.Interaction): The interaction context.
        Returns:
            tuple[discord.Embed, discord.ui.View]: The message and view for the mod options.
        """

        ticket = db.get_ticket(str(interaction.channel.id))
        if ticket is None:
            return error_embed(R.ticket_not_found_msg), None

        val, err = is_mod_or_admin(interaction.user)
        if err:
            # Error checking permissions
            return error_embed(err), None
        if not val:
            # User is not a mod or admin
            return error_embed(R.mod_options_no_permission), None

        assignee_id = ticket.assignee_id
        user_id = ticket.user_id
        archived = ticket.archived
        category = ticket.category
        created_at = ticket.created_at

        # Get assignee mention
        if assignee_id is None:
            # No assignee
            assignee_mention = None
        else:
            try:
                assignee = interaction.guild.get_member(
                    int(assignee_id))
            except ValueError:
                # Invalid assignee ID
                assignee = None
            assignee_mention = assignee.mention if assignee else f"<@{assignee_id}>"

        # Get user mention
        if user_id is None:
            # No user
            return error_embed(R.user_not_found_msg), None
        try:
            user = interaction.guild.get_member(int(user_id))
        except ValueError:
            # Invalid user ID
            user = None
        user_mention = user.mention if user else f"<@{user_id}>"

        # Create the view
        view = ModOptionsMessage(
            ticket=ticket,
            interaction=interaction,
        )

        # Create the embed message
        embed = discord.Embed(
            title=R.mod_options_title,
            color=C.embed_color
        )

        embed.add_field(
            name=R.mod_options_user,
            value=user_mention,
            inline=True
        )
        embed.add_field(
            name=R.mod_options_assignee,
            value=assignee_mention if assignee_mention else R.mod_options_unassigned,
            inline=True
        )
        match category:
            case C.cat_application:
                c = R.application
            case C.cat_report:
                c = R.report
            case C.cat_support:
                c = R.support
            case _:
                logger.error(
                    "mod_options", f"Unknown category {category} for ticket {str(interaction.channel.id)}")
                c = R.support
        embed.add_field(
            name=R.mod_options_category,
            value=c,
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
