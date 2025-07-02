from src.utils import logger


class ConstantManager:
    def __init__(self, connection):
        """
        Initialize the ConstantManager with a database connection.
        Args:
            connection: SQLite database connection object.
        """
        self.connection = connection
        self.cursor = connection.cursor()

    def get(self, key: str, guild: int) -> str | None:
        """
        Get a constant value from the database.
        Args:
            key (str): Key of the constant.
            guild (int): Guild ID for the constant.
        Returns:
            str | None: Constant value if found, else None.
        """
        self.cursor.execute(
            "SELECT value FROM constants WHERE key = ? AND guild_id = ?", (key, guild))
        constant = self.cursor.fetchone()
        if constant:
            return constant[0]
        else:
            return None

    def set(self, key: str, value: str, guild: int):
        """
        Set a constant value in the database.
        Args:
            key (str): Key of the constant.
            value (str): Value to set.
            guild (int): Guild ID for the constant.
        """
        self.cursor.execute(
            "INSERT OR REPLACE INTO constants (key, guild_id, value) VALUES (?, ?, ?)",
            (key, guild, value)
        )
        self.connection.commit()
        logger.info(f"Constant {key} set to {value} for guild {guild}.")
