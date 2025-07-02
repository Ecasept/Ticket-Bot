from src.utils import logger
from database.other import DatabaseError
import datetime


class Giveaway:
    """
    Represents a giveaway with validation for all fields.

    Args:
        message_id (int): The Discord message ID for the giveaway.
        channel_id (int): The Discord channel ID where the giveaway is hosted.
        guild_id (int): The Discord guild ID where the giveaway is hosted.
        host_id (int): The Discord user ID who created the giveaway.
        prize (str): What is being given away.
        winner_count (int): Number of winners to select.
        role_id (int | None): Discord role ID to assign to winners, or None if no role.
        ends_at (datetime.datetime): When the giveaway ends.
        ended (bool): Whether the giveaway has ended.
        created_at (datetime.datetime): When the giveaway was created.

    Raises:
        DatabaseError: If any field has an invalid format.
    """

    def __init__(self, message_id: int, channel_id: int, guild_id: int, host_id: int, prize: str,
                 winner_count: int, role_id: int | None, ends_at: datetime.datetime,
                 ended: bool, created_at: datetime.datetime):
        if not isinstance(message_id, int):
            raise DatabaseError(f"Invalid message_id: {message_id}")
        if not isinstance(channel_id, int):
            raise DatabaseError(f"Invalid channel_id: {channel_id}")
        if not isinstance(guild_id, int):
            raise DatabaseError(f"Invalid guild_id: {guild_id}")
        if not isinstance(host_id, int):
            raise DatabaseError(f"Invalid host_id: {host_id}")
        if not isinstance(prize, str) or not prize.strip():
            raise DatabaseError(f"Invalid prize: {prize}")
        if not isinstance(winner_count, int) or winner_count < 1:
            raise DatabaseError(f"Invalid winner_count: {winner_count}")
        if role_id is not None and not isinstance(role_id, int):
            raise DatabaseError(f"Invalid role_id: {role_id}")
        if not isinstance(ends_at, datetime.datetime):
            raise DatabaseError(f"Invalid ends_at: {ends_at}")
        if not isinstance(ended, bool):
            raise DatabaseError(f"Invalid ended status: {ended}")
        if not isinstance(created_at, datetime.datetime):
            raise DatabaseError(f"Invalid created_at: {created_at}")

        self.message_id = message_id
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.host_id = host_id
        self.prize = prize
        self.winner_count = winner_count
        self.role_id = role_id
        self.ends_at = ends_at
        self.ended = ended
        self.created_at = created_at


class GiveawayManager:
    def __init__(self, connection):
        """
        Initialize the GiveawayManager with a database connection.
        Args:
            connection: SQLite database connection object.
        """
        self.connection = connection
        self.cursor = connection.cursor()

    def create_giveaway(self, message_id: int, channel_id: int, guild_id: int, host_id: int,
                        prize: str, winner_count: int, role_id: int | None, ends_at: datetime.datetime) -> int:
        """
        Create a new giveaway record in the database.
        Args:
            message_id (int): Discord message ID for the giveaway.
            channel_id (int): Discord channel ID where the giveaway is hosted.
            guild_id (int): Discord guild ID where the giveaway is hosted.
            host_id (int): ID of the user who created the giveaway.
            prize (str): What is being given away.
            winner_count (int): Number of winners to select.
            role_id (int | None): Discord role ID to assign to winners.
            ends_at (datetime.datetime): When the giveaway ends.
        Returns:
            int: The message_id of the created giveaway.
        """
        self.cursor.execute(
            "INSERT INTO giveaways (message_id, channel_id, guild_id, host_id, prize, winner_count, role_id, ends_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (message_id, channel_id, guild_id, host_id,
             prize, winner_count, role_id, ends_at)
        )
        self.connection.commit()
        logger.info(
            f"Giveaway {message_id} created for prize '{prize}' in channel {channel_id}.")
        return message_id

    def get_giveaway(self, message_id: int) -> Giveaway | None:
        """
        Retrieve a giveaway by its message_id.
        Args:
            message_id (int): Discord message ID for the giveaway.
        Returns:
            Giveaway | None: Giveaway data if found, else None.
        """
        self.cursor.execute(
            "SELECT message_id, channel_id, guild_id, host_id, prize, winner_count, role_id, ends_at, ended, created_at FROM giveaways WHERE message_id = ?",
            (message_id,)
        )
        giveaway_data = self.cursor.fetchone()
        if giveaway_data:
            return Giveaway(*giveaway_data)
        else:
            return None

    def update_giveaway(self, message_id: int, **fields):
        """
        Update one or more fields of a giveaway.
        Args:
            message_id (int): Discord message ID for the giveaway.
            **fields: Keyword arguments for fields to update.
                     Supported fields: ended
        """
        if not fields:
            raise ValueError("At least one field must be provided for update")

        set_clauses = []
        values = []
        for field, value in fields.items():
            if field not in ['ended']:
                raise ValueError(
                    f"Invalid field '{field}' for giveaway update")
            set_clauses.append(f"{field} = ?")
            values.append(value)

        # Add message_id to the end for the WHERE clause
        values.append(message_id)

        query = f"UPDATE giveaways SET {', '.join(set_clauses)} WHERE message_id = ?"
        self.cursor.execute(query, values)
        self.connection.commit()

        # Log the update
        field_updates = ", ".join([f"{k}={v}" for k, v in fields.items()])
        logger.info(f"Giveaway {message_id} updated: {field_updates}")

    def get_active_giveaways(self, current_time: datetime.datetime) -> list[Giveaway]:
        """
        Get all giveaways that have ended but haven't been processed yet.
        Args:
            current_time (datetime.datetime): The current time to compare against.
        Returns:
            list[Giveaway]: List of giveaways that need to be ended.
        """
        query = """
            SELECT message_id, channel_id, guild_id, host_id, prize, winner_count, role_id, ends_at, ended, created_at
            FROM giveaways
            WHERE ends_at <= ? AND ended = FALSE
        """
        self.cursor.execute(query, (current_time,))
        giveaways_data = self.cursor.fetchall()
        return [Giveaway(*giveaway_data) for giveaway_data in giveaways_data]
