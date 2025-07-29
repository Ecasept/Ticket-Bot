"""
Setup button interface for the ticket menu.
"""
import discord
from src.res import R, lang_info
from src.res.utils import LateView, late, button, select, role_select, channel_select
from src.constants import C
from src.utils import create_embed, logger
from src.database import db
from src.features.setup.setup import (
    setup_tickets, setup_transcript, setup_logchannel,
    setup_timeout_logchannel, show_modroles, setup_language
)
from src.res.utils import LateView, late, button, channel_select, role_select, select


class SetupOptionView(LateView):
    def __init__(self, option):
        super().__init__(timeout=300)
        self.option = option

    @late(lambda: button(
        label=R.setup_view_value,
        style=discord.ButtonStyle.secondary,
        emoji="👁️"
    ))
    async def view_value_callback(self, button, interaction: discord.Interaction):
        if self.option == "tickets":
            await setup_tickets(interaction)
        elif self.option == "transcript":
            await setup_transcript(interaction)
        elif self.option == "logchannel":
            await setup_logchannel(interaction)
        elif self.option == "timeout_logchannel":
            await setup_timeout_logchannel(interaction)
        elif self.option == "modroles":
            await show_modroles(interaction)
        elif self.option == "language":
            await setup_language(interaction)

        logger.info(f"Viewed setup option {self.option}", interaction)

    @late(lambda: button(
        label=R.setup_set_value,
        style=discord.ButtonStyle.primary,
        emoji="✏️"
    ))
    async def set_value_callback(self, button, interaction: discord.Interaction):
        if self.option == "tickets":
            await self._set_tickets(interaction)
        elif self.option == "transcript":
            await self._set_transcript(interaction)
        elif self.option == "logchannel":
            await self._set_logchannel(interaction)
        elif self.option == "timeout_logchannel":
            await self._set_timeout_logchannel(interaction)
        elif self.option == "modroles":
            await self._set_modroles(interaction)
        elif self.option == "language":
            await self._set_language(interaction)

        logger.info(f"Setting setup option {self.option}", interaction)

    async def _set_tickets(self, interaction: discord.Interaction):
        class CategorySelectView(LateView):
            def __init__(self):
                super().__init__(timeout=120)

            @late(lambda: channel_select(
                placeholder=R.setup_tickets_select_placeholder,
                channel_types=[discord.ChannelType.category]
            ))
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                category = select.values[0]
                await setup_tickets(interaction, category)
                self.stop()

        view = CategorySelectView()
        await interaction.response.send_message(
            embed=create_embed(R.feature.setup.button.set_tickets.embed_desc,
                               title=R.feature.setup.button.set_tickets.embed_title),
            view=view,
            ephemeral=True
        )

    async def _set_transcript(self, interaction: discord.Interaction):
        class CategorySelectView(LateView):
            def __init__(self):
                super().__init__(timeout=120)

            @late(lambda: channel_select(
                placeholder=R.setup_transcript_select_placeholder,
                channel_types=[discord.ChannelType.category]
            ))
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                category = select.values[0]
                await setup_transcript(interaction, category)
                self.stop()

        view = CategorySelectView()
        await interaction.response.send_message(
            embed=create_embed(
                R.feature.setup.button.set_transcript.embed_desc, title=R.feature.setup.button.set_transcript.embed_title),
            view=view,
            ephemeral=True
        )

    async def _set_logchannel(self, interaction: discord.Interaction):
        class ChannelSelectView(LateView):
            def __init__(self):
                super().__init__(timeout=120)

            @late(lambda: channel_select(
                placeholder=R.setup_logchannel_select_placeholder,
                channel_types=[discord.ChannelType.text]
            ))
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                channel = select.values[0]
                await setup_logchannel(interaction, channel)
                self.stop()

        view = ChannelSelectView()
        await interaction.response.send_message(
            embed=create_embed(R.feature.setup.button.set_logchannel.embed_desc,
                               title=R.feature.setup.button.set_logchannel.embed_title),
            view=view,
            ephemeral=True
        )

    async def _set_timeout_logchannel(self, interaction: discord.Interaction):
        class ChannelSelectView(LateView):
            def __init__(self):
                super().__init__(timeout=120)

            @late(lambda: channel_select(
                placeholder=R.setup_timeout_logchannel_select_placeholder,
                channel_types=[discord.ChannelType.text]
            ))
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                channel = select.values[0]
                await setup_timeout_logchannel(interaction, channel)
                self.stop()

        view = ChannelSelectView()
        await interaction.response.send_message(
            embed=create_embed(R.feature.setup.button.set_timeout_logchannel.embed_desc,
                               title=R.feature.setup.button.set_timeout_logchannel.embed_title),
            view=view,
            ephemeral=True
        )

    async def _set_modroles(self, interaction: discord.Interaction):
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
                    return
                # Save selected roles as comma-separated IDs
                role_ids = [str(role.id) for role in self.selected_roles]
                db.constant.set(C.DBKey.mod_roles, ",".join(
                    role_ids), interaction.guild.id)
                roles_mentions = ", ".join(
                    [role.mention for role in self.selected_roles])
                await interaction.response.edit_message(
                    embed=create_embed(R.setup_modroles_set % roles_mentions,
                                       color=C.success_color, title=R.mod_roles_title),
                    view=None
                )
                self.stop()

        view = ModRolesSelectView()
        await interaction.response.send_message(
            embed=create_embed(R.setup_modroles_select_prompt,
                               title=R.mod_roles_title),
            view=view,
            ephemeral=True
        )

    async def _set_language(self, interaction: discord.Interaction):
        class LanguageSelectView(LateView):
            def __init__(self):
                super().__init__(timeout=120)

            @late(lambda: select(
                placeholder=R.command.setup.language.option.language_desc,
                options=[
                    discord.SelectOption(
                        label=item["native_name"],
                        value=item["code"],
                        emoji=item["emoji"],
                    ) for item in lang_info
                ]
            ))
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                language = select.values[0]
                await setup_language(interaction, language)
                self.stop()

        view = LanguageSelectView()
        await interaction.response.send_message(
            embed=create_embed(R.command.setup.language.option.language_desc,
                               title=R.command.setup.language.name),
            view=view,
            ephemeral=True
        )


class SetupSelectView(LateView):
    def __init__(self):
        super().__init__(timeout=300)

    @late(lambda: select(
        placeholder=R.setup_select_option_placeholder,
        options=[
            discord.SelectOption(
                label=R.feature.setup.button.option_view.option_name_tickets,
                description=R.command.setup.tickets.desc,
                value="tickets",
                emoji="🎫"
            ),
            discord.SelectOption(
                label=R.feature.setup.button.option_view.option_name_transcript,
                description=R.command.setup.transcript.desc,
                value="transcript",
                emoji="📜"
            ),
            discord.SelectOption(
                label=R.feature.setup.button.option_view.option_name_logchannel,
                description=R.command.setup.logchannel.desc,
                value="logchannel",
                emoji="📝"
            ),
            discord.SelectOption(
                label=R.feature.setup.button.option_view.option_name_timeout_logchannel,
                description=R.command.setup.timeoutlogchannel.desc,
                value="timeout_logchannel",
                emoji="⏰"
            ),
            discord.SelectOption(
                label=R.feature.setup.button.option_view.option_name_modroles,
                description=R.command.setup.modroles.desc,
                value="modroles",
                emoji="👮"
            ),
            discord.SelectOption(
                label=R.feature.setup.button.option_view.option_name_language,
                description=R.command.setup.language.desc,
                value="language",
                emoji="🌐"
            )
        ]
    ))
    async def setup_select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        option = select.values[0]

        # Show the new interface with Set Value and View Value buttons
        option_names = {
            "tickets": R.feature.setup.button.option_view.option_name_tickets,
            "transcript": R.feature.setup.button.option_view.option_name_transcript,
            "logchannel": R.feature.setup.button.option_view.option_name_logchannel,
            "timeout_logchannel": R.feature.setup.button.option_view.option_name_timeout_logchannel,
            "modroles": R.feature.setup.button.option_view.option_name_modroles,
            "language": R.feature.setup.button.option_view.option_name_language
        }

        embed = create_embed(
            R.feature.setup.button.option_view.embed_desc % option_names[option],
            title=R.feature.setup.button.option_view.embed_title,
            color=C.embed_color
        )
        view = SetupOptionView(option)
        await interaction.response.edit_message(embed=embed, view=view)

        logger.info(f"Setup option {option} selected", interaction)


class SetupButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label=R.ticket_menu_setup,
            style=discord.ButtonStyle.secondary,
            emoji="⚙️",
            custom_id="ticket_menu_setup"
        )

    async def callback(self, interaction: discord.Interaction):
        embed = create_embed(
            R.feature.setup.button.select_view.embed_desc,
            title=R.feature.setup.button.select_view.embed_title,
            color=C.embed_color
        )
        view = SetupSelectView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        logger.info("Setup select menu opened", interaction)
