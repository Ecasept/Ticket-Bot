"""
Giveaway module for the Discord bot. Handles giveaway creation, management, and automatic winner selection.
"""
import discord
from discord.ext import tasks
import datetime
import random
import re
from src.database import db
from src.utils import error_embed, format_duration, logger, handle_error, create_embed, mention, parse_duration
from src.res import C, R
from src.error import We


async def create_giveaway_embed(giveaway_data: dict) -> discord.Embed:
    """
    Create an embed for a giveaway.
    Args:
        giveaway_data (dict): Giveaway information.
        participants_count (int): Number of current participants.
    Returns:
        discord.Embed: The giveaway embed.
    """
    duration = giveaway_data["duration"]

    color = C.embed_color
    title = R.giveaway_title

    role_text = f"<@&{giveaway_data['role_id']}>" if giveaway_data.get(
        'role_id') else f"*{R.giveaway_no_role}*"

    prize = R.giveaway_prize % giveaway_data['prize']
    duration = R.giveaway_duration % format_duration(duration)
    role = R.giveaway_role % role_text
    winner_count = R.giveaway_winner_count % giveaway_data['winner_count']
    host = R.giveaway_host % mention(giveaway_data['host_id'])

    embed = discord.Embed(
        title=title,
        description=f"{prize}\n{duration}\n{role}\n{winner_count}\n{host}",
        color=color
    )

    return embed


async def end_giveaway(bot: discord.Bot, giveaway):
    """
    End a giveaway and select winners.
    Args:
        bot (discord.Bot): The Discord bot instance.
        giveaway: The giveaway object from the database.
    """
    try:
        channel = bot.get_channel(giveaway.channel_id)
        if not channel:
            logger.error(
                We(f"Channel {giveaway.channel_id} not found for giveaway {giveaway.message_id}"))
            # Mark as ended to prevent retries
            db.update_giveaway(giveaway.message_id, ended=True)
            return

        try:
            message = await channel.fetch_message(giveaway.message_id)
        except discord.NotFound:
            logger.error(
                We(f"Message {giveaway.message_id} not found for giveaway"))
            db.update_giveaway(giveaway.message_id, ended=True)
            return

        # Collect participants from reactions
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
            db.update_giveaway(giveaway.message_id, ended=True)
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
                            await member.add_roles(role, reason="Giveaway gewonnen")
                        except discord.Forbidden:
                            msg = R.giveaway_role_perms_error % (
                                role.mention, winner.mention)
                            await channel.send(embed=error_embed(msg))
                            logger.error(We(msg))

        # Mark as ended
        db.update_giveaway(giveaway.message_id, ended=True)
        logger.info(
            f"Giveaway {giveaway.message_id} ended with {len(winners)} winners")

    except Exception as e:
        logger.error(We(f"Error ending giveaway {giveaway.message_id}: {e}"))
        # Still mark as ended to prevent infinite retries
        db.update_giveaway(giveaway.message_id, ended=True)


def setup_giveaway_command(bot: discord.Bot):
    """
    Setup the giveaway command and background task for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """

    @bot.slash_command(name="giveaway", description=R.giveaway_desc)
    @discord.default_permissions(administrator=True)
    @discord.option(
        "dauer",
        description=R.giveaway_duration_desc,
        required=True
    )
    @discord.option(
        "preis",
        description=R.giveaway_prize_desc,
        required=True
    )
    @discord.option(
        "gewinner",
        description=R.giveaway_winners_desc,
        required=False,
        default=1,
        min_value=1,
        max_value=20
    )
    @discord.option(
        "rolle",
        description=R.giveaway_role_desc,
        required=False,
        default=None,
        type=discord.SlashCommandOptionType.role
    )
    async def giveaway_command(
        interaction: discord.Interaction,
        dauer: str,
        preis: str,
        gewinner: int = 1,
        rolle: discord.Role = None
    ):
        """
        Start a giveaway with automatic winner selection.
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
        db.create_giveaway(
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
        logger.info(
            f"Giveaway {message.id} started", interaction)

    @tasks.loop(seconds=C.giveaway_check_interval)
    async def check_giveaways():
        """
        Background task that checks for ended giveaways and processes them.
        """
        try:
            now = datetime.datetime.now()
            ended_giveaways = db.get_active_giveaways(now)

            for giveaway in ended_giveaways:
                await end_giveaway(bot, giveaway)

        except Exception as e:
            logger.error(We(f"Error in giveaway check task: {e}"))

    # Start the background task
    check_giveaways.start()
