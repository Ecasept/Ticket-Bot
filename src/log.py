"""
Simple logging utility for the bot, supporting different log levels and file output.
"""
import datetime


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

    def log(self, level: str, tag: str, message: str):
        """
        Write a log message with a given level and tag.
        Args:
            level (str): Log level (e.g., 'INFO', 'ERROR').
            tag (str): Tag for the log message, indicating the source or context.
            message (str): The log message.
        """
        now = datetime.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M:%S")

        msg = f"{t} [{level}] <{tag}> {message}\n"

        print(msg, end='')

        with open(self.filename, 'a') as file:
            file.write(msg)

    def debug(self, tag: str, message: str):
        """
        Log a debug message.
        """
        self.log("DEBUG", tag, message)

    def info(self, tag: str, message: str):
        """
        Log an info message.
        """
        self.log("INFO", tag, message)

    def warning(self, tag: str, message: str):
        """
        Log a warning message.
        """
        self.log("WARNING", tag, message)

    def error(self, tag: str, message: str):
        """
        Log an error message.
        """
        self.log("ERROR", tag, message)
