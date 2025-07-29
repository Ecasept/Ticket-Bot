"""
This module provides a generalized way to display lists of items in embeds,
handling message splitting and providing an update button.
"""
import discord
from src.res import R
from src.constants import C
from src.error import Error, We
from typing import List, Tuple, Callable, Awaitable


def _split_message(message: str) -> tuple[list[str], None] | tuple[None, We]:
    """Splits a message into chunks that fit within the embed description limit."""
    split = []
    i = 0
    max_len = C.embed_desc_max_length - 10  # -10 to be safe
    while i < len(message):
        if i + max_len >= len(message):
            # The remaining part fits in one chunk
            next_index = len(message)
        else:
            # Find the last newline within the max length
            next_index = message.rfind("\n", i, i + max_len)
            if next_index == -1:
                # No newline found, message is too long
                return None, We(R.list_too_long)
            # next_index = i + max_len
        split.append(message[i:next_index])
        i = next_index + 1
    if len(split) > C.max_embeds:
        return None, We(R.list_too_long)
    if sum(len(s) for s in split) > C.embed_total_max_length:
        return None, We(R.list_too_long)

    return split, None


def create_list_embeds(title: str, items: List[Tuple[str, str]], empty_message: str) -> list[discord.Embed] | Error:
    """
    Create a list of embeds from a list of items.

    Args:
        title (str): The main title for the embed list.
        items (List[Tuple[str, str]]): A list of tuples, where each tuple is (item_title, item_content).
        empty_message (str): The message to display if there are no items.

    Returns:
        list[discord.Embed] | Error: The formatted embeds, or an Error if content is too large.
    """
    if not items:
        message = empty_message
    else:
        message = "\n\n".join(
            [f"{item_title}\n{item_content}" for (
                item_title, item_content) in items]
        )

    split, err = _split_message(message)
    if err:
        return err

    embeds = [discord.Embed(
        title=title if i == 0 else None,
        description=desc,
        color=C.embed_color
    ) for i, desc in enumerate(split)]

    return embeds


class ListDisplayView(discord.ui.View):
    """
    A generic view for displaying lists that can be updated.
    """

    def __init__(self, custom_id: str, update_callback: Callable[[discord.Interaction], Awaitable[None]]):
        super().__init__(timeout=None)
        self.update_callback = update_callback

        self.update_button = discord.ui.Button(
            label=R.update_button_label,
            style=discord.ButtonStyle.secondary,
            emoji=discord.PartialEmoji(name="🔄"),
            custom_id=custom_id
        )
        self.update_button.callback = self.update_callback
        self.add_item(self.update_button)
