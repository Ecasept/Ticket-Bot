"""
Setup slash command - separated from functionality.
"""
import discord
from src.res import R, RD, RL, lang_info, late, button, select, role_select, LateView
from src.constants import C
from src.utils import create_embed, handle_error, logger, error_embed, get_timeout_log_channel
from src.database import db
from src.error import We
from src.features.setup.setup import (
    setup_tickets, setup_transcript, setup_logchannel,
    setup_timeout_logchannel, setup_language
)


def setup_setup_command(bot: discord.Bot):
    """
    Setup the setup command group for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """
    setup = discord.SlashCommandGroup(
        name=RD.command.setup.name,
        name_localizations=RL.command.setup.name,
        description=RD.command.setup.desc,
        description_localizations=RL.command.setup.desc,
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @setup.command(
        name=RD.command.setup.tickets.name,
        name_localizations=RL.command.setup.tickets.name,
        description=RD.command.setup.tickets.desc,
        description_localizations=RL.command.setup.tickets.desc
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        name=RD.command.setup.tickets.option.category,
        name_localizations=RL.command.setup.tickets.option.category,
        description=RD.command.setup.tickets.option.category_desc,
        description_localizations=RL.command.setup.tickets.option.category_desc,
        required=False,
        default=None,
        type=discord.SlashCommandOptionType.channel,
        channel_types=[discord.ChannelType.category]
    )
    async def setup_tickets_command(ctx: discord.ApplicationContext, category: discord.CategoryChannel = None):
        await setup_tickets(ctx.interaction, category)

    @setup.command(
        name=RD.command.setup.transcript.name,
        name_localizations=RL.command.setup.transcript.name,
        description=RD.command.setup.transcript.desc,
        description_localizations=RL.command.setup.transcript.desc
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        name=RD.command.setup.transcript.option.category,
        name_localizations=RL.command.setup.transcript.option.category,
        description=RD.command.setup.transcript.option.category_desc,
        description_localizations=RL.command.setup.transcript.option.category_desc,
        required=False,
        default=None,
        type=discord.SlashCommandOptionType.channel,
        channel_types=[discord.ChannelType.category]
    )
    async def setup_transcript_command(ctx: discord.ApplicationContext, category: discord.CategoryChannel = None):
        await setup_transcript(ctx.interaction, category)

    @setup.command(
        name=RD.command.setup.logchannel.name,
        name_localizations=RL.command.setup.logchannel.name,
        description=RD.command.setup.logchannel.desc,
        description_localizations=RL.command.setup.logchannel.desc
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        name=RD.command.setup.logchannel.option.channel,
        name_localizations=RL.command.setup.logchannel.option.channel,
        description=RD.command.setup.logchannel.option.channel_desc,
        description_localizations=RL.command.setup.logchannel.option.channel_desc,
        required=False,
        default=None,
        type=discord.SlashCommandOptionType.channel,
        channel_types=[discord.ChannelType.text]
    )
    async def setup_logchannel_command(ctx: discord.ApplicationContext, channel: discord.TextChannel = None):
        await setup_logchannel(ctx.interaction, channel)

    @setup.command(
        name=RD.command.setup.timeoutlogchannel.name,
        name_localizations=RL.command.setup.timeoutlogchannel.name,
        description=RD.command.setup.timeoutlogchannel.desc,
        description_localizations=RL.command.setup.timeoutlogchannel.desc
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        name=RD.command.setup.timeoutlogchannel.option.channel,
        name_localizations=RL.command.setup.timeoutlogchannel.option.channel,
        description=RD.command.setup.timeoutlogchannel.option.channel_desc,
        description_localizations=RL.command.setup.timeoutlogchannel.option.channel_desc,
        required=False,
        default=None,
        type=discord.SlashCommandOptionType.channel,
        channel_types=[discord.ChannelType.text]
    )
    async def setup_timeout_logchannel_command(ctx: discord.ApplicationContext, channel: discord.TextChannel = None):
        await setup_timeout_logchannel(ctx.interaction, channel)

    @setup.command(
        name=RD.command.setup.modroles.name,
        name_localizations=RL.command.setup.modroles.name,
        description=RD.command.setup.modroles.desc,
        description_localizations=RL.command.setup.modroles.desc
    )
    @discord.default_permissions(administrator=True)
    async def setup_modroles_command(ctx: discord.ApplicationContext):
        """
        Show a dialog to select multiple moderator roles for the bot.
        Args:
            ctx (discord.ApplicationContext): The command context.
        """
        class ModRolesSelectView(LateView):
            def __init__(self):
                super().__init__(timeout=120)
                self.selected_roles = []

            @late(lambda: role_select(
                placeholder=R.setup_modroles_select_placeholder,
                min_values=1,
                max_values=25,
            ))
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                self.selected_roles = select.values
                await interaction.response.defer()

            @late(lambda: button(
                label=R.modroles_submit_button_label,
                style=discord.ButtonStyle.primary,
            ))
            async def submit_callback(self, button, interaction: discord.Interaction):
                if not self.selected_roles:
                    await interaction.response.send_message(embed=create_embed(R.setup_modroles_none_selected, color=C.error_color), ephemeral=True)
                    logger.error(
                        We(R.setup_modroles_none_selected), ctx.interaction)
                    return
                # Save selected roles as comma-separated IDs
                role_ids = [str(role.id) for role in self.selected_roles]
                db.constant.set(C.DBKey.mod_roles, ",".join(role_ids), ctx.guild.id)
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
        mod_role_ids = db.constant.get(C.DBKey.mod_roles, ctx.guild.id)
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

    @setup.command(
        name=RD.command.setup.language.name,
        name_localizations=RL.command.setup.language.name,
        description=RD.command.setup.language.desc,
        description_localizations=RL.command.setup.language.desc
    )
    @discord.default_permissions(administrator=True)
    @discord.option(
        name=RD.command.setup.language.option.language,
        name_localizations=RL.command.setup.language.option.language,
        description=RD.command.setup.language.option.language_desc,
        description_localizations=RL.command.setup.language.option.language_desc,
        required=False,
        default=None,
        choices=[item["code"] for item in lang_info]
    )
    async def setup_language_command(ctx: discord.ApplicationContext, language: str = None):
        await setup_language(ctx.interaction, language)

    bot.add_application_command(setup)
