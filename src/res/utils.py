from typing import Callable
import discord
from discord.ui.select import MISSING

from .res import R
from .log_helper import logger


def with_callback_factory(item):
    """
    Returns a function that takes a callback and adds it to the item.
    """
    def with_callback(callback: Callable[[discord.ui.Item, discord.Interaction], None]) -> discord.ui.Item:
        """Adds a callback to the item and returns it the item"""
        async def callback_wrapper(interaction: discord.Interaction):
            """A wrapper so that the callback receives both the item and the interaction."""
            await R.init(interaction.guild_id)
            return await callback(item, interaction)
        item.callback = callback_wrapper
        return item
    return with_callback


def button(
    label: str | None = None,
    custom_id: str | None = None,
    disabled: bool = False,
    style: discord.ButtonStyle = discord.ButtonStyle.secondary,
    emoji: str | discord.Emoji | discord.PartialEmoji | None = None,
    row: int | None = None,
):
    return with_callback_factory(
        discord.ui.Button(
            label=label,
            custom_id=custom_id,
            disabled=disabled,
            style=style,
            emoji=emoji,
            row=row
        )
    )


def select(
    select_type: discord.ComponentType = discord.ComponentType.string_select,
    placeholder: str | None = None,
    custom_id: str | None = None,
    min_values: int = 1,
    max_values: int = 1,
    options: list[discord.SelectOption] = MISSING,
    channel_types: list[discord.ChannelType] = MISSING,
    disabled: bool = False,
    row: int | None = None,
):
    return with_callback_factory(
        discord.ui.Select(
            select_type=select_type,
            placeholder=placeholder,
            custom_id=custom_id,
            min_values=min_values,
            max_values=max_values,
            options=options,
            channel_types=channel_types,
            disabled=disabled,
            row=row
        )
    )


def role_select(
    placeholder: str | None = None,
    custom_id: str | None = None,
    min_values: int = 1,
    max_values: int = 1,
    disabled: bool = False,
    row: int | None = None,
):

    return with_callback_factory(
        discord.ui.Select(
            select_type=discord.ComponentType.role_select,
            placeholder=placeholder,
            custom_id=custom_id,
            min_values=min_values,
            max_values=max_values,
            disabled=disabled,
            row=row
        )
    )


def channel_select(
    placeholder: str | None = None,
    custom_id: str | None = None,
    min_values: int = 1,
    max_values: int = 1,
    disabled: bool = False,
    channel_types: list[discord.ChannelType] = MISSING,
    row: int | None = None,
):
    return with_callback_factory(
        discord.ui.Select(
            select_type=discord.ComponentType.channel_select,
            placeholder=placeholder,
            custom_id=custom_id,
            min_values=min_values,
            max_values=max_values,
            disabled=disabled,
            channel_types=channel_types,
            row=row
        )
    )


def user_select(
    placeholder: str | None = None,
    custom_id: str | None = None,
    min_values: int = 1,
    max_values: int = 1,
    disabled: bool = False,
    row: int | None = None,
):
    return with_callback_factory(
        discord.ui.Select(
            select_type=discord.ComponentType.user_select,
            placeholder=placeholder,
            custom_id=custom_id,
            min_values=min_values,
            max_values=max_values,
            disabled=disabled,
            row=row
        )
    )


type Callback = Callable[[discord.ui.Button, discord.Interaction], None]
# A function that returns an item, but adds the given callback to it
type ItemCallbackCreator = Callable[[Callback], discord.ui.Button]
# A function that creates an item callback creator
type LateItemCallbackCreator = Callable[..., ItemCallbackCreator]


class InitView(discord.ui.View):
    """
    This view should be used in all views that require access to the resources.
    """
    @classmethod
    async def create(cls, interaction: discord.Interaction, *args, **kwargs):
        """
        Initialize the view with the interaction's guild ID.
        This is necessary to ensure that the resources are loaded correctly.
        """
        # Actually not necessary:
        # await R.init(interaction.guild_id)
        return cls(*args, **kwargs)


class LateView(InitView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in dir(self):
            if name.startswith("__"):
                continue
            attr = getattr(self, name)
            if callable(attr) and hasattr(attr, "__late_item_callback_creator"):
                logger().debug(
                    f"Late binding for {name} in {self.__class__.__name__}")
                func = attr
                button_callback_creator = getattr(
                    func, "__late_item_callback_creator")()
                button = button_callback_creator(func)
                self.add_item(button)


def late(creator: LateItemCallbackCreator):
    """
    If you directly annotate a function like this:
    ```
    @discord.ui.button(label=R.label)
    def bla(...): ...
    ```
    the resource string will be evaluated at definition time, not when the class is instantiated (at the time of the request).

    Instead, use this decorator like this:
    ```
    @late(lambda: button(label=R.label))
    def bla(...): ...
    ```

    The lambda creates a late binding closure, meaning that the resource string is evaluated 
    not at the definition, but when the lambda is called.
    When the lambda is called, `button` (or whichever function you use) will be called
    and create your button with the correct label.

    The `late` decorator ensures that the lambda (and therefore the button creation) is called on class instantiation, and not definition.
    This is only possible because you pass in a lambda which can be evaluated at class instantiation manually.

    Implementation detail:
    The `button` function (and other functions) does not actually return a button.
    It returns another function that takes a callback and returns a button with that callback.
    """
    def decorator(func: Callback):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__late_item_callback_creator = creator
        return wrapper
    return decorator
