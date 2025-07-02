import datetime
from src.utils import logger


class ApplicationBanManager:
    def __init__(self, connection):
        """
        Initialize the ApplicationBanManager with a database connection.
        Args:
            connection: SQLite database connection object.
        """
        self.connection = connection
        self.cursor = self.connection.cursor(

        )

    def ban_user(self, user_id: int, guild_id: int, ends_at: datetime.datetime | None):
        """
        Ban a user from creating application tickets.
        Args:
            user_id (int): Discord user ID to ban.
            guild_id (int): Guild ID where the ban applies.
            ends_at (datetime.datetime | None): When the ban ends, or None for permanent ban.
        """
        self.cursor.execute(
            "INSERT INTO application_bans (user_id, guild_id, ends_at) VALUES (?, ?, ?)",
            (user_id, guild_id, ends_at)
        )
        self.connection.commit()
        logger.info(
            f"User {user_id} banned from applications in guild {guild_id} until {ends_at}.")

    def unban_user(self, user_id: int, guild_id: int):
        """
        Remove a user's ban from creating application tickets.
        Args:
            user_id (int): Discord user ID to unban.
            guild_id (int): Guild ID where the ban applies.
        """
        self.cursor.execute(
            "DELETE FROM application_bans WHERE user_id = ? AND guild_id = ?",
            (user_id, guild_id)
        )
        self.connection.commit()
        logger.info(
            f"User {user_id} unbanned from applications in guild {guild_id}.")

    def is_user_banned(self, user_id: int, guild_id: int) -> bool:
        """
        Check if a user is banned from creating application tickets.
        Args:
            user_id (int): Discord user ID to check.
            guild_id (int): Guild ID to check the ban in.
        Returns:
            bool: True if the user is banned, False otherwise.
        """
        self.cursor.execute(
            "SELECT 1 FROM application_bans WHERE user_id = ? AND guild_id = ?",
            (user_id, guild_id)
        )
        return self.cursor.fetchone() is not None

    def get_expired(self, current_time: datetime.datetime) -> list[tuple[int, int]]:
        """
        Get all application bans that have expired.
        Args:
            current_time (datetime.datetime): The current time to compare against.
        Returns:
            list[tuple[int, int]]: List of tuples containing (user_id, guild_id) for expired bans.
        """
        self.cursor.execute(
            "SELECT user_id, guild_id FROM application_bans WHERE ends_at < ?",
            (current_time,)
        )
        return self.cursor.fetchall()
