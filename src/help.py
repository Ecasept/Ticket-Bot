"""
Help command module for the Discord bot. Provides an overview of all available commands.
"""
import discord
from src.utils import MODE, logger
from src.constants import C
from src.res import R, RD, RL


def setup_help_command(bot: discord.Bot):
    """
    Setup the help command for the bot.
    Args:
        bot (discord.Bot): The Discord bot instance.
    """

    @bot.slash_command(
        name=RD.command.help.name,
        name_localizations=RL.command.help.name,
        description=RD.command.help.desc,
        description_localizations=RL.command.help.desc
    )
    async def help_command(ctx: discord.ApplicationContext):
        """
        Display all available bot commands in an organized embed.
        Args:
            ctx (discord.ApplicationContext): The interaction context.
        """
        # The command names change based on locale name so here we want resource strings for the user locale
        await R.initlocale(ctx.locale)
        embed = discord.Embed(
            title=R.help_title,
            description=R.help_description,
            color=C.embed_color
        )
        if MODE == "tickets" or MODE == "all":
            # General Commands section
            general_commands = [
                f"- `/{R.command.ping.name}` - " + R.command.ping.desc,
                f"- `/{R.command.help.name}` - " + R.command.help.desc,
                f"- `/{R.command.ticket.name}` - " +
                R.command.ticket.desc + " *(Administrator)*",
                f"- `/{R.command.createpanel.name}` - " + R.command.createpanel.desc +
                " *(Administrator)*",
                f"- `/{R.command.giveaway.name}` - " +
                R.command.giveaway.desc + " *(Administrator)*",
                f"- `/{R.command.timeout.name}` - " +
                R.command.timeout.desc + " *(Moderator)*",
                f"- `/{R.command.category.name}` - {R.command.category.desc} *(Administrator)*",
            ]

            embed.add_field(
                name=R.help_general_commands,
                value="\n".join(general_commands),
                inline=False
            )

            # Setup Commands section
            setup_commands = [
                f"- `/{R.command.setup.name} {R.command.setup.tickets.name}` - " +
                R.command.setup.tickets.desc,
                f"- `/{R.command.setup.name} {R.command.setup.transcript.name}` - " +
                R.command.setup.transcript.desc,
                f"- `/{R.command.setup.name} {R.command.setup.logchannel.name}` - " +
                R.command.setup.logchannel.desc,
                f"- `/{R.command.setup.name} {R.command.setup.modroles.name}` - " +
                R.command.setup.modroles.desc,
                f"- `/{R.command.setup.name} {R.command.setup.timeoutlogchannel.name}` - " +
                R.command.setup.timeoutlogchannel.desc,
            ]

            embed.add_field(
                name=R.help_setup_commands,
                value="\n".join(setup_commands),
                inline=False
            )

        if MODE == "team" or MODE == "all":
            # Team Commands section
            team_commands = [
                f"- `/{R.command.team.name} {R.command.team.add.name}` - " +
                R.command.team.add.desc,
                f"- `/{R.command.team.name} {R.command.team.remove.name}` - " +
                R.command.team.remove.desc,
                f"- `/{R.command.team.name} {R.command.team.wechsel.name}` - " +
                R.command.team.wechsel.desc,
                f"- `/{R.command.team.name} {R.command.team.list.name}` - " +
                R.command.team.list.desc,
                f"- `/{R.command.team.name} {R.command.team.sperre.name}` - " +
                R.command.team.sperre.desc
            ]

            embed.add_field(
                name=R.help_team_commands,
                value="\n".join(team_commands),
                inline=False
            )

        if MODE == "tickets" or MODE == "all":
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
