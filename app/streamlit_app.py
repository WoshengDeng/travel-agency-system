# streamlit_app.py
"""
Main entry point for the Travel Agency System Streamlit application.

This module initializes the database connection, sets up session state,
and renders all 10 query interfaces.
"""

import atexit
import streamlit as st

from db.connection import connect_database, close_connection
from db.init_db import set_up
from queries.query01 import run_query1
from queries.query02 import run_query2
from queries.query03 import run_query3
from queries.query04 import run_query4
from queries.query05 import run_query5
from queries.query06 import run_query6
from queries.query07 import run_query7
from queries.query08 import run_query8
from queries.query09 import run_query9
from queries.query10 import run_query10


def run_streamlit() -> None:
    """Configure the Streamlit page and render all query modules."""
    st.set_page_config(page_title="ISE 503 Project", layout="centered")
    st.header("ISE 503 Project - Travel Agency System")

    # Render each query's UI
    run_query1()
    run_query2()
    run_query3()
    run_query4()
    run_query5()
    run_query6()
    run_query7()
    run_query8()
    run_query9()
    run_query10()


def main() -> None:
    """Main application routine: connect to database and launch UI."""
    connect_database()
    run_streamlit()


if __name__ == "__main__":
    # Register cleanup handler to close database connection on exit
    atexit.register(close_connection)

    # Perform one-time setup: create tables, insert seed data, initialize session state
    set_up()

    # Start the Streamlit app
    main()