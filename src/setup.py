import discord

from src.utils import C, R, error_embed, create_embed
from src.database import db
from src.utils import logger


def setup_setup_command(bot: discord.Bot):
    """
    Setup the setup command for the bot.
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
            cat = db.get_constant(C.ticket_category)
            if cat is None:
                # No category set
                await ctx.respond(embed=create_embed(R.setup_no_ticket_category, color=C.warning_color), ephemeral=True)
                return
            cat = ctx.guild.get_channel(int(cat))
            if cat is None:
                # Category not found
                await ctx.respond(embed=error_embed(R.setup_ticket_category_not_found), ephemeral=True)
                return
            await ctx.respond(
                embed=create_embed(R.setup_tickets_current_category %
                                   cat.mention, title=R.setup_title),
                ephemeral=True
            )
            return
        # Set the category in the database
        db.set_constant(C.ticket_category, str(category.id))
        await ctx.respond(
            embed=create_embed(R.setup_tickets_set_category %
                               category.mention, color=C.success_color, title=R.setup_title),
            ephemeral=True
        )
        logger.info(
            "setup", f"Ticket category set to {category.name} (ID: {category.id}) by {ctx.user.name} (ID: {ctx.user.id})")

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
            cat = db.get_constant(C.transcript_category)
            if cat is None:
                # No category set
                await ctx.respond(embed=create_embed(R.setup_no_transcript_category, color=C.warning_color), ephemeral=True)
                return
            # Get the category channel
            cat = ctx.guild.get_channel(int(cat))
            if cat is None:
                # Category not found
                await ctx.respond(embed=error_embed(R.setup_transcript_category_not_found), ephemeral=True)
                return
            await ctx.respond(
                embed=create_embed(
                    R.setup_transcript_current_category % cat.mention),
                ephemeral=True
            )
            return
        # Set the category in the database
        db.set_constant(C.transcript_category, str(category.id))
        await ctx.respond(
            embed=create_embed(R.setup_transcript_set_category %
                               category.mention, color=C.success_color),
            ephemeral=True
        )
        logger.info(
            "setup", f"Transcript category set to {category.name} (ID: {category.id}) by {ctx.user.name} (ID: {ctx.user.id})")

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
            log_channel_id = db.get_constant(C.log_channel)
            if log_channel_id is None:
                await ctx.respond(embed=create_embed(R.setup_no_logchannel, color=C.warning_color, title=R.log_channel_title), ephemeral=True)
                return
            log_ch = ctx.guild.get_channel(int(log_channel_id))
            if log_ch is None:
                await ctx.respond(embed=error_embed(R.setup_logchannel_not_found, title=R.log_channel_title), ephemeral=True)
                return
            await ctx.respond(
                embed=create_embed(R.setup_logchannel_current %
                                   log_ch.mention, title=R.log_channel_title),
                ephemeral=True
            )
            return

        # Set the log channel in the database
        db.set_constant(C.log_channel, str(channel.id))
        await ctx.respond(
            embed=create_embed(R.setup_logchannel_set % channel.mention,
                               color=C.success_color, title=R.log_channel_title),
            ephemeral=True
        )
        logger.info(
            "setup", f"Log channel set to {channel.name} (ID: {channel.id}) by {ctx.user.name} (ID: {ctx.user.id})")

    @setup.command(name="modroles", description=R.setup_modroles_desc)
    @discord.default_permissions(administrator=True)
    async def setup_modroles(ctx: discord.ApplicationContext):
        """
        Show a dialog to select multiple moderator roles for the bot.
        """
        class ModRolesSelectView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=120)
                self.selected_roles = []

            @discord.ui.role_select(
                placeholder=R.setup_modroles_select_placeholder,
                min_values=1,
                max_values=25,
                custom_id="modroles_select_dropdown"
            )
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                self.selected_roles = select.values
                await interaction.response.defer()

            @discord.ui.button(
                label=R.modroles_submit_button_label,
                style=discord.ButtonStyle.primary,
                custom_id="submit_modroles"
            )
            async def submit_callback(self, button, interaction: discord.Interaction):
                if not self.selected_roles:
                    await interaction.response.send_message(embed=create_embed(R.setup_modroles_none_selected, color=C.error_color), ephemeral=True)
                    return
                # Save selected roles as comma-separated IDs
                role_ids = [str(role.id) for role in self.selected_roles]
                db.set_constant(C.mod_roles, ",".join(role_ids))
                roles_mentions = ", ".join(
                    [role.mention for role in self.selected_roles])
                await interaction.response.edit_message(
                    embed=create_embed(R.setup_modroles_set % roles_mentions,
                                       color=C.success_color, title=R.mod_roles_title),
                    view=None
                )
                logger.info(
                    "setup", f"Moderator roles set to {[role.name for role in self.selected_roles]} by {ctx.user.name} (ID: {ctx.user.id})")
                self.stop()

        # Show current mod roles if set
        mod_role_ids = db.get_constant(C.mod_roles)
        if mod_role_ids:
            role_ids = [int(rid) for rid in mod_role_ids.split(",") if rid]
            roles = [ctx.guild.get_role(rid) for rid in role_ids]
            roles = [r for r in roles if r]
            if roles:
                await ctx.respond(
                    embed=create_embed(R.setup_modroles_current % (
                        ", ".join([r.mention for r in roles])), title=R.mod_roles_title),
                    ephemeral=True
                )
            else:
                await ctx.respond(embed=error_embed(R.setup_modroles_not_found, title=R.mod_roles_title), ephemeral=True)
        await ctx.respond(
            embed=create_embed(R.setup_modroles_select_prompt,
                               title=R.mod_roles_title),
            view=ModRolesSelectView(),
            ephemeral=True
        )

    bot.add_application_command(setup)
