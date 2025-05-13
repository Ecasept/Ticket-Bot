from typing import Type
import discord
from utils import logger


class DynamicPersistentView(discord.ui.View):
    """A view that can be used to create dynamic components.
    A dynamic component is a component that can store state
    in the custom_id.
    """

    def __init__(self, view_id, *args):
        super().__init__(timeout=None)
        self.data = view_id + ":" + ":".join(args)

    def add_item(self, item: discord.ui.Item):
        item.custom_id = self.data + ":" + item.custom_id
        super().add_item(item)

    async def resolve(self, interaction: discord.Interaction, id: str):
        for item in self.children:
            if item.custom_id.split(":")[-1] == id:
                await item.callback(interaction)
                break


def add_dynamic_view(view: Type[DynamicPersistentView]):
    """Register a dynamic view"""
    if not issubclass(view, DynamicPersistentView):
        raise TypeError("view must be a subclass of DynamicPersistentView")
    _dynamic_views.append(view)


_dynamic_views: list[Type[DynamicPersistentView]] = []


async def resolve_interaction(interaction: discord.Interaction):
    """Will try finding a dynamic view for the interaction."""
    if interaction.type == discord.InteractionType.component:
        parts = interaction.custom_id.split(":")
        view_id = parts[0]
        data = parts[1:-1]
        component_id = parts[-1]
        for view in _dynamic_views:
            if view.view_id == view_id:
                logger.debug(
                    f"Dynamic view interaction: {interaction.custom_id}")
                # Create a new instance of the view
                new_view = view(*data)
                await new_view.resolve(interaction, component_id)
                break
        else:
            logger.debug(
                f"Non-dynamic view interaction: {interaction.custom_id}")
