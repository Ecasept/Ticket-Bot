from src.utils import logger, create_embed, error_embed, error_to_embed, get_log_channel
from src.error import We
import discord
import re
from src.res import C, R


class RoleSelectView(discord.ui.View):
    """
    View for selecting roles to display in the team list.
    """

    def __init__(self):
        super().__init__(timeout=180)
        self.selected_roles: list[discord.Role] = []

    @discord.ui.role_select(
        placeholder=R.team_list_role_select_placeholder,
        min_values=1,
        max_values=25,
        custom_id="role_select_dropdown"
    )
    async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction) -> None:
        """
        Callback for role selection dropdown.
        Args:
            select (discord.ui.Select): The select component.
            interaction (discord.Interaction): The interaction context.
        """
        self.selected_roles = select.values
        # Acknowledge the interaction to prevent "Interaction failed"
        await interaction.response.defer()

    @discord.ui.button(
        label=R.team_list_submit_button_label,
        style=discord.ButtonStyle.primary,
        custom_id="submit_roles"
    )
    async def submit_callback(self, button, interaction: discord.Interaction) -> None:
        """
        Callback for submit button.
        Args:
            button: The button component.
            interaction (discord.Interaction): The interaction context.
        """
        if not self.selected_roles:
            await interaction.response.send_message(embed=create_embed(R.team_list_select_at_least_one_role, color=C.error_color), ephemeral=True)
            logger.error(We(R.team_list_select_at_least_one_role), interaction)
            return
        await interaction.response.defer()
        embed, view = TeamListMessage.create(self.selected_roles)
        await interaction.channel.send(embed=embed, view=view)
        await interaction.delete_original_response()

        logger.info(
            f"Showing team list for roles: {', '.join([r.name for r in self.selected_roles])}", interaction)


class TeamListMessage(discord.ui.View):
    """
    View for displaying and updating team lists showing members of selected roles.
    """

    @staticmethod
    def create(roles: list[discord.Role]) -> tuple[discord.Embed, discord.ui.View]:
        """
        Factory method to create team list embed and view.
        Args:
            roles (list[discord.Role]): List of roles to display.
        Returns:
            tuple[discord.Embed, discord.ui.View]: The embed and view.
        """
        embed = TeamListMessage.create_embed(roles)
        view = TeamListMessage()
        return embed, view

    @staticmethod
    def status_to_str(status: discord.Status) -> str:
        """
        Converts a discord.Status object to a string.
        Args:
            status (discord.Status): The status to convert.
        Returns:
            str: The string representation of the status.
        """
        if status == discord.Status.online:
            return R.status_online
        elif status == discord.Status.idle:
            return R.status_idle
        elif status == discord.Status.dnd:
            return R.status_dnd
        elif status == discord.Status.offline:
            return R.status_offline
        else:
            return R.status_unknown

    @staticmethod
    def create_embed(roles: list[discord.Role]) -> discord.Embed:
        """
        Create an embed showing team members for the given roles.
        Args:
            roles (list[discord.Role]): List of roles to display.
        Returns:
            discord.Embed: The formatted embed.
        """
        embed = discord.Embed(
            title=R.team_list_embed_title, color=C.embed_color)

        # Sort roles by position (highest first)
        sorted_roles = sorted(
            roles, key=lambda r: r.position, reverse=True)

        # Create a mapping of roles to members
        sorted_role_member_map: dict[discord.Role, list[discord.Member]] = {}
        for role in sorted_roles:
            sorted_role_member_map[role] = []
            for member in role.members:
                sorted_role_member_map[role].append(member)

        # Create embed
        for (role, members) in sorted_role_member_map.items():
            title = f"**{role.mention} ({len(members)})**"
            if len(members) > 0:
                text = []
                for member in members:
                    mention = member.mention
                    name = member.name
                    status = TeamListMessage.status_to_str(member.status)
                    if member.is_on_mobile():
                        status += R.status_mobile
                    msg = f"- {mention} {status} ({name})"
                    text.append(msg)
                text = "\n".join(text)
                embed.add_field(
                    name="",
                    value=f"{title}\n{text}",
                    inline=False
                )
            else:
                embed.add_field(
                    name="",
                    value=f"{title}\n{R.team_list_no_members_found}",
                    inline=False
                )

        return embed

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label=R.team_list_update_button_label,
        style=discord.ButtonStyle.secondary,
        custom_id="update_team_list",
        emoji=discord.PartialEmoji(name=R.team_list_upate_emoji))
    async def update(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Updates the team list message with the current members of the selected roles.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction that triggered the button click.
        """
        # Get the original message

        roles = []
        for field in interaction.message.embeds[0].fields:
            if field.name == "":
                # match the role id for all role mentions of the form <@&role_id>
                regex = re.compile(r"<@&(\d*)>")
                matches = regex.findall(field.value)
                for role_id in matches:
                    role = interaction.guild.get_role(int(role_id))
                    if role:
                        roles.append(role)
                    else:
                        logger.error(
                            We(f"Role with ID {role_id} not found in guild"), interaction)

        embed = TeamListMessage.create_embed(roles)
        await interaction.response.edit_message(embed=embed)
        logger.info(f"Team list updated", interaction)


def setup_team_list_command(bot: discord.Bot) -> None:
    """
    Setup team management commands for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """
    team = discord.SlashCommandGroup(
        "team",
        R.team_group_desc,
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @team.command(name="add", description=R.team_add_desc)
    @discord.default_permissions(administrator=True)
    @discord.option(
        "user",
        description=R.team_add_user_desc,
        type=discord.SlashCommandOptionType.user,
        required=True
    )
    @discord.option(
        "role",
        description=R.team_add_role_desc,
        type=discord.SlashCommandOptionType.role,
        required=True
    )
    async def team_add(ctx: discord.ApplicationContext, user: discord.Member, role: discord.Role):
        log_channel, err = await get_log_channel(ctx.interaction.guild)
        if err:
            await ctx.respond(embed=error_to_embed(err), ephemeral=True)
            logger.error(err, ctx.interaction)
            return

        try:
            # Add the role to the user
            await user.add_roles(role, reason=f"Added to team by {ctx.author.name}")
            # Send a message to the log channel
            log_message = R.team_add_success_log % (
                user.mention, ctx.author.mention, role.mention)
            await log_channel.send(embed=create_embed(log_message, title=R.new_team_member_title))
            # Send a confirmation message to the user
            await ctx.respond(embed=create_embed(log_message, color=C.success_color), ephemeral=True)
            logger.info(
                f"added role {role.name} to {user.name}", ctx.interaction)

        except discord.Forbidden:
            await ctx.respond(embed=error_embed(R.add_role_no_perm), ephemeral=True)
            logger.error(We(R.add_role_no_perm), ctx.interaction)
        except discord.HTTPException as e:
            await ctx.respond(embed=error_embed(R.error_occurred % e), ephemeral=True)
            raise e  # Re-raise the exception to log it

    @team.command(name="remove", description=R.team_remove_desc)
    @discord.default_permissions(administrator=True)
    @discord.option(
        "user",
        description=R.team_remove_user_desc,
        type=discord.SlashCommandOptionType.user,
        required=True
    )
    @discord.option(
        "role",
        description=R.team_remove_role_desc,
        type=discord.SlashCommandOptionType.role,
        required=True
    )
    async def team_remove(ctx: discord.ApplicationContext, user: discord.Member, role: discord.Role):
        log_channel, err = await get_log_channel(ctx.interaction.guild)
        if err:
            await ctx.respond(embed=error_to_embed(err), ephemeral=True)
            logger.error(err, ctx.interaction)
            return
        if role not in user.roles:
            await ctx.respond(embed=create_embed(R.team_remove_user_missing_role, color=C.error_color), ephemeral=True)
            logger.error(We(R.team_remove_user_missing_role), ctx.interaction)
            return
        try:
            await user.remove_roles(role, reason=f"Removed from team by {ctx.author.name}")
            log_message = R.team_remove_success_log % (
                user.mention, ctx.author.mention, role.mention)
            await log_channel.send(embed=create_embed(log_message, title=R.team_remove_success_title))
            await ctx.respond(embed=create_embed(log_message, color=C.success_color), ephemeral=True)
            logger.info(
                f"removed role {role.name} from {user.name}", ctx.interaction)
        except discord.Forbidden:
            await ctx.respond(embed=error_embed(R.add_role_no_perm), ephemeral=True)
            logger.error(We(R.add_role_no_perm), ctx.interaction)
        except discord.HTTPException as e:
            await ctx.respond(embed=error_embed(R.error_occurred % e), ephemeral=True)
            raise e  # Re-raise the exception to log it

    @team.command(name="wechsel", description=R.team_wechsel_desc)
    @discord.default_permissions(administrator=True)
    @discord.option(
        "user",
        description=R.team_wechsel_user_desc,
        type=discord.SlashCommandOptionType.user,
        required=True
    )
    @discord.option(
        "von",
        description=R.team_wechsel_from_role_desc,
        type=discord.SlashCommandOptionType.role,
        required=True
    )
    @discord.option(
        "zu",
        description=R.team_wechsel_to_role_desc,
        type=discord.SlashCommandOptionType.role,
        required=True
    )
    async def team_wechsel(ctx: discord.ApplicationContext, user: discord.Member, from_role: discord.Role, to_role: discord.Role):
        log_channel, err = await get_log_channel(ctx.interaction.guild)
        if err:
            await ctx.respond(embed=error_to_embed(err), ephemeral=True)
            logger.error(err, ctx.interaction)
            return
        if from_role not in user.roles:
            await ctx.respond(embed=create_embed(R.team_wechsel_user_missing_from_role, color=C.error_color), ephemeral=True)
            logger.error(
                We(R.team_wechsel_user_missing_from_role), ctx.interaction)
            return
        if to_role in user.roles:
            await ctx.respond(embed=create_embed(R.team_wechsel_user_already_has_to_role, color=C.error_color), ephemeral=True)
            logger.error(
                We(R.team_wechsel_user_already_has_to_role), ctx.interaction)
            return
        try:
            await user.remove_roles(from_role, reason=f"Role switch by {ctx.author.name}")
            await user.add_roles(to_role, reason=f"Role switch by {ctx.author.name}")
            log_message = R.team_wechsel_success_log % (
                user.mention, ctx.author.mention, from_role.mention, to_role.mention)
            await log_channel.send(embed=create_embed(log_message, title=R.team_wechsel_success_title))
            await ctx.respond(embed=create_embed(log_message, color=C.success_color), ephemeral=True)
            logger.info(
                f"switched role from {from_role.name} to {to_role.name} for {user.name}", ctx.interaction)
        except discord.Forbidden:
            await ctx.respond(embed=error_embed(R.add_role_no_perm), ephemeral=True)
            logger.error(We(R.add_role_no_perm), ctx.interaction)
        except discord.HTTPException as e:
            await ctx.respond(embed=error_embed(R.error_occurred % e), ephemeral=True)
            raise e

    @team.command(name="list", description=R.team_list_desc)
    @discord.default_permissions(administrator=True)
    async def team_list(ctx: discord.ApplicationContext) -> None:
        """
        Display a role selection interface for creating team lists.
        Args:
            ctx (discord.ApplicationContext): The command context.
        """
        view = RoleSelectView()
        await ctx.respond(embed=create_embed(R.team_list_select_roles_prompt), view=view, ephemeral=True)

    bot.add_application_command(team)
