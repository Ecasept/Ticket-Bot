from src.res import R
import traceback

type Error = CriticalError | WarningError


class CriticalError():
    """
    Represents an error that is unexpected and may hint at a bug in the code.

    Args:
        message (str): The error message to display.
        title (str): The title for the error embed. Defaults to R.error_title.
    """

    def __init__(self, message: str, title: str = R.error_title):
        self.message = message
        self.title = title
        self.show_traceback = True
        self.stack = traceback.extract_stack()


class WarningError():
    """
    Represents an error that can occur during normal operation, such as user input errors.

    Args:
        message (str): The warning message to display.
        title (str): The title for the warning embed. Defaults to R.error_title.
    """

    def __init__(self, message: str, title: str = R.error_title):
        self.message = message
        self.title = title
        self.show_traceback = False
        self.stack = traceback.extract_stack()


# Shortcuts for error types
Ce = CriticalError
We = WarningError
