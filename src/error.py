from typing import Type
from src.res import R
import traceback


class Error:
    """Base class for errors."""

    def __init__(self, message: str, title: str = R.error_title, show_traceback: bool = False):
        self.message = message
        self.title = title
        self.show_traceback = show_traceback
        self.stack = traceback.extract_stack()

    def iserr(self, error_type: Type['Error']) -> bool:
        """
        Check if the current error is of a specific type.

        Args:
            error_type (Type[Error]): The type to check against.

        Returns:
            bool: True if the current error is of the specified type, False otherwise.
        """
        return isinstance(self, error_type)


class CriticalError(Error):
    """
    Represents an error that is unexpected and may hint at a bug in the code.

    Args:
        message (str): The error message to display.
        title (str): The title for the error embed. Defaults to R.error_title.
    """

    def __init__(self, message: str, title: str = R.error_title):
        super().__init__(message, title, show_traceback=True)


class UserNotFoundError(Error):
    def __init__(self, user_id: int, title: str = R.error_title):
        message = R.user_not_found % user_id
        super().__init__(message, title, show_traceback=False)


class WarningError(Error):
    """
    Represents an error that can occur during normal operation, such as user input errors.

    Args:
        message (str): The warning message to display.
        title (str): The title for the warning embed. Defaults to R.error_title.
    """

    def __init__(self, message: str, title: str = R.error_title):
        super().__init__(message, title, show_traceback=False)


# Shortcuts for error types
Ce = CriticalError
We = WarningError
