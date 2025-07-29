"""
Simple logging utility for the bot, supporting different log levels and file output.
"""
from dataclasses import dataclass
import datetime
import traceback

import discord
from src.error import Error

# ANSI escape sequences for colored output


@dataclass
class Col:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    ORANGE = "\033[38;5;208m"
    RESET = "\033[0m"

    @dataclass
    class BG:
        RED = "\033[41m"
        GREEN = "\033[42m"
        YELLOW = "\033[43m"
        BLUE = "\033[44m"
        MAGENTA = "\033[45m"
        CYAN = "\033[46m"
        WHITE = "\033[47m"
        ORANGE = "\033[48;5;208m"


class Logger:
    """
    Logger class for writing log messages to a file and printing them to stdout.
    """

    def __init__(self, filename: str):
        """
        Initialize the Logger.
        Args:
            filename (str): Path to the log file.
        """
        self.filename = filename

    def _format_frame(self, frame: traceback.FrameSummary) -> str:
        """
        Format a single frame from the stack trace.
        Args:
            frame (traceback.FrameSummary): The frame to format.
        Returns:
            str: Formatted string of the frame.
        """
        filename = frame.filename.split("/")[-1].replace(".py", "")
        lno = frame.lineno
        func = frame.name
        return f"{filename}:{lno}:{func}"

    def _get_formatted_stack(self, stacksum: traceback.StackSummary) -> list[str]:
        """
        Format a stack trace summary into a list of formatted frame strings.
        Args:
            stacksum (traceback.StackSummary): The stack summary to format.
        Returns:
            list[str]: List of formatted frame strings.
        """
        formatted_stack = []
        for frame in stacksum:
            # Skip if the frame is from the logging function itself
            if frame.filename.endswith("log.py"):
                continue
            # Skip frames that are part of the error handling
            if frame.name == "handle_error":
                continue
            if frame.filename.endswith("error.py"):
                continue
            formatted_stack.append(self._format_frame(frame))
        return formatted_stack

    def _get_interaction_info(self, interaction: discord.Interaction | None) -> str:
        """
        Get formatted interaction information if available.
        Args:
            interaction (discord.Interaction | None): The interaction context.
        Returns:
            str: Formatted interaction information.
        """
        if interaction:
            user_id = str(interaction.user.id)
            user_name = interaction.user.name
            guild_id = str(
                interaction.guild.id) if interaction.guild else "None"
            guild_name = interaction.guild.name if interaction.guild else "None"
            channel_id = str(
                interaction.channel.id) if interaction.channel else "None"
            channel_name = interaction.channel.name if interaction.channel else "None"
            return f" {{{user_name}/{user_id} in {guild_name}/{guild_id} #{channel_name}/{channel_id}}}"
        return ""

    def _log(self, level: str, message: str, interaction: discord.Interaction | None, stack: traceback.StackSummary, extended_traceback: bool = False) -> None:
        """
        Core logging method that formats and outputs log messages.
        Args:
            level (str): The log level (DEBUG, INFO, WARNING, ERROR).
            message (str): The message to log.
            interaction (discord.Interaction | None): Optional interaction context.
            stack (traceback.StackSummary): The stack trace information.
            extended_traceback (bool): Whether to include full traceback. Defaults to False.
        """
        formatted_stack = self._get_formatted_stack(stack)
        location = formatted_stack[-1] if formatted_stack else "unknown"
        interaction_info = self._get_interaction_info(interaction)

        now = datetime.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M:%S")

        msg = f"{t} [{level}] <{location}> {message}{interaction_info}\n"
        level_color = {
            "DEBUG": Col.CYAN,
            "INFO": Col.GREEN,
            "WARNING": Col.YELLOW,
            "ERROR": Col.RED
        }.get(level, Col.WHITE)
        # Color the individual parts of the log message
        msg_colored = (
            f"{Col.WHITE}{t} {Col.RESET}"
            f"{level_color}[{level}]{Col.RESET} "
            f"{Col.MAGENTA}<{location}>{Col.RESET} "
            f"{Col.WHITE}{message}{Col.RESET}"
            f"{Col.ORANGE}{interaction_info}{Col.RESET}\n"
        )

        if extended_traceback and formatted_stack:
            traceback_list = "\n".join(traceback.format_list(stack))
            msg += f"Traceback:\n{traceback_list}\n"
            msg_colored += f"{Col.RED}Traceback:\n{Col.RESET}{traceback_list}\n"

        print(msg_colored, end='')

        with open(self.filename, 'a') as file:
            file.write(msg)

    def _log_str(self, level: str, message: str, interaction: discord.Interaction | None) -> None:
        """
        Log a string message with the specified level.
        Args:
            level (str): The log level.
            message (str): The message to log.
            interaction (discord.Interaction | None): Optional interaction context.
        """
        stack = traceback.extract_stack()
        self._log(level, message, interaction, stack, False)

    def debug(self, message: str, interaction: discord.Interaction | None = None):
        """
        Log a debug message.
        Args:
            message (str): The debug message to log.
            interaction (discord.Interaction | None): Optional interaction context.
        """
        self._log_str("DEBUG", message, interaction)

    def info(self, message: str, interaction: discord.Interaction | None = None):
        """
        Log an info message.
        Args:
            message (str): The info message to log.
            interaction (discord.Interaction | None): Optional interaction context.
        """
        self._log_str("INFO", message, interaction)

    def warning(self, message: str, interaction: discord.Interaction | None = None):
        """
        Log a warning message.
        Args:
            message (str): The warning message to log.
            interaction (discord.Interaction | None): Optional interaction context.
        """
        self._log_str("WARNING", message, interaction)

    def error(self, error: Error, interaction: discord.Interaction | None = None):
        """
        Log an error message.
        Args:
            error (Error): The error object to log.
            interaction (discord.Interaction | None): Optional interaction context.
        """
        self._log("ERROR", error.message, interaction,
                  error.stack, error.show_traceback)
