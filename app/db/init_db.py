# db/init_db.py
"""
Database initialization and session state setup for the Travel Agency System.

This module provides functions to create database tables, insert seed data,
and initialize Streamlit session state with constants used by the query modules.
"""

import mysql.connector
import streamlit as st

from db.connection import connect_database, run_sql
from config import (
    DEFAULT_LIMIT_NUMBER,
    LOCATIONS,
    SEAT_QUERY_LIST,
    USER_LIST,
    CANCEL_TRANSACTION_LIST,
)


def _get_queries(file_path: str) -> list:
    """
    Read an SQL file and split it into individual statements.

    Args:
        file_path: Path to the SQL file.

    Returns:
        List of SQL statements (strings), empty statements removed.
    """
    with open(file_path, "r") as f:
        sql_script = f.read()
    statements = [stmt.strip() for stmt in sql_script.split(";") if stmt.strip()]
    return statements


def _initialize(init_file: str) -> None:
    """
    Execute a series of SQL statements to initialize the database (e.g., create tables).

    Args:
        init_file: Path to the SQL file containing initialization statements.
    """
    connector = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
    )
    cursor = connector.cursor()

    init_sql = _get_queries(init_file)
    for stmt in init_sql:
        if stmt:
            try:
                cursor.execute(stmt)
            except mysql.connector.Error as err:
                print(f"Initialization Error: {err}\nStatement: {stmt}")

    print(f"{'-'*10} Initialization Completed {'-'*10}")
    connector.commit()
    cursor.close()
    connector.close()


def set_up() -> None:
    """
    Perform one‑time setup for the application.

    1. Creates database tables (schema.sql)
    2. Inserts seed data (seed.sql)
    3. Initializes Streamlit session state using constants from config.py
    """
    # Step 1: Create tables
    _initialize("../database/schema.sql")

    # Step 2: Insert seed data
    connect_database()
    insert_sql = _get_queries("../database/seed.sql")
    for stmt in insert_sql:
        if stmt:
            try:
                cursor = st.session_state.db_connector.cursor()
                cursor.execute(stmt)
                cursor.close()
            except mysql.connector.Error as err:
                print(f"Insert data Error: {err}\nStatement: {stmt}")
    st.session_state.db_connector.commit()
    print(f"{'-'*10} Insert data Completed {'-'*10}")

    # Step 3: Initialize session state constants (now imported from config)
    st.session_state.limit_number = DEFAULT_LIMIT_NUMBER
    st.session_state.locations = LOCATIONS
    st.session_state.seat_query_list = SEAT_QUERY_LIST
    st.session_state.user_list = USER_LIST
    st.session_state.cancel_transaction_list = CANCEL_TRANSACTION_LIST