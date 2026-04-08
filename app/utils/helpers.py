# utils/helpers.py
"""
Helper utilities for the Travel Agency System.

This module provides common helper functions used across the application,
such as reading and parsing SQL files.
"""

from typing import List


def get_queries(file_path: str) -> List[str]:
    """
    Read an SQL file and split it into individual statements.

    The function reads the entire file, strips leading/trailing whitespace,
    and splits the content by semicolon (;). Empty statements are removed.

    Args:
        file_path: Path to the SQL file.

    Returns:
        List of SQL statements (strings), with each statement stripped of
        surrounding whitespace. Empty statements are excluded.

    Example:
        >>> statements = get_queries("database/schema.sql")
        >>> for stmt in statements:
        ...     cursor.execute(stmt)
    """
    with open(file_path, "r") as f:
        sql_script = f.read()
    # Split by semicolon and filter out empty statements
    statements = [stmt.strip() for stmt in sql_script.split(";") if stmt.strip()]
    return statements