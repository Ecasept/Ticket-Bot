"""
Implements the ModOptionsMessage view for moderator actions on tickets, such as assigning, unassigning, approving, or rejecting applications.
"""
import discord
from src.utils import C, R, get_support_role, create_embed, error_embed
from src.database import db
from src.utils import logger


class ModOptionsMessage(discord.ui.View):
    """
    A Discord UI view that provides moderator options for ticket management, including assignment and application review.
    """
    view_id: str = "mod_options"

    def __init__(self, category: str, assigned_id: str,  assigned_to_self: bool, user_id: str):
        """
        Initialize the ModOptionsMessage view.
        Args:
            category (str): The ticket category.
            assigned_id (str): The user ID of the assignee.
            assigned_to_self (bool): Whether the current user is the assignee.
            user_id (str): The user ID of the ticket creator.
        """
        super().__init__()

        self.category = category
        self.assignee_id = assigned_id
        self.assigned_to_self = assigned_to_self
        self.user_id = user_id

        if self.assignee_id is None:
            assign_button = discord.ui.Button(
                label=R.assign_ticket, style=discord.ButtonStyle.primary, custom_id="assign_ticket")
            assign_button.callback = self.assign_ticket
            self.add_item(assign_button)
        elif self.assigned_to_self:
            unassign_button = discord.ui.Button(
                label=R.unassign_ticket, style=discord.ButtonStyle.primary, custom_id="unassign_ticket")
            unassign_button.callback = self.unassign_ticket
            self.add_item(unassign_button)
        else:
            unassign_button = discord.ui.Button(
                label=R.unassign_ticket, style=discord.ButtonStyle.primary, custom_id="unassign_ticket",
                disabled=True)
            self.add_item(unassign_button)

        if category == C.cat_application and self.assigned_to_self:
            approve_button = discord.ui.Button(
                row=1,
                label=R.approve_application, style=discord.ButtonStyle.success, custom_id="approve_ticket")
            approve_button.callback = self.approve_application
            self.add_item(approve_button)

            reject_button = discord.ui.Button(
                row=1,
                label=R.reject_application, style=discord.ButtonStyle.danger, custom_id="reject_ticket")
            reject_button.callback = self.reject_application
            self.add_item(reject_button)

    async def assign_ticket(self, interaction: discord.Interaction):
        """
        Assign the ticket to the current user and update permissions and database.
        Args:
            interaction (discord.Interaction): The interaction that triggered the assignment.
        """
        await interaction.response.defer(ephemeral=True)

        new_assigned_id = str(interaction.user.id)

        # Update ticket in database
        db.update_ticket_assignee(str(interaction.channel.id), new_assigned_id)

        # Edit mod options message
        msg, view = ModOptionsMessage.create(interaction)
        await interaction.edit_original_response(
            embed=create_embed(msg),
            view=view
        )

        logger.info("mod_options",
                    f"Ticket {str(interaction.channel.id)} assigned to {interaction.user.name} (ID: {interaction.user.id})"
                    )

    async def unassign_ticket(self, interaction: discord.Interaction):
        """
        Unassign the ticket and update permissions and database.
        Args:
            interaction (discord.Interaction): The interaction that triggered the unassignment.
        """
        await interaction.response.defer(ephemeral=True)

        # Update ticket in database
        db.update_ticket_assignee(str(interaction.channel.id), None)

        # Edit channel permissions
        assignee_member = interaction.guild.get_member(int(self.assignee_id))
        await interaction.channel.set_permissions(
            assignee_member,
            send_messages=None
        )

        support_role = get_support_role(interaction.guild)
        await interaction.channel.set_permissions(
            support_role,
            send_messages=None
        )

        # Edit mod options message
        new_msg, new_view = ModOptionsMessage.create(interaction)
        await interaction.edit_original_response(
            embed=create_embed(new_msg),
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
        await interaction.response.defer(ephemeral=True)

        # Get the user who submitted the application
        user = interaction.guild.get_member(int(self.user_id))
        if user is None:
            await interaction.followup.send(
                embed=error_embed(R.user_not_found_msg),
                ephemeral=True
            )
            return

        # Add the user to the role
        support_role = get_support_role(interaction.guild)
        await user.add_roles(support_role)
        # Optionally, you can also send a message in the ticket channel
        await interaction.channel.send(
            embed=create_embed(R.application_approved_msg % user.mention, color=C.success_color),
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
        await interaction.response.defer(ephemeral=True)

        # Get the user who submitted the application
        user = interaction.guild.get_member(int(self.user_id))
        if user is None:
            await interaction.followup.send(
                embed=error_embed(R.user_not_found_msg),
                ephemeral=True
            )
            return

        # Optionally, you can also send a message in the ticket channel
        await interaction.channel.send(
            embed=create_embed(R.application_rejected_msg % user.mention, color=discord.Color.red()),
        )

        logger.info("mod_options",
                    f"Application rejected for {user.name} (ID: {user.id}) by {interaction.user.name} (ID: {interaction.user.id})"
                    )

    @staticmethod
    def create(interaction: discord.Interaction) -> tuple[str, discord.ui.View]:
        """
        Factory method to create the mod options message and view for a given interaction.
        Args:
            interaction (discord.Interaction): The interaction context.
        Returns:
            tuple[str, discord.ui.View]: The message and the view to display.
        """
        support_role = get_support_role(interaction.guild)
        if support_role not in interaction.user.roles:
            return R.mod_options_no_permission, None
        else:
            ticket = db.get_ticket(str(interaction.channel.id))
            if ticket is None:
                return R.ticket_not_found_msg, None
            assignee_id = ticket["assignee_id"]

            view = ModOptionsMessage(
                category=ticket["category"],
                assigned_id=assignee_id,
                assigned_to_self=interaction.user.id == int(
                    assignee_id) if assignee_id else False,
                user_id=str(interaction.user.id)
            )

            if assignee_id is None:
                mention = None
            else:
                try:
                    assignee = interaction.guild.get_member(
                        int(assignee_id))
                except ValueError:
                    assignee = None
                mention = assignee.mention if assignee else f"<@{assignee_id}>"

            assignee = interaction.guild.get_member(
                int(assignee_id)) if assignee_id else None
            msg = (R.mod_options_assigned_msg %
                   mention) if mention else R.mod_options_unassigned_msg
            return msg, view
