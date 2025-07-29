"""
Giveaway button interface for the ticket menu.
"""
import discord
from src.res import R
from src.constants import C
from src.res.utils import LateView, late, select, role_select, button
from src.utils import create_embed, logger
from src.features.giveaway.giveaway import create_giveaway


class GiveawayConfigView(LateView):
    def __init__(self):
        super().__init__(timeout=300)
        self.selected_duration = None
        self.prize = None
        self.winner_count = 1
        self.selected_role = None

    @late(lambda: select(
        placeholder=R.giveaway_duration_select_placeholder,
        options=[
            discord.SelectOption(
                label=R.giveaway_duration_30s_label,
                description=R.giveaway_duration_30s_desc,
                value="30s",
                emoji="⚡"
            ),
            discord.SelectOption(
                label=R.giveaway_duration_5m_label,
                description=R.giveaway_duration_5m_desc,
                value="5m",
                emoji="⏱️"
            ),
            discord.SelectOption(
                label=R.giveaway_duration_1h_label,
                description=R.giveaway_duration_1h_desc,
                value="1h",
                emoji="⏰"
            ),
            discord.SelectOption(
                label=R.giveaway_duration_1d_label,
                description=R.giveaway_duration_1d_desc,
                value="1d",
                emoji="📅"
            ),
            discord.SelectOption(
                label=R.giveaway_duration_1w_label,
                description=R.giveaway_duration_1w_desc,
                value="1w",
                emoji="📆"
            )
        ]
    ))
    async def duration_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.selected_duration = select.values[0]
        await interaction.response.defer()

    @late(lambda: select(
        placeholder=R.giveaway_winner_count_select_placeholder,
        options=[
            discord.SelectOption(
                label=R.giveaway_winner_1_label, value="1", emoji="🥇"),
            discord.SelectOption(
                label=R.giveaway_winner_2_label, value="2", emoji="🥈"),
            discord.SelectOption(
                label=R.giveaway_winner_3_label, value="3", emoji="🥉"),
            discord.SelectOption(
                label=R.giveaway_winner_5_label, value="5", emoji="🏆"),
            discord.SelectOption(
                label=R.giveaway_winner_10_label, value="10", emoji="🎊")
        ]
    ))
    async def winner_count_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.winner_count = int(select.values[0])
        await interaction.response.defer()

    @late(lambda: role_select(
        placeholder=R.giveaway_role_select_placeholder,
        min_values=0,
        max_values=1,
    ))
    async def role_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.selected_role = select.values[0] if select.values else None
        await interaction.response.defer()

    @late(lambda: button(
        label=R.giveaway_set_prize_button,
        style=discord.ButtonStyle.primary,
        emoji="🎁"
    ))
    async def set_prize_callback(self, button, interaction: discord.Interaction):
        class PrizeModal(discord.ui.Modal):
            def __init__(self, parent_view):
                super().__init__(title=R.feature.giveaway.button.prize_modal.title)
                self.parent_view = parent_view

                self.add_item(discord.ui.InputText(
                    label=R.feature.giveaway.button.prize_modal.label,
                    placeholder=R.feature.giveaway.button.prize_modal.placeholder,
                    required=True,
                    max_length=256
                ))

            async def callback(self, interaction: discord.Interaction):
                self.parent_view.prize = self.children[0].value
                await interaction.response.send_message(
                    embed=create_embed(
                        R.feature.giveaway.button.prize_set_success % self.parent_view.prize, color=C.success_color),
                    ephemeral=True
                )

        modal = PrizeModal(self)
        await interaction.response.send_modal(modal)

    @late(lambda: button(
        label=R.giveaway_start_button,
        style=discord.ButtonStyle.success,
        emoji="🎉"
    ))
    async def start_giveaway_callback(self, button, interaction: discord.Interaction):
        if not self.selected_duration:
            await interaction.response.send_message(
                embed=create_embed(
                    R.feature.giveaway.button.no_duration_error, color=C.error_color),
                ephemeral=True
            )
            return

        if not self.prize:
            await interaction.response.send_message(
                embed=create_embed(
                    R.feature.giveaway.button.no_prize_error, color=C.error_color),
                ephemeral=True
            )
            return

        await create_giveaway(interaction, self.selected_duration, self.prize, self.winner_count, self.selected_role)
        self.stop()

    @late(lambda: button(
        label=R.giveaway_cancel_button,
        style=discord.ButtonStyle.secondary,
        emoji="❌"
    ))
    async def cancel_callback(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(
            embed=create_embed(R.feature.giveaway.button.cancelled_msg,
                               color=C.warning_color),
            view=None
        )
        self.stop()


class GiveawayButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label=R.ticket_menu_giveaway,
            style=discord.ButtonStyle.primary,
            emoji="🎉",
            custom_id="ticket_menu_giveaway"
        )

    async def callback(self, interaction: discord.Interaction):
        embed = create_embed(
            R.feature.giveaway.button.config_embed_desc,
            title=R.feature.giveaway.button.config_embed_title,
            color=C.embed_color
        )
        embed.add_field(
            name=R.feature.giveaway.button.config_embed_steps_name,
            value=R.feature.giveaway.button.config_embed_steps_value,
            inline=False
        )
        view = GiveawayConfigView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info("Giveaway config menu opened", interaction)
