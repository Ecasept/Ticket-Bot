"""
Setup functionality module - core logic separated from command interface.
"""
import discord
from src.res import R, DEFAULT_LANG, lang_info
from src.constants import C
from src.utils import create_embed, handle_error, logger, error_embed, get_timeout_log_channel
from src.database import db
from src.error import We


async def setup_tickets(interaction: discord.Interaction, category: discord.CategoryChannel = None):
    """
    Set or view the tickets category.
    Args:
        interaction (discord.Interaction): The interaction context.
        category (discord.CategoryChannel): The category to set (optional).
    """
    if category is None:
        # Tell the user the current ticket category
        cat = db.constant.get(C.DBKey.ticket_category, interaction.guild.id)
        if cat is None:
            await interaction.response.send_message(embed=create_embed(R.setup_no_ticket_category, color=C.warning_color, title=R.setup_title), ephemeral=True)
            logger.error(We(R.setup_no_ticket_category), interaction)
            return
        # Get the category channel
        cat = interaction.guild.get_channel(int(cat))
        if cat is None:
            # Category not found
            await interaction.response.send_message(embed=error_embed(R.setup_ticket_category_not_found), ephemeral=True)
            logger.error(We(R.setup_ticket_category_not_found), interaction)
            return
        await interaction.response.send_message(
            embed=create_embed(R.setup_tickets_current_category %
                               cat.mention, title=R.setup_title),
            ephemeral=True
        )
        logger.info(
            f"Told user current ticket category: {cat.name} (ID: {cat.id})", interaction)
        return

    # Set the category in the database
    db.constant.set(C.DBKey.ticket_category, str(
        category.id), interaction.guild.id)
    await interaction.response.send_message(
        embed=create_embed(R.setup_tickets_set_category %
                           category.mention, color=C.success_color, title=R.setup_title),
        ephemeral=True
    )
    logger.info(
        f"Ticket category set to {category.name} (ID: {category.id})", interaction)


async def setup_transcript(interaction: discord.Interaction, category: discord.CategoryChannel = None):
    """
    Set or view the transcript category.
    Args:
        interaction (discord.Interaction): The interaction context.
        category (discord.CategoryChannel): The category to set (optional).
    """
    if category is None:
        # Tell the user the current transcript category
        cat = db.constant.get(C.DBKey.transcript_category,
                              interaction.guild.id)
        if cat is None:
            await interaction.response.send_message(embed=create_embed(R.setup_no_transcript_category, color=C.warning_color), ephemeral=True)
            logger.error(We(R.setup_no_transcript_category), interaction)
            return
        # Get the category channel
        cat = interaction.guild.get_channel(int(cat))
        if cat is None:
            # Category not found
            await interaction.response.send_message(embed=error_embed(R.setup_transcript_category_not_found), ephemeral=True)
            logger.error(
                We(R.setup_transcript_category_not_found), interaction)
            return
        await interaction.response.send_message(
            embed=create_embed(
                R.setup_transcript_current_category % cat.mention),
            ephemeral=True
        )
        logger.info(
            f"Told user current transcript category: {cat.name} (ID: {cat.id})", interaction)
        return

    # Set the category in the database
    db.constant.set(C.DBKey.transcript_category, str(
        category.id), interaction.guild.id)
    await interaction.response.send_message(
        embed=create_embed(R.setup_transcript_set_category %
                           category.mention, color=C.success_color),
        ephemeral=True
    )
    logger.info(
        f"Transcript category set to {category.name} (ID: {category.id})", interaction)


async def setup_logchannel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    """
    Set or view the log channel.
    Args:
        interaction (discord.Interaction): The interaction context.
        channel (discord.TextChannel): The channel to set (optional).
    """
    if channel is None:
        # Tell the user the current log channel
        log_channel_id = db.constant.get(
            C.DBKey.log_channel, interaction.guild.id)
        if log_channel_id is None:
            await interaction.response.send_message(embed=create_embed(R.setup_no_logchannel, color=C.warning_color, title=R.log_channel_title), ephemeral=True)
            logger.error(We(R.setup_no_logchannel), interaction)
            return
        log_ch = interaction.guild.get_channel(int(log_channel_id))
        if log_ch is None:
            await interaction.response.send_message(embed=error_embed(R.setup_logchannel_not_found, title=R.log_channel_title), ephemeral=True)
            logger.error(We(R.setup_logchannel_not_found), interaction)
            return
        await interaction.response.send_message(
            embed=create_embed(R.setup_logchannel_current %
                               log_ch.mention, title=R.log_channel_title),
            ephemeral=True
        )
        logger.info(
            f"Told user current log channel: {log_ch.name} (ID: {log_ch.id})", interaction)
        return

    # Set the log channel in the database
    db.constant.set(C.DBKey.log_channel, str(channel.id), interaction.guild.id)
    await interaction.response.send_message(
        embed=create_embed(R.setup_logchannel_set % channel.mention,
                           color=C.success_color, title=R.log_channel_title),
        ephemeral=True
    )
    logger.info(
        f"Log channel set to {channel.name} (ID: {channel.id})", interaction)


async def setup_timeout_logchannel(interaction: discord.Interaction, channel: discord.TextChannel = None):
    """
    Set or view the timeout log channel.
    Args:
        interaction (discord.Interaction): The interaction context.
        channel (discord.TextChannel): The channel to set (optional).
    """
    guild_id = interaction.guild.id
    if channel is None:
        # Tell the user the current timeout log channel
        log_channel, err = await get_timeout_log_channel(interaction.guild)
        if err:
            await handle_error(interaction, err)
            return
        await interaction.response.send_message(
            embed=create_embed(R.setup_timeout_logchannel_current %
                               log_channel.mention, title=R.timeout_log_channel_title),
            ephemeral=True
        )
        return

    # Set the log channel in the database
    db.constant.set(C.DBKey.timeout_log_channel, str(channel.id), guild_id)
    await interaction.response.send_message(
        embed=create_embed(R.setup_timeout_logchannel_set % channel.mention,
                           color=C.success_color, title=R.timeout_log_channel_title),
        ephemeral=True
    )
    logger.info(
        f"Timeout log channel set to {channel.name} (ID: {channel.id})", interaction)


async def show_modroles(interaction: discord.Interaction):
    """
    Show the current moderator roles.
    Args:
        interaction (discord.Interaction): The interaction context.
    """
    mod_role_ids = db.constant.get(C.DBKey.mod_roles, interaction.guild.id)
    if mod_role_ids:
        role_ids = [int(rid) for rid in mod_role_ids.split(",") if rid]
        roles = [interaction.guild.get_role(rid) for rid in role_ids]
        roles = [r for r in roles if r]
        if roles:
            current_roles_msg = R.setup_modroles_current % (
                ", ".join([r.mention for r in roles]))
            await interaction.response.send_message(
                embed=create_embed(current_roles_msg, title=R.mod_roles_title),
                ephemeral=True
            )
            logger.info(
                f"Told user current mod roles: {[r.name for r in roles]}", interaction)
        else:
            await interaction.response.send_message(embed=error_embed(R.setup_modroles_not_found, title=R.mod_roles_title), ephemeral=True)
            logger.error(We(R.setup_modroles_not_found), interaction)
    else:
        await interaction.response.send_message(embed=create_embed(R.setup_no_modroles, color=C.warning_color, title=R.mod_roles_title), ephemeral=True)
        logger.error(We(R.setup_no_modroles), interaction)


def get_native_name(locale: str) -> str:
    """
    Get the native name of a language by its locale code.
    Args:
        locale (str): The locale code (e.g., 'en', 'fr').
    Returns:
        str: The native name of the language.
    """
    item = next((x for x in lang_info if x["code"] == locale), None)
    return item["native_name"] if item else R.feature.setup.language.unknown


async def setup_language(interaction: discord.Interaction, language: str = None):
    """
    Set or view the guild language.
    Args:
        interaction (discord.Interaction): The interaction context.
        language (str): The language to set (optional).
    """
    if language:
        db.constant.set(C.DBKey.locale, language, interaction.guild.id)
        # Switch to the new language
        await R.init(interaction.guild.id)
        lang = get_native_name(language)
        await interaction.response.send_message(embed=create_embed(R.feature.setup.language.set_success % lang, color=C.success_color), ephemeral=True)
        logger.info(
            f"Language set to {language}",
            interaction)
    else:
        locale = db.constant.get(
            C.DBKey.locale, interaction.guild.id) or DEFAULT_LANG

        lang = get_native_name(locale)

        await interaction.response.send_message(embed=create_embed(R.feature.setup.language.current % lang), ephemeral=True)
        logger.info(
            f"Told user current language: {locale}", interaction)
