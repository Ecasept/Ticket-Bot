"""
Setup slash command - separated from functionality.
"""
import discord
from src.res import R, C
from src.utils import create_embed, handle_error, logger, error_embed, get_timeout_log_channel
from src.database import db
from src.error import We
from src.features.setup.setup import (
    setup_tickets, setup_transcript, setup_logchannel, 
    setup_timeout_logchannel
)


def setup_setup_command(bot: discord.Bot):
    """
    Setup the setup command group for the bot.
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
    async def setup_tickets_command(ctx: discord.ApplicationContext, category: discord.CategoryChannel = None):
        await setup_tickets(ctx.interaction, category)

    @setup.command(name="transcript", description=R.setup_transcript_desc)
    @discord.default_permissions(administrator=True)
    @discord.option(
        "category",
        required=False,
        default=None,
        type=discord.SlashCommandOptionType.channel,
        channel_types=[discord.ChannelType.category]
    )
    async def setup_transcript_command(ctx: discord.ApplicationContext, category: discord.CategoryChannel = None):
        await setup_transcript(ctx.interaction, category)

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
    async def setup_logchannel_command(ctx: discord.ApplicationContext, channel: discord.TextChannel = None):
        await setup_logchannel(ctx.interaction, channel)

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
    async def setup_timeout_logchannel_command(ctx: discord.ApplicationContext, channel: discord.TextChannel = None):
        await setup_timeout_logchannel(ctx.interaction, channel)

    @setup.command(name="modroles", description=R.setup_modroles_desc)
    @discord.default_permissions(administrator=True)
    async def setup_modroles_command(ctx: discord.ApplicationContext):
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
                    logger.error(We(R.setup_modroles_none_selected), ctx.interaction)
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
                logger.error(We(R.setup_modroles_not_found), ctx.interaction)
        
        await ctx.respond(
            embed=create_embed(R.setup_modroles_select_prompt,
                               title=R.mod_roles_title),
            view=ModRolesSelectView(),
            ephemeral=True
        )
        logger.info("Opened mod roles set dialog", ctx.interaction)

    bot.add_application_command(setup)
