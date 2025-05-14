import discord
import dynamic
from utils import C, R, get_support_role


class ModOptionsMessage(dynamic.DynamicPersistentView):
    """
    A view that contains buttons for mod options.
    """
    view_id: str = "mod_options"

    def __init__(self, category: str, assigned_id: str, interaction_user_id: str, parent_msg_id: str, archived: str):
        super().__init__(self.view_id, category, assigned_id,
                         interaction_user_id, parent_msg_id, archived)
        self.category = category
        self.assigned_id = assigned_id
        self.interaction_user_id = interaction_user_id
        self.parent_msg_id = parent_msg_id
        self.assigned_to_self = assigned_id == interaction_user_id
        self.archived = archived

        print(f"Assigned ID: {self.assigned_id}")

        if self.assigned_id == "":
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
                label=R.approve_application, style=discord.ButtonStyle.success, custom_id="approve_ticket")
            approve_button.callback = self.approve_application
            self.add_item(approve_button)

            reject_button = discord.ui.Button(
                label=R.reject_application, style=discord.ButtonStyle.danger, custom_id="reject_ticket")
            reject_button.callback = self.reject_application
            self.add_item(reject_button)

    async def assign_ticket(self, interaction: discord.Interaction):
        from ticket import TicketOptionsMessage
        new_assigned_id = str(interaction.user.id)
        # Get ticket options message
        ticket_options_msg = await interaction.channel.fetch_message(self.parent_msg_id)
        # Get ticket options view
        new_msg = TicketOptionsMessage(
            self.category,
            new_assigned_id,
            self.archived
        )
        # Edit ticket options message
        await ticket_options_msg.edit(
            content=new_msg.msg,
            view=new_msg
        )
        # Edit mod options message
        new_msg, new_view = ModOptionsMessage.create(
            interaction,
            self.category,
            new_assigned_id,
            self.parent_msg_id,
            self.archived
        )
        await interaction.edit(
            content=new_msg,
            view=new_view
        )

    async def unassign_ticket(self, interaction: discord.Interaction):
        from ticket import TicketOptionsMessage
        # Get ticket options message
        ticket_options_msg = await interaction.channel.fetch_message(self.parent_msg_id)
        # Get ticket options view
        new_msg = TicketOptionsMessage(
            self.category,
            "",
            self.archived
        )
        # Edit ticket options message
        await ticket_options_msg.edit(
            content=new_msg.msg,
            view=new_msg
        )
        # Edit mod options message
        new_msg, new_view = ModOptionsMessage.create(
            interaction,
            self.category,
            "",
            self.parent_msg_id,
            self.archived
        )
        await interaction.edit(
            content=new_msg,
            view=new_view
        )

    async def approve_application(self, interaction: discord.Interaction):
        pass

    async def reject_application(self, interaction: discord.Interaction):
        pass

    @staticmethod
    def create(interaction: discord.Interaction, category: str, assigned_id: str, parent_msg_id: str, archived: str) -> tuple[str, discord.ui.View]:
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
            view = ModOptionsMessage(category, assigned_id,
                                     str(interaction.user.id), parent_msg_id, archived)
            assigned_user = interaction.guild.get_member(
                int(assigned_id)) if assigned_id else None
            msg = (R.mod_options_assigned_msg %
                   assigned_user.mention) if assigned_user else R.mod_options_unassigned_msg
            return msg, view
