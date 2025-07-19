"""
This module defines the BanlistManager class, which is responsible for 
managing bans in the database.
"""
import sqlite3
from typing import List, Tuple

class BanlistManager:
    """
    Manages bans in the database.
    """

    def __init__(self, connection: sqlite3.Connection):
        """
        Initializes the BanlistManager.

        Args:
            connection (sqlite3.Connection): The database connection.
        """
        self.connection = connection
        self.cursor = connection.cursor()

    def add_ban(self, name: str, guild_id: int, reason: str, banned_by: str, length: str):
        """
        Adds a ban to the database.

        Args:
            name (str): The name of the banned user.
            guild_id (int): The ID of the guild.
            reason (str): The reason for the ban.
            banned_by (str): The user who issued the ban.
            length (str): The length of the ban.
        """
        self.cursor.execute(
            "INSERT INTO banlist_bans (name, guild_id, reason, banned_by, length) VALUES (?, ?, ?, ?, ?)",
            (name, guild_id, reason, banned_by, length)
        )
        self.connection.commit()

    def remove_ban(self, name: str, guild_id: int):
        """
        Removes a ban from the database.

        Args:
            name (str): The name of the banned user.
            guild_id (int): The ID of the guild.
        """
        self.cursor.execute(
            "DELETE FROM banlist_bans WHERE name = ? AND guild_id = ?",
            (name, guild_id)
        )
        self.connection.commit()

    def is_banned(self, name: str, guild_id: int) -> bool:
        """
        Checks if a user is banned in a specific guild.

        Args:
            name (str): The name of the user.
            guild_id (int): The ID of the guild.

        Returns:
            bool: True if the user is banned, False otherwise.
        """
        self.cursor.execute(
            "SELECT 1 FROM banlist_bans WHERE name = ? AND guild_id = ?",
            (name, guild_id)
        )
        return self.cursor.fetchone() is not None

    def get_bans(self, guild_id: int) -> List[Tuple[str, str, str, str]]:
        """
        Gets all bans for a specific guild.

        Args:
            guild_id (int): The ID of the guild.

        Returns:
            List[Tuple[str, str, str, str]]: A list of tuples, where each tuple
            contains the name, reason, banned_by, and length of a ban.
        """
        self.cursor.execute(
            "SELECT name, reason, banned_by, length FROM banlist_bans WHERE guild_id = ?",
            (guild_id,)
        )
        return self.cursor.fetchall()
