import discord
from utils import C, R, get_support_role
from database import db


class ModOptionsMessage(discord.ui.View):
    """
    A view that contains buttons for mod options.
    """
    view_id: str = "mod_options"

    def __init__(self, category: str, assigned_id: str,  assigned_to_self: bool, user_id: str):
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
        await interaction.response.defer(ephemeral=True)

        new_assigned_id = str(interaction.user.id)

        # Update ticket in database
        db.update_ticket_assignee(str(interaction.channel.id), new_assigned_id)

        # Edit channel permissions
        await interaction.channel.set_permissions(
            interaction.guild.get_member(int(new_assigned_id)),
            send_messages=True
        )
        support_role = get_support_role(interaction.guild)
        await interaction.channel.set_permissions(
            support_role,
            send_messages=False
        )
        # Edit mod options message
        new_msg, new_view = ModOptionsMessage.create(interaction)
        await interaction.edit(
            content=new_msg,
            view=new_view
        )

    async def unassign_ticket(self, interaction: discord.Interaction):
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
        await interaction.edit(
            content=new_msg,
            view=new_view
        )

    async def approve_application(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # Get the user who submitted the application
        user = interaction.guild.get_member(int(self.user_id))
        if user is None:
            await interaction.followup.send(
                content=R.user_not_found_msg,
                ephemeral=True
            )
            return

        # Add the user to the role
        support_role = get_support_role(interaction.guild)
        await user.add_roles(support_role)
        # Optionally, you can also send a message in the ticket channel
        await interaction.channel.send(
            content=R.application_approved_msg % user.mention,
        )

    async def reject_application(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        # Get the user who submitted the application
        user = interaction.guild.get_member(int(self.user_id))
        if user is None:
            await interaction.followup.send(
                content=R.user_not_found_msg,
                ephemeral=True
            )
            return

        # Optionally, you can also send a message in the ticket channel
        await interaction.channel.send(
            content=R.application_rejected_msg % user.mention,
        )

    @staticmethod
    def create(interaction: discord.Interaction) -> tuple[str, discord.ui.View]:
        """
        Create a mod options message and view.
        :param interaction: The interaction object from which the mod options message is created.
        :param category: The category of the ticket.
        :param assigned_id: The ID of the user to whom the ticket is assigned.
        :param parent_msg_id: The ID of the parent ticket options message.
        :param archived: Whether the ticket is archived or not.
        :return: A tuple containing the mod options message and view.
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
