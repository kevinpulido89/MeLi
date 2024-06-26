"""Contains helper functions that can be used in any process."""

import json
import os
import sqlite3
from typing import Any, Self


def sanitize_file_path(file_path: str) -> str:
    """Sanitize the given file path to prevent directory traversal attacks.

    Args:
    - file_path (str): The original file path.
    - allowed_directory (str): The allowed directory or its subdirectories.

    Returns:
    - str: The sanitized file path.

    Raises:
    - ValueError: If the file_path is deemed unsafe.

    """
    # Get the absolute path of the allowed directory
    allowed_directory = os.path.abspath(os.getcwd())

    # Get the absolute path of the provided file_path
    absolute_path = os.path.abspath(file_path)

    # Check if the absolute_path is within or equal to the allowed_directory
    if not absolute_path.startswith(allowed_directory):
        raise ValueError(f"Unsafe file path: {file_path}")

    return absolute_path


def read_config_from_file(file_path: str) -> dict:
    """Read configuration from a JSON file.

    Args:
    - file_path (str): The path to the JSON file.

    Returns:
    - dict: The configuration as a dictionary.

    Raises:
    - FileNotFoundError: If the specified file_path does not exist.
    - json.JSONDecodeError: If there is an issue decoding the JSON content.
    - ValueError: If the file_path is deemed unsafe.

    """
    sanitized_path = sanitize_file_path(file_path)

    try:
        with open(sanitized_path, "r") as json_file:
            config = json.load(json_file)
        return config

    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{sanitized_path}' does not exist.")

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            msg=f"Error decoding JSON in '{sanitized_path}': {str(e)}", doc=e.doc, pos=e.pos
        )


class DatabaseHandler:
    """A class to handle database operations."""

    def __init__(self, db_name: str):
        """Initialize the DatabaseHandler object."""
        self.db_name = db_name

    def __enter__(self) -> Self:
        """Enter the context manager.

        Returns:
            Self: The current instance.

        """
        self.connect_to_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager.

        Args:
            exc_type: The type of the exception.
            exc_val: The exception value.
            exc_tb: The exception traceback.

        """
        self.close_connection()

    def connect_to_db(self):
        """Connect to the database."""
        self.cnx = sqlite3.connect(self.db_name)
        self.cur = self.cnx.cursor()

    def get_table_names(self) -> list[Any]:
        """Get the names of the tables in the database.

        Returns:
            list[Any]: The names of the tables in the database.

        """
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        return [table[0] for table in self.cur.execute(query).fetchall()]

    def get_table_columns(self, table_name: str) -> list[Any]:
        """Get the columns of the specified table.

        Args:
            table_name (str): The name of the table.

        Returns:
            list[Any]: The columns of the specified table.

        """
        query = f"PRAGMA table_info({table_name});"
        return [column[1] for column in self.cur.execute(query).fetchall()]

    def get_table_data(self, table_name: str) -> list[Any]:
        """Get the data from the specified table.

        Args:
            table_name (str): The name of the table.

        Returns:
            list[Any]: The data from the specified table.

        """
        query = f"SELECT * FROM {table_name};"
        return self.cur.execute(query).fetchall()

    def close_connection(self):
        """Close the connection to the database and the cursor."""
        self.cur.close()
        self.cnx.close()
