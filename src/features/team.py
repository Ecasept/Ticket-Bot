"""
Team management commands.
"""
from src.custom_bot import CustomBot
import re
import discord
import datetime
from src.res import role_select
from src.utils import handle_error, logger, create_embed, error_embed, error_to_embed, get_log_channel, parse_duration, get_team_welcome_channel
from src.error import Error, We
from src.database import db
from src.constants import C
from src.res import R, RD, RL, LateView, button, late
from discord.ext import tasks
from src.features.shared.list_display import ListDisplayView, create_list_embeds


class ApplicationBannedView(LateView):
    def __init__(self, user: discord.Member):
        super().__init__(timeout=None)
        self.user = user

    @late(lambda: button(
        label=R.team_sperre_unban,
        style=discord.ButtonStyle.danger,
        emoji=discord.PartialEmoji(name=R.team_sperre_unban_emoji)))
    async def unban(self, button: discord.ui.Button, interaction: discord.Interaction):
        """
        Unban the user from creating application tickets.
        Args:
            button (discord.ui.Button): The button that was clicked.
            interaction (discord.Interaction): The interaction context.
        """
        log_channel, err = await get_log_channel(interaction.guild)
        if err:
            await handle_error(interaction, err)
            return

        db.ab.unban_user(self.user.id, interaction.guild.id)
        await interaction.response.send_message(embed=create_embed(R.team_sperre_unban_success % self.user.mention, color=C.success_color), ephemeral=True)
        log_message = R.team_sperre_unban_log % (
            interaction.user.mention, self.user.mention)
        await log_channel.send(embed=create_embed(log_message, title=R.team_sperre_unban_log_title))

        logger.info(
            f"User {self.user.name} ({self.user.id}) unbanned from creating application tickets", interaction)


class RoleSelectView(LateView):
    """
    View for selecting roles to display in the team list.
    """

    def __init__(self):
        super().__init__(timeout=180)
        self.selected_roles: list[discord.Role] = []

    @late(lambda: role_select(
        placeholder=R.team_list_role_select_placeholder,
        min_values=1,
        max_values=25,
    ))
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

    @late(lambda: button(
        label=R.team_list_submit_button_label,
        style=discord.ButtonStyle.primary,
    ))
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
        embeds, view = TeamListMessage.create(self.selected_roles)
        if isinstance(embeds, Error):
            await handle_error(interaction, embeds)
            return

        await interaction.channel.send(
            embeds=embeds,
            view=view
        )
        await interaction.delete_original_response()

        logger.info(
            f"Showing team list for roles: {', '.join([r.name for r in self.selected_roles])}", interaction)


class TeamListMessage:
    """
    Helper class for creating team list messages.
    """

    @staticmethod
    def generate_text(roles: list[discord.Role]) -> list[tuple[str, str]]:
        """
        Generates the list of items for the team list embed.
        """
        # Sort roles by position (highest first)
        sorted_roles = sorted(
            roles, key=lambda r: r.position, reverse=True)

        # Create a mapping of roles to members
        sorted_role_member_map: dict[discord.Role, list[discord.Member]] = {}
        for role in sorted_roles:
            sorted_role_member_map[role] = sorted(
                role.members, key=lambda m: m.name)

        items = []
        for role, members in sorted_role_member_map.items():
            title = f"**{role.mention} ({len(members)})**"
            if members:
                text = []
                for member in members:
                    status = TeamListMessage.status_to_str(member.status)
                    if member.is_on_mobile():
                        status += R.status_mobile
                    text.append(f"- {member.mention} {status} ({member.name})")
                items.append((title, "\n".join(text)))
            else:
                items.append((title, R.team_list_no_members_found))
        return items

    @staticmethod
    def status_to_str(status: discord.Status) -> str:
        """
        Converts a discord.Status object to a string.
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
    async def update_team_list(interaction: discord.Interaction):
        """
        Updates the team list message.
        """
        if len(interaction.message.embeds[0].fields) > 0:
            await handle_error(interaction, We(R.team_list_old_version))
            return

        roles = []
        for embed in interaction.message.embeds:
            # match the role id for all role mentions of the form <@&role_id>
            regex = re.compile(r"<@&(\d+)>")
            matches = regex.findall(embed.description)
            for role_id in matches:
                role = interaction.guild.get_role(int(role_id))
                if role:
                    roles.append(role)
                else:
                    logger.error(
                        We(f"Role with ID {role_id} not found in guild"), interaction)

        items = TeamListMessage.generate_text(roles)
        embeds_or_err = create_list_embeds(
            R.team_list_embed_title, items, R.team_list_no_members_found)

        if isinstance(embeds_or_err, Error):
            await handle_error(interaction, embeds_or_err)
            return
        await interaction.response.edit_message(embeds=embeds_or_err)
        logger.info(f"Team list updated", interaction)

    @staticmethod
    def create(roles: list[discord.Role]) -> tuple[list[discord.Embed] | Error, discord.ui.View]:
        """
        Factory method to create team list embeds and view.
        """
        items = TeamListMessage.generate_text(roles)
        embeds_or_err = create_list_embeds(
            R.team_list_embed_title, items, R.team_list_no_members_found)

        if isinstance(embeds_or_err, Error):
            return embeds_or_err, None

        view = ListDisplayView(custom_id="update_team_list",
                               update_callback=TeamListMessage.update_team_list)
        return embeds_or_err, view


def setup_team_command(bot: CustomBot) -> None:
    """
    Setup team management commands for the bot.
    Args:
        bot (CustomBot): The Discord bot instance.
    """
    team = discord.SlashCommandGroup(
        name=RD.command.team.name,
        name_localizations=RL.command.team.name,
        description=RD.command.team.desc,
        description_localizations=RL.command.team.desc,
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @team.command(
        name=RD.command.team.add.name,
        name_localizations=RL.command.team.add.name,
        description=RD.command.team.add.desc,
        description_localizations=RL.command.team.add.desc
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        name=RD.command.team.add.option.user,
        name_localizations=RL.command.team.add.option.user,
        description=RD.command.team.add.option.user_desc,
        description_localizations=RL.command.team.add.option.user_desc,
        type=discord.SlashCommandOptionType.user,
        required=True
    )
    @discord.option(
        name=RD.command.team.add.option.role,
        name_localizations=RL.command.team.add.option.role,
        description=RD.command.team.add.option.role_desc,
        description_localizations=RL.command.team.add.option.role_desc,
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

            # Send a welcome message to the configured welcome channel
            welcome_channel, err = await get_team_welcome_channel(ctx.guild)
            if not err and welcome_channel:
                await welcome_channel.send(embed=create_embed(R.welcome_message % (user.mention, role.mention), title=R.new_team_member_title))
            logger.info(
                f"added role {role.name} to {user.name}", ctx.interaction)

        except discord.Forbidden:
            await ctx.respond(embed=error_embed(R.add_role_no_perm), ephemeral=True)
            logger.error(We(R.add_role_no_perm), ctx.interaction)
        except discord.HTTPException as e:
            await ctx.respond(embed=error_embed(R.error_occurred % e), ephemeral=True)
            raise e  # Re-raise the exception to log it

    @team.command(
        name=RD.command.team.remove.name,
        name_localizations=RL.command.team.remove.name,
        description=RD.command.team.remove.desc,
        description_localizations=RL.command.team.remove.desc
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        name=RD.command.team.remove.option.user,
        name_localizations=RL.command.team.remove.option.user,
        description=RD.command.team.remove.option.user_desc,
        description_localizations=RL.command.team.remove.option.user_desc,
        type=discord.SlashCommandOptionType.user,
        required=True
    )
    @discord.option(
        name=RD.command.team.remove.option.role,
        name_localizations=RL.command.team.remove.option.role,
        description=RD.command.team.remove.option.role_desc,
        description_localizations=RL.command.team.remove.option.role_desc,
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

    @team.command(
        name=RD.command.team.wechsel.name,
        name_localizations=RL.command.team.wechsel.name,
        description=RD.command.team.wechsel.desc,
        description_localizations=RL.command.team.wechsel.desc
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        name=RD.command.team.wechsel.option.user,
        name_localizations=RL.command.team.wechsel.option.user,
        description=RD.command.team.wechsel.option.user_desc,
        description_localizations=RL.command.team.wechsel.option.user_desc,
        type=discord.SlashCommandOptionType.user,
        required=True
    )
    @discord.option(
        name=RD.command.team.wechsel.option.from_role,
        name_localizations=RL.command.team.wechsel.option.from_role,
        description=RD.command.team.wechsel.option.from_role_desc,
        description_localizations=RL.command.team.wechsel.option.from_role_desc,
        type=discord.SlashCommandOptionType.role,
        required=True
    )
    @discord.option(
        name=RD.command.team.wechsel.option.to_role,
        name_localizations=RL.command.team.wechsel.option.to_role,
        description=RD.command.team.wechsel.option.to_role_desc,
        description_localizations=RL.command.team.wechsel.option.to_role_desc,
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

    @team.command(
        name=RD.command.team.list.name,
        name_localizations=RL.command.team.list.name,
        description=RD.command.team.list.desc,
        description_localizations=RL.command.team.list.desc
    )
    @discord.default_permissions(administrator=True)
    async def team_list(ctx: discord.ApplicationContext) -> None:
        """
        Display a role selection interface for creating team lists.
        Args:
            ctx (discord.ApplicationContext): The command context.
        """
        view = RoleSelectView.create(ctx.interaction)
        await ctx.respond(embed=create_embed(R.team_list_select_roles_prompt), view=view, ephemeral=True)

    @team.command(
        name=RD.command.team.sperre.name,
        name_localizations=RL.command.team.sperre.name,
        description=RD.command.team.sperre.desc,
        description_localizations=RL.command.team.sperre.desc
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        name=RD.command.team.sperre.option.user,
        name_localizations=RL.command.team.sperre.option.user,
        description=RD.command.team.sperre.option.user_desc,
        description_localizations=RL.command.team.sperre.option.user_desc,
        type=discord.SlashCommandOptionType.user,
        required=True
    )
    @discord.option(
        name=RD.command.team.sperre.option.duration,
        name_localizations=RL.command.team.sperre.option.duration,
        description=RD.command.team.sperre.option.duration_desc,
        description_localizations=RL.command.team.sperre.option.duration_desc,
        type=discord.SlashCommandOptionType.string,
        required=False,
        default=None
    )
    async def team_sperre(ctx: discord.ApplicationContext, user: discord.Member, duration: str = None):
        """
        Ban a user from creating application tickets.
        Args:
            ctx (discord.ApplicationContext): The command context.
            user (discord.Member): The user to ban from creating applications.
        """
        # Check if the user is already banned
        if db.ab.is_user_banned(user.id, ctx.guild.id):

            view = ApplicationBannedView.create(ctx.interaction, user)
            await ctx.respond(embed=create_embed(R.team_sperre_already_banned % user.mention, color=C.warning_color), view=view, ephemeral=True)
            logger.info(
                f"User {user.name} ({user.id}) is already banned from creating application tickets", ctx.interaction)

            return

        # If a duration is provided, validate it
        ends_at = None
        if duration:
            seconds, err = parse_duration(duration)
            if err:
                await handle_error(ctx.interaction, err)
                return
            ends_at = datetime.datetime.now(
                datetime.timezone.utc) + datetime.timedelta(seconds=seconds)

        log_channel, err = await get_log_channel(ctx.interaction.guild)
        if err:
            await handle_error(ctx.interaction, err)
            return

        # Ban the user
        db.ab.ban_user(user.id, ctx.guild.id, ends_at)

        if duration:
            str_duration = str(datetime.timedelta(seconds=seconds))
            log_message = R.team_sperre_success_log_duration % (
                user.mention, ctx.author.mention, str_duration)
        else:
            log_message = R.team_sperre_success_log % (
                user.mention, ctx.author.mention)
        await log_channel.send(embed=create_embed(log_message, title=R.team_sperre_success_title))
        await ctx.respond(embed=create_embed(log_message, color=C.success_color), ephemeral=True)

        logger.info(
            f"User {user.name} ({user.id}) banned from creating application tickets", ctx.interaction)

    @team.command(
        name=RD.command.team.welcome.name,
        name_localizations=RL.command.team.welcome.name,
        description=RD.command.team.welcome.desc,
        description_localizations=RL.command.team.welcome.desc
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        name=RD.command.team.welcome.option.channel,
        name_localizations=RL.command.team.welcome.option.channel,
        description=RD.command.team.welcome.option.channel_desc,
        description_localizations=RL.command.team.welcome.option.channel_desc,
        type=discord.SlashCommandOptionType.channel,
        required=False,
        default=None,
        channel_types=[discord.ChannelType.text]
    )
    async def team_welcome(ctx: discord.ApplicationContext, channel: discord.TextChannel = None):
        if channel:
            db.constant.set(C.DBKey.welcome_channel_id,
                            channel.id, ctx.guild.id)
            await ctx.respond(embed=create_embed(R.team_welcome_channel_set % channel.mention, color=C.success_color), ephemeral=True)
            logger.info(
                f"Welcome channel set to {channel.name} ({channel.id})", ctx.interaction)
        else:
            welcome_channel, err = await get_team_welcome_channel(ctx.guild)
            if err:
                await handle_error(ctx.interaction, err)
                return
            await ctx.respond(embed=create_embed(R.team_welcome_current_channel % welcome_channel.mention), ephemeral=True)

    @tasks.loop(seconds=C.application_ban_check_interval)
    async def check_application_bans():
        """
        Background task that checks for expired application bans and removes them.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        expired_bans = db.ab.get_expired(now)
        for (user_id, guild_id) in expired_bans:
            db.ab.unban_user(user_id, guild_id)
            logger.info(
                f"Automatically removed expired application ban for user {user_id} in guild {guild_id}")
    check_application_bans.start()

    bot.add_application_command(team)
