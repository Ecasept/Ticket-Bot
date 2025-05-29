"""
Help command module for the Discord bot. Provides an overview of all available commands.
"""
import discord
from src.utils import logger
from src.res import C, R


def setup_help_command(bot: discord.Bot):
    """
    Setup the help command for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """

    @bot.slash_command(name="help", description=R.help_desc)
    async def help_command(ctx: discord.ApplicationContext):
        """
        Display all available bot commands in an organized embed.
        Args:
            ctx (discord.ApplicationContext): The interaction context.
        """
        embed = discord.Embed(
            title=R.help_title,
            description=R.help_description,
            color=C.embed_color
        )

        # General Commands section
        general_commands = [
            "- `/ping` - " + R.ping_desc,
            "- `/help` - " + R.help_desc,
            "- `/createpanel` - " + R.ticket_msg_desc + " *(Administrator)*",
            "- `/giveaway` - " + R.giveaway_desc + " *(Administrator)*"
        ]

        embed.add_field(
            name=R.help_general_commands,
            value="\n".join(general_commands),
            inline=False
        )

        # Setup Commands section
        setup_commands = [
            "- `/setup tickets [category]` - " + R.setup_tickets_desc,
            "- `/setup transcript [category]` - " + R.setup_transcript_desc,
            "- `/setup logchannel [channel]` - " + R.setup_logchannel_desc,
            "- `/setup modroles` - " + R.setup_modroles_desc
        ]

        embed.add_field(
            name=R.help_setup_commands,
            value="\n".join(setup_commands),
            inline=False
        )

        # Team Commands section
        team_commands = [
            "- `/team add <user> <role>` - " + R.team_add_desc,
            "- `/team remove <user> <role>` - " + R.team_remove_desc,
            "- `/team wechsel <user> <von> <zu>` - " + R.team_wechsel_desc,
            "- `/team list` - " + R.team_list_desc
        ]

        embed.add_field(
            name=R.help_team_commands,
            value="\n".join(team_commands),
            inline=False
        )

        # Tutorial section
        embed.add_field(
            name=R.help_tutorial_title,
            value=R.help_tutorial_text,
            inline=False
        )

        # Add footer
        embed.set_footer(text=R.help_footer)

        await ctx.respond(embed=embed, ephemeral=True)
        logger.info("Help command executed", ctx.interaction)
