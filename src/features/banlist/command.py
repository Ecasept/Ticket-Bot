"""
This module contains the commands for the banlist feature.
"""
import discord
from src.database import db
from src.error import Error, We
from src.res import R, RD, RL
from src.constants import C
from src.utils import handle_error, create_embed, logger, is_valid_url
from src.features.shared.list_display import ListDisplayView, create_list_embeds


def get_banlist_items(guild_id: int) -> list[tuple[str, str]]:
    """
    Retrieves and formats the banlist for a given guild.
    """
    bans = db.banlist.get_bans(guild_id)
    items = []
    for name, reason, banned_by, length, image_url in bans:
        title = f"**{name}**"
        if image_url:
            title += R.banlist_image_indicator
        content = f"- {R.banlist_item_banned_by_for % (banned_by, length)}\n- {R.banlist_item_reason % reason}"
        items.append((title, content))
    return items


async def update_banlist(interaction: discord.Interaction):
    """
    Callback to update the banlist message.
    """
    items = get_banlist_items(interaction.guild.id)
    embeds_or_err = create_list_embeds(
        R.banlist_embed_title, items, R.banlist_no_bans)
    if isinstance(embeds_or_err, Error):
        await handle_error(interaction, embeds_or_err)
        return
    await interaction.response.edit_message(embeds=embeds_or_err)
    logger.info("Banlist updated", interaction)


def setup_banlist_command(bot: discord.Bot):
    """
    Sets up the banlist command group.
    """
    banlist = discord.SlashCommandGroup(
        name=RD.command.banlist.name,
        name_localizations=RL.command.banlist.name,
        description=RD.command.banlist.desc,
        description_localizations=RL.command.banlist.desc,
        default_member_permissions=discord.Permissions(moderate_members=True)
    )

    @banlist.command(
        name=RD.command.banlist.show.name,
        name_localizations=RL.command.banlist.show.name,
        description=RD.command.banlist.show.desc,
        description_localizations=RL.command.banlist.show.desc
    )
    async def show(ctx: discord.ApplicationContext):
        """
        Displays the banlist.
        """
        items = get_banlist_items(ctx.guild.id)
        embeds_or_err = create_list_embeds(
            R.banlist_embed_title, items, R.banlist_no_bans)
        if isinstance(embeds_or_err, Error):
            await handle_error(ctx.interaction, embeds_or_err)
            return

        view = ListDisplayView(custom_id="update_banlist",
                               update_callback=update_banlist)
        await ctx.respond(embeds=embeds_or_err, view=view)

    @banlist.command(
        name=RD.command.banlist.add.name,
        name_localizations=RL.command.banlist.add.name,
        description=RD.command.banlist.add.desc,
        description_localizations=RL.command.banlist.add.desc
    )
    @discord.option(
        name=RD.command.banlist.add.option.name,
        name_localizations=RL.command.banlist.add.option.name,
        description=RD.command.banlist.add.option.name_desc,
        description_localizations=RL.command.banlist.add.option.name_desc,
        required=True
    )
    @discord.option(
        name=RD.command.banlist.add.option.reason,
        name_localizations=RL.command.banlist.add.option.reason,
        description=RD.command.banlist.add.option.reason_desc,
        description_localizations=RL.command.banlist.add.option.reason_desc,
        required=True
    )
    @discord.option(
        name=RD.command.banlist.add.option.banned_by,
        name_localizations=RL.command.banlist.add.option.banned_by,
        description=RD.command.banlist.add.option.banned_by_desc,
        description_localizations=RL.command.banlist.add.option.banned_by_desc,
        required=True
    )
    @discord.option(
        name=RD.command.banlist.add.option.length,
        name_localizations=RL.command.banlist.add.option.length,
        description=RD.command.banlist.add.option.length_desc,
        description_localizations=RL.command.banlist.add.option.length_desc,
        required=True
    )
    @discord.option(
        name=RD.command.banlist.add.option.image_url,
        name_localizations=RL.command.banlist.add.option.image_url,
        description=RD.command.banlist.add.option.image_desc,
        description_localizations=RL.command.banlist.add.option.image_desc,
        required=False
    )
    async def add(ctx: discord.ApplicationContext, name: str, reason: str, banned_by: str, length: str, image_url: str = None):
        """
        Adds a user to the banlist.
        """
        if db.banlist.is_banned(name, ctx.guild.id):
            await handle_error(ctx.interaction, We(R.banlist_already_banned % name))
            return

        # Validate image URL if provided
        if image_url and not is_valid_url(image_url):
            await handle_error(ctx.interaction, We(R.banlist_invalid_url))
            return

        db.banlist.add_ban(name, ctx.guild.id, reason,
                           banned_by, length, image_url)
        await ctx.respond(embed=create_embed(R.banlist_add_success % name, color=C.success_color), ephemeral=True)
        logger.info(f"Added {name} to banlist", ctx.interaction)

    @banlist.command(
        name=RD.command.banlist.remove.name,
        name_localizations=RL.command.banlist.remove.name,
        description=RD.command.banlist.remove.desc,
        description_localizations=RL.command.banlist.remove.desc
    )
    @discord.option(
        name=RD.command.banlist.remove.option.name,
        name_localizations=RL.command.banlist.remove.option.name,
        description=RD.command.banlist.remove.option.name_desc,
        description_localizations=RL.command.banlist.remove.option.name_desc,
        required=True
    )
    async def remove(ctx: discord.ApplicationContext, name: str):
        """
        Removes a user from the banlist.
        """
        if not db.banlist.is_banned(name, ctx.guild.id):
            await handle_error(ctx.interaction, We(R.banlist_not_banned % name))
            return

        db.banlist.remove_ban(name, ctx.guild.id)
        await ctx.respond(embed=create_embed(R.banlist_remove_success % name, color=C.success_color), ephemeral=True)
        logger.info(f"Removed {name} from banlist", ctx.interaction)

    @banlist.command(
        name=RD.command.banlist.showimg.name,
        name_localizations=RL.command.banlist.showimg.name,
        description=RD.command.banlist.showimg.desc,
        description_localizations=RL.command.banlist.showimg.desc
    )
    @discord.option(
        name=RD.command.banlist.showimg.option.name,
        name_localizations=RL.command.banlist.showimg.option.name,
        description=RD.command.banlist.showimg.option.name_desc,
        description_localizations=RL.command.banlist.showimg.option.name_desc,
        required=True
    )
    async def showimg(ctx: discord.ApplicationContext, name: str):
        """
        Shows the image of a banned user.
        """
        if not db.banlist.is_banned(name, ctx.guild.id):
            await handle_error(ctx.interaction, We(R.banlist_not_banned % name))
            return

        ban_data = db.banlist.get_ban(name, ctx.guild.id)
        image_url = ban_data[4]

        if not image_url:
            await handle_error(ctx.interaction, We(R.banlist_no_image % name))
            return

        embed = create_embed(
            title=R.banlist_showimg_embed_title % name,
            color=C.embed_color
        )
        embed.set_image(url=image_url)
        await ctx.respond(embed=embed)

    bot.add_application_command(banlist)
