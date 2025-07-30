import asyncio
import dataclasses
import threading
from typing import Annotated, Type
from src.constants import C
from enum import Enum
from .lang.de import ResDE
from .lang.en import ResEN
from .log_helper import logger

task_locales: dict[int, str] = {}
tglock = threading.Lock()

# List of valid discord locales:
# https://discord.com/developers/docs/reference#locales
locale_mapping = {
    "de": ResDE,
    "en-US": ResEN,
}

lang_info = [
    {
        "code": "de",
        "native_name": "Deutsch",
        "emoji": "🇩🇪",
    },
    {
        "code": "en-US",
        "native_name": "English",
        "emoji": "🇺🇸",
    }
]

DEFAULT_LANG = "de"


class RMode(Enum):
    NORMAL = 1
    DEFAULT_LANG = 2
    LOCALIZED = 3


class LocaleDictionary(dict):
    def __getattr__(self, item):
        first_value = next(iter(self.values()), None)
        if hasattr(first_value, item):
            # User is trying to access a subattribute of the resource strings
            # eg. if this is the locale dict for R.feature, they might try to access R.feature.giveaway
            return LocaleDictionary({lang_code: getattr(res_class, item)
                                     for lang_code, res_class in self.items()})
        else:
            return super().__getattr__(item)


UNIQUE = object()


class LocaleObject(object):
    def __init__(self, obj: object, path: str):
        self.obj = obj
        self.path = path

    def __getattr__(self, item):
        attr = getattr(self.obj, item, UNIQUE)
        if attr is UNIQUE:
            # If the attribute does not exist, return a placeholder
            logger().warning(
                f"Resource '{self.path}.{item}' not found, returning LocaleUnknownString")
            return LocaleUnknownString(f"{self.path}.{item}")
        if dataclasses.is_dataclass(attr):
            # If this is a further subgroup
            return LocaleObject(attr, f"{self.path}.{item}")
        else:
            # If we reached the end, log the attribute access
            logger().debug(f"Accessing resource '{self.path}.{item}'")
            return attr


class LocaleUnknownString(str):
    """
    This class is used to represent a path with no associated resource string.
    """

    def __init__(self, path: str):
        self.path = path

    def __getattr__(self, item):
        self.path += f".{item}"
        return self

    def __str__(self):
        return self.path

    def __repr__(self):
        return f"LocaleUnknownString({self.path})"


class Resources:
    def __init__(self, mode: RMode):
        """
        Initialize the Resources class.
        If `default` is True, this instance will be used for decorators
        and will not require initialization with a guild ID.
        """
        self.mode = mode

    async def initlocale(self, locale: str):
        return await self._set_locale(locale)

    async def init(self, guild_id: int):
        """
        Call this method before the `R` object is used in a task
        to configure the locale for resources for this task.
        The locale will be retrieved based on the guild's settings.
        Can be called multiple times to switch the guild/locale used by the task.
        """

        from src.database import db

        # Get the locale configured for this guild
        locale = db.constant.get(C.DBKey.locale, guild_id)
        if locale is None:
            locale = DEFAULT_LANG

        return await self._set_locale(locale)

    async def _set_locale(self, locale: str):
        if self.mode != RMode.NORMAL:
            raise RuntimeError(
                "Can only set locale in NORMAL mode"
            )
        if locale not in locale_mapping:
            # Unknown or unsupported locale
            locale = DEFAULT_LANG

        # Get id of this asyncio task
        current_task = asyncio.current_task()
        _id = id(current_task)

        logger().debug(
            f"Initializing resources for task {_id} with locale '{locale}'"
        )

        # Store the locale for this task
        with tglock:
            task_locales[_id] = locale

        # When the task finishes, its id might be reused,
        # so we need to remove it from the task_locales dict
        current_task.add_done_callback(
            self._create_on_task_finished(_id)
        )

    def _create_on_task_finished(self, _id: int):
        def _on_task_finished(task: asyncio.Task):
            with tglock:
                task_locales.pop(_id, None)
        return _on_task_finished

    def __getattr__(self, item):
        if self.mode == RMode.DEFAULT_LANG:
            # If this is the default resources instance,
            # we don't need to check the task id
            res_class = locale_mapping.get(DEFAULT_LANG, ResDE)
            return getattr(res_class, item)
        elif self.mode == RMode.LOCALIZED:
            # Return all strings in a dictionary format
            # See https://guide.pycord.dev/interactions/application-commands/localizations
            return LocaleDictionary({
                lang_code: getattr(res_class, item)
                for lang_code, res_class in locale_mapping.items()
            })

        # Get the current task id
        try:
            current_task = asyncio.current_task()
            _id = id(current_task)
        except RuntimeError:
            # No running event loop
            # Use a default id for the main thread
            from src.error import Ce
            logger().error(Ce("Cannot access resources outside of an asyncio task. ", title="a"))
            _id = 0

        # Get the locale for this task
        with tglock:
            locale = task_locales.get(_id, DEFAULT_LANG)

        # Get the resource class for the locale
        res_class = locale_mapping.get(locale, locale_mapping[DEFAULT_LANG])

        # Return the attribute from the resource class
        lo = LocaleObject(res_class, "R")
        return getattr(lo, item)


class TResource(ResDE):
    """
    The Type of the resources class.
    This is used so that the resource strings appear
    during autocomplete, as normally the attribute
    access would go over the `__getattr__` method.
    """

    async def init(self, guild_id: int) -> None: ...
    async def initlocale(self, locale: str) -> None: ...


# Following classes are used to provide docstrings for the resource objects

class Resource(TResource):
    """
    This global resource object is used to access
    the resource strings in the code. If not used in an interaction,
    where the guild_id is set by default, it must be set manually
    with `await R.init(guild_id)` before accessing any resource strings.
    """
    pass


class ResourceDefault(TResource):
    """
    This resource object is used to provide default resources
    for places where the guild_id is not available, such as decorators.
    It does not require initialization with a guild_id.

    Should be used eg. when a resource needs to be accessed at "compile time"
    instead of when a request with an associated guild is made.
    """
    pass


class ResourceLocalizations(TResource):
    """
    This resource object returns a special dictionary
    that contains all resource strings in the format required
    by pycord to provide localized strings in the discord client.
    """


R: Type[Resource] = Resources(RMode.NORMAL)
RD: Type[ResourceDefault] = Resources(RMode.DEFAULT_LANG)
RL: Type[ResourceLocalizations] = Resources(RMode.LOCALIZED)
