"""
Timeout button interface for the ticket menu.
"""
import discord
from src.res import R
from src.res.utils import late, button, select, LateView, user_select
from src.constants import C
from src.utils import create_embed, logger
from src.features.timeout.timeout import timeout_user


class TimeoutSelectView(LateView):
    def __init__(self):
        super().__init__(timeout=300)
        self.selected_user = None
        self.selected_duration = None
        self.reason = None

    @late(lambda: user_select(
        placeholder=R.timeout_user_select_placeholder,
        min_values=1,
        max_values=1,
    ))
    async def user_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.selected_user = select.values[0]
        await interaction.response.defer()

    @late(lambda: select(
        placeholder=R.timeout_duration_select_placeholder,
        options=[
            discord.SelectOption(
                label=R.timeout_30s_label,
                description=R.timeout_30s_desc,
                value="30s",
                emoji="⏱️"
            ),
            discord.SelectOption(
                label=R.timeout_5m_label,
                description=R.timeout_5m_desc,
                value="5m",
                emoji="⏰"
            ),
            discord.SelectOption(
                label=R.timeout_1h_label,
                description=R.timeout_1h_desc,
                value="1h",
                emoji="🕐"
            ),
            discord.SelectOption(
                label=R.timeout_1d_label,
                description=R.timeout_1d_desc,
                value="1d",
                emoji="📅"
            ),
            discord.SelectOption(
                label=R.timeout_1w_label,
                description=R.timeout_1w_desc,
                value="1w",
                emoji="📆"
            )
        ]
    ))
    async def duration_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.selected_duration = select.values[0]
        await interaction.response.defer()

    @late(lambda: button(
        label=R.timeout_execute_button,
        style=discord.ButtonStyle.danger,
        emoji="⏰"
    ))
    async def execute_timeout_callback(self, button, interaction: discord.Interaction):
        if not self.selected_user:
            await interaction.response.send_message(
                embed=create_embed(
                    R.timeout_select_user_error, color=C.error_color),
                ephemeral=True
            )
            return

        if not self.selected_duration:
            await interaction.response.send_message(
                embed=create_embed(
                    R.timeout_select_duration_error, color=C.error_color),
                ephemeral=True
            )
            return

        # Convert user to member if needed
        if isinstance(self.selected_user, discord.User):
            member = interaction.guild.get_member(self.selected_user.id)
            if not member:
                await interaction.response.send_message(
                    embed=create_embed(
                        R.timeout_user_not_on_server, color=C.error_color),
                    ephemeral=True
                )
                return
        else:
            member = self.selected_user

        await timeout_user(interaction, member, self.selected_duration, self.reason)
        self.stop()

    @late(lambda: button(
        label=R.timeout_cancel_button,
        style=discord.ButtonStyle.secondary,
        emoji="❌"
    ))
    async def cancel_callback(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=create_embed(R.timeout_cancelled, color=C.warning_color),
            view=None
        )
        self.stop()


class TimeoutButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label=R.ticket_menu_timeout,
            style=discord.ButtonStyle.secondary,
            emoji="⏰",
            custom_id="ticket_menu_timeout"
        )

    async def callback(self, interaction: discord.Interaction):
        await R.init(interaction.guild_id)
        embed = create_embed(
            R.timeout_interface_description,
            title=R.timeout_interface_title,
            color=C.embed_color
        )
        view = TimeoutSelectView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info("Timeout select menu opened", interaction)
