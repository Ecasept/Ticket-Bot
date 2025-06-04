import discord

from src.utils import error_embed, create_embed, handle_error
from src.error import We
from src.database import db
from src.utils import logger
from src.res import C, R


def setup_setup_command(bot: discord.Bot):
    """
    Setup the setup command for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """
    setup = discord.SlashCommandGroup(
        "setup",
        R.setup_subcommand_desc,
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @setup.command(name="tickets", description=R.setup_tickets_desc)
    @discord.default_permissions(administrator=True)
    @discord.option(
        "category",
        required=False,
        default=None,
        type=discord.SlashCommandOptionType.channel,
        channel_types=[discord.ChannelType.category]
    )
    async def setup_tickets(ctx: discord.ApplicationContext, category: discord.CategoryChannel = None):
        """
        Set the ticket category for the bot.
        If no category is provided, it will show the current category.
        Args:
            ctx (discord.ApplicationContext): The context of the command.
            category (discord.CategoryChannel, optional): The category to set for tickets. Defaults to None.
        """

        if category is None:
            # Tell the user the current category
            cat = db.get_constant(C.ticket_category, ctx.guild.id)
            if cat is None:
                # No category set
                await ctx.respond(embed=create_embed(R.setup_no_ticket_category, color=C.warning_color), ephemeral=True)
                logger.error(We(R.setup_no_ticket_category), ctx.interaction)
                return
            cat = ctx.guild.get_channel(int(cat))
            if cat is None:
                # Category not found
                await ctx.respond(embed=error_embed(R.setup_ticket_category_not_found), ephemeral=True)
                logger.error(
                    We(R.setup_ticket_category_not_found), ctx.interaction)
                return
            await ctx.respond(
                embed=create_embed(R.setup_tickets_current_category %
                                   cat.mention, title=R.setup_title),
                ephemeral=True
            )
            logger.info(f"Told user current ticket category: {cat.name} (ID: {cat.id})",
                        ctx.interaction)
            return
        # Set the category in the database
        db.set_constant(C.ticket_category, str(category.id), ctx.guild.id)
        await ctx.respond(
            embed=create_embed(R.setup_tickets_set_category %
                               category.mention, color=C.success_color, title=R.setup_title),
            ephemeral=True
        )
        logger.info(
            f"Ticket category set to {category.name} (ID: {category.id})",
            ctx.interaction)

    @setup.command(name="transcript", description=R.setup_transcript_desc)
    @discord.default_permissions(administrator=True)
    @discord.option(
        "category",
        required=False,
        default=None,
        type=discord.SlashCommandOptionType.channel,
        channel_types=[discord.ChannelType.category]
    )
    async def setup_transcript(ctx: discord.ApplicationContext, category: discord.CategoryChannel = None):
        """
        Set the transcript category for the bot.
        If no category is provided, it will show the current category.
        Args:
            ctx (discord.ApplicationContext): The context of the command.
            category (discord.CategoryChannel, optional): The category to set for transcripts. Defaults to None.
        """

        if category is None:
            # Tell the user the current category
            cat = db.get_constant(C.transcript_category, ctx.guild.id)
            if cat is None:
                # No category set
                await ctx.respond(embed=create_embed(R.setup_no_transcript_category, color=C.warning_color), ephemeral=True)
                logger.error(We(R.setup_no_transcript_category),
                             ctx.interaction)
                return
            # Get the category channel
            cat = ctx.guild.get_channel(int(cat))
            if cat is None:
                # Category not found
                await ctx.respond(embed=error_embed(R.setup_transcript_category_not_found), ephemeral=True)
                logger.error(
                    We(R.setup_transcript_category_not_found), ctx.interaction)
                return
            await ctx.respond(
                embed=create_embed(
                    R.setup_transcript_current_category % cat.mention),
                ephemeral=True
            )
            logger.info(f"Told user current transcript category: {cat.name} (ID: {cat.id})",
                        ctx.interaction)
            return
        # Set the category in the database
        db.set_constant(C.transcript_category, str(category.id), ctx.guild.id)
        await ctx.respond(
            embed=create_embed(R.setup_transcript_set_category %
                               category.mention, color=C.success_color),
            ephemeral=True
        )
        logger.info(
            f"Transcript category set to {category.name} (ID: {category.id})",
            ctx.interaction)

    @setup.command(name="logchannel", description=R.setup_logchannel_desc)
    @discord.default_permissions(administrator=True)
    @discord.option(
        "channel",
        description=R.setup_logchannel_desc,
        required=False,
        default=None,
        type=discord.SlashCommandOptionType.channel,
        channel_types=[discord.ChannelType.text]
    )
    async def setup_logchannel(ctx: discord.ApplicationContext, channel: discord.TextChannel = None):
        """
        Set the log channel for team-related actions.
        If no channel is provided, it will show the current log channel.
        Args:
            ctx (discord.ApplicationContext): The context of the command.
            channel (discord.TextChannel, optional): The text channel to set for logs. Defaults to None.
        """
        if channel is None:
            # Tell the user the current log channel
            log_channel_id = db.get_constant(C.log_channel, ctx.guild.id)
            if log_channel_id is None:
                await ctx.respond(embed=create_embed(R.setup_no_logchannel, color=C.warning_color, title=R.log_channel_title), ephemeral=True)
                logger.error(We(R.setup_no_logchannel), ctx.interaction)
                return
            log_ch = ctx.guild.get_channel(int(log_channel_id))
            if log_ch is None:
                await ctx.respond(embed=error_embed(R.setup_logchannel_not_found, title=R.log_channel_title), ephemeral=True)
                logger.error(
                    We(R.setup_logchannel_not_found), ctx.interaction)
                return
            await ctx.respond(
                embed=create_embed(R.setup_logchannel_current %
                                   log_ch.mention, title=R.log_channel_title),
                ephemeral=True
            )
            logger.info(f"Told user current log channel: {log_ch.name} (ID: {log_ch.id})",
                        ctx.interaction)
            return

        # Set the log channel in the database
        db.set_constant(C.log_channel, str(channel.id), ctx.guild.id)
        await ctx.respond(
            embed=create_embed(R.setup_logchannel_set % channel.mention,
                               color=C.success_color, title=R.log_channel_title),
            ephemeral=True
        )
        logger.info(
            f"Log channel set to {channel.name} (ID: {channel.id})",
            ctx.interaction)

    @setup.command(name="modroles", description=R.setup_modroles_desc)
    @discord.default_permissions(administrator=True)
    async def setup_modroles(ctx: discord.ApplicationContext):
        """
        Show a dialog to select multiple moderator roles for the bot.
        Args:
            ctx (discord.ApplicationContext): The command context.
        """
        class ModRolesSelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=120)
                self.selected_roles = []

            @discord.ui.role_select(
                placeholder=R.setup_modroles_select_placeholder,
                min_values=1,
                max_values=25,
            )
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                self.selected_roles = select.values
                await interaction.response.defer()

            @discord.ui.button(
                label=R.modroles_submit_button_label,
                style=discord.ButtonStyle.primary,
            )
            async def submit_callback(self, button, interaction: discord.Interaction):
                if not self.selected_roles:
                    await interaction.response.send_message(embed=create_embed(R.setup_modroles_none_selected, color=C.error_color), ephemeral=True)
                    logger.error(
                        We(R.setup_modroles_none_selected), ctx.interaction)
                    return
                # Save selected roles as comma-separated IDs
                role_ids = [str(role.id) for role in self.selected_roles]
                db.set_constant(C.mod_roles, ",".join(role_ids), ctx.guild.id)
                roles_mentions = ", ".join(
                    [role.mention for role in self.selected_roles])
                await interaction.response.edit_message(
                    embed=create_embed(R.setup_modroles_set % roles_mentions,
                                       color=C.success_color, title=R.mod_roles_title),
                    view=None
                )
                logger.info(
                    f"Moderator roles set to {[role.name for role in self.selected_roles]}",
                    ctx.interaction)
                self.stop()

        # Show current mod roles if set
        mod_role_ids = db.get_constant(C.mod_roles, ctx.guild.id)
        if mod_role_ids:
            role_ids = [int(rid) for rid in mod_role_ids.split(",") if rid]
            roles = [ctx.guild.get_role(rid) for rid in role_ids]
            roles = [r for r in roles if r]
            if roles:
                current_roles_msg = R.setup_modroles_current % (
                    ", ".join([r.mention for r in roles]))
                await ctx.respond(
                    embed=create_embed(current_roles_msg,
                                       title=R.mod_roles_title),
                    ephemeral=True
                )
                logger.info(
                    f"Told user current mod roles: {[r.name for r in roles]}", ctx.interaction)
            else:
                await ctx.respond(embed=error_embed(R.setup_modroles_not_found, title=R.mod_roles_title), ephemeral=True)
                logger.error(
                    We(R.setup_modroles_not_found), ctx.interaction)
        await ctx.respond(
            embed=create_embed(R.setup_modroles_select_prompt,
                               title=R.mod_roles_title),
            view=ModRolesSelectView(),
            ephemeral=True
        )
        logger.info("Opened mod roles set dialog", ctx.interaction)

    @setup.command(name="timeoutlogchannel", description=R.setup_timeout_logchannel_desc)
    @discord.default_permissions(administrator=True)
    @discord.option(
        "channel",
        description=R.setup_timeout_logchannel_desc,
        required=False,
        default=None,
        type=discord.SlashCommandOptionType.channel,
        channel_types=[discord.ChannelType.text]
    )
    async def setup_timeout_logchannel(ctx: discord.ApplicationContext, channel: discord.TextChannel = None):
        """
        Set the log channel for timeouts.
        If no channel is provided, it will show the current log channel.
        Args:
            ctx (discord.ApplicationContext): The context of the command.
            channel (discord.TextChannel, optional): The text channel to set for timeout logs. Defaults to None.
        """
        guild_id = ctx.guild.id
        if channel is None:
            # Tell the user the current timeout log channel
            log_channel_id = db.get_constant(C.timeout_log_channel, guild_id)
            if log_channel_id is None:
                # No log channel set
                await handle_error(
                    ctx.interaction, We(R.setup_no_timeout_logchannel)
                )
                return
            log_channel = ctx.guild.get_channel(int(log_channel_id))
            if log_channel is None:
                await handle_error(
                    ctx.interaction, We(R.setup_timeout_logchannel_not_found)
                )
                return
            await ctx.respond(
                embed=create_embed(R.setup_timeout_logchannel_current %
                                   log_channel.mention, title=R.timeout_log_channel_title),
                ephemeral=True
            )
            return

        # Set the log channel in the database
        db.set_constant(C.timeout_log_channel,
                        str(channel.id), guild_id)
        await ctx.respond(
            embed=create_embed(R.setup_timeout_logchannel_set % channel.mention,
                               color=C.success_color, title=R.timeout_log_channel_title),
            ephemeral=True
        )
        logger.info(
            f"Timeout log channel set to {channel.name} (ID: {channel.id})",
            ctx.interaction)

    bot.add_application_command(setup)
