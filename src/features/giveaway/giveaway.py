"""
Giveaway functionality module - core logic separated from command interface.
"""
import discord
import datetime
import random
from src.res import R
from src.constants import C
from src.utils import create_embed, parse_duration, handle_error, logger, error_embed
from src.database import db
from src.error import Ce, We
from discord.ext import tasks

from src.custom_bot import CustomBot


async def create_giveaway_embed(giveaway_data):
    """
    Create the embed for a giveaway announcement.
    Args:
        giveaway_data (dict): Giveaway data containing prize, duration, etc.
    Returns:
        discord.Embed: The formatted giveaway embed.
    """
    embed = discord.Embed(
        title=R.giveaway_title % giveaway_data['prize'],
        description=R.giveaway_description % (
            giveaway_data['prize'], giveaway_data['winner_count']),
        color=C.embed_color
    )

    # Calculate end time for display
    end_time = datetime.datetime.now(
    ) + datetime.timedelta(seconds=giveaway_data['duration'])
    embed.add_field(
        name=R.giveaway_ends_at,
        value=f"<t:{int(end_time.timestamp())}:f>",
        inline=False
    )

    if giveaway_data['role_id']:
        embed.add_field(
            name=R.giveaway_role_prize,
            value=f"<@&{giveaway_data['role_id']}>",
            inline=False
        )

    embed.add_field(
        name=R.giveaway_participation,
        value=R.giveaway_react_to_participate % C.giveaway_reaction,
        inline=False
    )

    embed.set_footer(text=R.giveaway_footer % giveaway_data['host_id'])
    return embed


async def create_giveaway(interaction: discord.Interaction, dauer: str, preis: str, gewinner: int = 1, rolle: discord.Role = None):
    """
    Create a giveaway with the specified parameters.
    Args:
        interaction (discord.Interaction): The interaction context.
        dauer (str): Duration of the giveaway (e.g., "30s", "2m", "1h").
        preis (str): What is being given away.
        gewinner (int): Number of winners to select.
        rolle (discord.Role): Role to award to winners (optional).
    """
    # Parse duration
    seconds, error = parse_duration(dauer)
    if error:
        await handle_error(interaction, error)
        return
    if seconds < C.giveaway_min_duration or seconds > C.giveaway_max_duration:
        await handle_error(interaction, We(R.giveaway_duration_extreme))
        return

    # Validate winner count
    if not (1 <= gewinner <= 20):
        await handle_error(interaction, We(R.giveaway_invalid_winners))
        return

    # Create giveaway embed
    giveaway_data = {
        'prize': preis,
        'duration': seconds,
        'role_id': str(rolle.id) if rolle else None,
        'host_id': str(interaction.user.id),
        'winner_count': gewinner
    }

    embed = await create_giveaway_embed(giveaway_data)

    # Send the giveaway message
    await interaction.response.defer(ephemeral=True)
    message = await interaction.channel.send(embed=embed,)

    # Add reaction for participation
    await message.add_reaction(discord.PartialEmoji(name=C.giveaway_reaction))

    # Calculate end time
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

    # Store in database
    db.giveaway.create(
        message_id=message.id,
        channel_id=interaction.channel.id,
        guild_id=interaction.guild.id,
        host_id=interaction.user.id,
        prize=preis,
        winner_count=gewinner,
        role_id=rolle.id if rolle else None,
        ends_at=end_time
    )

    # Send confirmation
    await interaction.followup.send(R.giveaway_started, ephemeral=True)
    logger.info(f"Giveaway {message.id} started", interaction)


async def end_giveaway(bot: CustomBot, giveaway):
    """
    End a giveaway and select winners.
    Args:
        bot (CustomBot): The bot instance.
        giveaway: The giveaway object from database.
    """
    try:
        # Get the channel and message
        channel = bot.get_channel(giveaway.channel_id)
        if not channel:
            logger.error(
                We(f"Channel {giveaway.channel_id} not found for giveaway {giveaway.message_id}"))
            db.giveaway.update(giveaway.message_id, ended=True)
            return

        try:
            message = await channel.fetch_message(giveaway.message_id)
        except discord.NotFound:
            logger.error(
                We(f"Message {giveaway.message_id} not found for giveaway"))
            db.giveaway.update(giveaway.message_id, ended=True)
            return

        # Get participants who reacted with the giveaway emoji
        participants = set()
        for reaction in message.reactions:
            if str(reaction.emoji) == C.giveaway_reaction:
                async for user in reaction.users():
                    if not user.bot:
                        participants.add(user)
                break

        if not participants:
            await channel.send(
                embed=create_embed(
                    R.giveaway_no_participants,
                    title=R.giveaway_ended_title,
                )
            )
            db.giveaway.update(giveaway.message_id, ended=True)
            return

        # Select winners
        winner_count = min(giveaway.winner_count, len(participants))
        winners = random.sample(list(participants), winner_count)

        # Announce winners
        winners_mention = ", ".join(user.mention for user in winners)
        await channel.send(R.giveaway_winners_announcement % (winners_mention, giveaway.prize))

        # Award role if specified
        if giveaway.role_id:
            guild = channel.guild
            role = guild.get_role(giveaway.role_id)
            if role:
                for winner in winners:
                    member = guild.get_member(winner.id)
                    if member:
                        try:
                            await member.add_roles(role, reason=R.feature.giveaway.role_award_reason)
                        except discord.Forbidden:
                            msg = R.giveaway_role_perms_error % (
                                role.mention, winner.mention)
                            await channel.send(embed=error_embed(msg))
                            logger.error(We(msg))

        # Mark as ended
        db.giveaway.update(giveaway.message_id, ended=True)
        logger.info(
            f"Giveaway {giveaway.message_id} ended with {len(winners)} winners")

    except Exception as e:
        logger.error(Ce(f"Error ending giveaway {giveaway.message_id}: {e}"))
        # Still mark as ended to prevent infinite retries
        db.giveaway.update(giveaway.message_id, ended=True)


def setup_giveaway_background_task(bot: CustomBot):
    """
    Setup the background task that checks for ended giveaways.
    Args:
        bot (CustomBot): The Discord bot instance.
    """
    @tasks.loop(seconds=C.giveaway_check_interval)
    async def check_ended_giveaways():
        """Check for ended giveaways and process them."""
        try:
            now = datetime.datetime.now()
            ended_giveaways = db.giveaway.get_active(now)
            if ended_giveaways:
                logger.info(f"Found {len(ended_giveaways)} ended giveaways.")

            for giveaway in ended_giveaways:
                await R.init(giveaway.guild_id)
                await end_giveaway(bot, giveaway)

        except Exception as e:
            logger.error(We(f"Error in giveaway check task: {e}"))

    # Start the background task
    check_ended_giveaways.start()
