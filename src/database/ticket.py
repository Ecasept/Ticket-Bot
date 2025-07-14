import datetime
from .other import DatabaseError
from src.utils import logger


class Ticket:
    """
    Represents a support ticket with validation for all fields.

    Args:
        channel_id (str): The Discord channel ID for the ticket (must be a valid integer string).
        category_id (int | None): The ticket category ID, or None for tickets without categories.
        user_id (str): The Discord user ID who created the ticket (must be a valid integer string).
        assignee_id (str | None): The Discord user ID of the assigned moderator, or None if unassigned.
        archived (bool): Whether the ticket is archived/closed.
        created_at (datetime.datetime): When the ticket was created.
        close_at (datetime.datetime | None): When the ticket is scheduled to close, or None if not scheduled.

    Raises:
        DatabaseError: If any field has an invalid format.
    """

    def __init__(self, channel_id: str, category_id: int | None, user_id: str, assignee_id: str | None, archived: bool, created_at: datetime.datetime, close_at: datetime.datetime | None):
        def is_string_digit(s: str) -> bool:
            """Check if a string is a digit."""
            return isinstance(s, str) and s.isdigit()

        if not is_string_digit(channel_id):
            raise DatabaseError(f"Invalid channel_id: {channel_id}")
        if category_id is not None and not isinstance(category_id, int):
            raise DatabaseError(f"Invalid category_id: {category_id}")
        if not is_string_digit(user_id):
            raise DatabaseError(f"Invalid user_id: {user_id}")
        if not is_string_digit(assignee_id) and assignee_id is not None:
            raise DatabaseError(f"Invalid assignee_id: {assignee_id}")
        if not isinstance(archived, bool):
            raise DatabaseError(f"Invalid archived status: {archived}")
        if not isinstance(created_at, datetime.datetime):
            raise DatabaseError(f"Invalid created_at: {created_at}")
        if not (isinstance(close_at, datetime.datetime) or close_at is None):
            raise DatabaseError(f"Invalid close_at: {close_at}")
        self.channel_id = channel_id
        self.category_id = category_id
        self.user_id = user_id
        self.assignee_id = assignee_id
        self.archived = archived
        self.created_at = created_at
        self.close_at = close_at


class TicketManager:

    def __init__(self, connection):
        """
        Initialize the TicketManager with a database connection.
        Args:
            connection: SQLite database connection object.
        """
        self.connection = connection
        self.cursor = connection.cursor()

    def create(self, channel_id: str, category_id: int | None, user_id: str, assignee_id: str | None, archived: bool = False, close_at: datetime.datetime | None = None) -> str:
        """
        Create a new ticket record in the database.
        Args:
            channel_id (str): Discord channel ID for the ticket.
            category_id (int | None): Ticket category ID, or None for tickets without categories.
            user_id (str): ID of the user who created the ticket.
            assignee_id (str | None): ID of the user assigned to the ticket.
            archived (bool): Whether the ticket is archived or not. Defaults to False.
            close_at (datetime.datetime | None): When the ticket should be closed. Defaults to None.
        Returns:
            str: The channel_id of the created ticket.
        """
        self.cursor.execute(
            "INSERT INTO tickets (channel_id, category_id, user_id, assignee_id, archived, close_at) VALUES (?, ?, ?, ?, ?, ?)",
            (channel_id, category_id, user_id, assignee_id, archived, close_at)
        )
        self.connection.commit()
        logger.info(
            f"Ticket {channel_id} created with category_id {category_id}, user {user_id}, assignee {assignee_id}, archived status {archived}, and close_at {close_at}.")
        return channel_id

    def get(self, channel_id: str) -> Ticket | None:
        """
        Retrieve a ticket by its channel_id.
        Args:
            channel_id (str): Discord channel ID for the ticket.
        Returns:
            Ticket | None: Ticket data if found, else None.
        """
        self.cursor.execute(
            "SELECT channel_id, category_id, user_id, assignee_id, archived, created_at, close_at FROM tickets WHERE channel_id = ?", (channel_id,))
        ticket_data = self.cursor.fetchone()
        if ticket_data:
            return Ticket(*ticket_data)
        else:
            return None

    def update(self, channel_id: str, **fields):
        """
        Update one or more fields of a ticket.
        Args:
            channel_id (str): Discord channel ID for the ticket.
            **fields: Keyword arguments for fields to update.
                     Supported fields: assignee_id, archived, close_at
        """
        if not fields:
            raise ValueError("At least one field must be provided for update")

        set_clauses = []
        values = []
        for field, value in fields.items():
            if field not in ['assignee_id', 'archived', 'close_at']:
                raise ValueError(f"Invalid field '{field}' for ticket update")
            set_clauses.append(f"{field} = ?")
            values.append(value)

        # Add channel_id to the end for the WHERE clause
        values.append(channel_id)

        query = f"UPDATE tickets SET {', '.join(set_clauses)} WHERE channel_id = ?"
        self.cursor.execute(query, values)
        self.connection.commit()

        # Log the update
        field_updates = ", ".join([f"{k}={v}" for k, v in fields.items()])
        logger.info(f"Ticket {channel_id} updated: {field_updates}")

    def delete(self, channel_id: str):
        """
        Delete a ticket by its channel_id.
        Args:
            channel_id (str): Discord channel ID for the ticket.
        """
        self.cursor.execute(
            "DELETE FROM tickets WHERE channel_id = ?", (channel_id,)
        )
        self.connection.commit()
        logger.info(f"Ticket {channel_id} deleted.")

    def get_overdue(self, time: datetime.datetime) -> list[str]:
        """
        Finds tickets where `close_at` is less than `now` and `archived` is `FALSE`,
        and returns their channel_ids.
        Args:
            time (datetime.datetime): The time to compare against ticket `close_at` times.
        Returns:
            list[str]: A list of channel_ids for the overdue tickets.

        """
        query = """
            SELECT channel_id
            FROM tickets
            WHERE close_at < ? AND archived = FALSE;
        """
        self.cursor.execute(query, (time,))
        overdue_ticket_ids = [row[0] for row in self.cursor.fetchall()]
        return overdue_ticket_ids
