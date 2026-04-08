# db/connection.py
"""
Database connection management for the Travel Agency System.

This module provides functions to establish, retrieve, and close a MySQL database
connection using Streamlit's session state, as well as a safe executor for SQL queries.
"""

import mysql.connector
import streamlit as st


def connect_database(database: str = "travel_agency") -> None:
    """
    Establish a database connection and store it in Streamlit session state.

    If a connection already exists in session state under the key "db_connector",
    this function does nothing. Otherwise, it creates a new connection using
    the provided database name and stores it.

    Args:
        database: Name of the MySQL database to connect to. Defaults to "travel_agency".
    """
    if "db_connector" not in st.session_state:
        connector = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=database,
        )
        st.session_state.db_connector = connector
        print(f"{'-'*10} Connect to database: {database} {'-'*10}")


def close_connection() -> None:
    """
    Close the database connection if it exists in session state.

    This function is typically registered with atexit to ensure proper cleanup
    when the Streamlit app terminates.
    """
    connector = st.session_state.get("db_connector", None)
    if connector:
        connector.close()
        print(f"{'-'*10} Close connections {'-'*10}")


def run_sql(query: str):
    """
    Execute a SQL query using the connection stored in session state.

    The function fetches all results, commits the transaction, and returns the
    result set. On error, it rolls back the transaction and re-raises the exception.

    Args:
        query: The SQL statement to execute (supports SELECT, UPDATE, INSERT, etc.).

    Returns:
        List of tuples containing the query result rows, or None for non-SELECT queries.

    Raises:
        mysql.connector.Error: If a database error occurs during execution.
    """
    connector = st.session_state.get("db_connector")
    if not connector:
        raise RuntimeError("No database connection found. Call connect_database() first.")

    cursor = None
    try:
        cursor = connector.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connector.commit()          # Important: commit after fetching results
        return result
    except mysql.connector.Error as err:
        print(f"Query Error: {err}")
        connector.rollback()        # Rollback on error to maintain consistency
        raise err
    finally:
        if cursor:
            cursor.close()          # Always close the cursor to free resources