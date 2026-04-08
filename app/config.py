# app/config.py
"""
Configuration constants for the Travel Agency System Streamlit app.

This module holds static data such as location ID mappings, test user IDs,
and default display limits used across query modules.
"""

# Default number of rows to display in query results
DEFAULT_LIMIT_NUMBER = 5

# Mapping from city names to their internal location IDs
LOCATIONS = {
    "Boston": "LOC0001",
    "Providence": "LOC0002",
    "New York": "LOC0003",
    "Philadelphia": "LOC0004",
    "Baltimore": "LOC0005",
    "Washington": "LOC0006",
    "Richmond": "LOC0007",
    "Charlotte": "LOC0008",
    "Jacksonville": "LOC0009",
    "Miami": "LOC0010",
}

# Sample route IDs used for seat availability queries
SEAT_QUERY_LIST = ["ROUTETRAIN001", "ROUTEPLANE001"]

# Sample user IDs for testing passenger account queries
USER_LIST = ["USR00001", "USR00002", "USR00003", "USR00004", "USR00005"]

# Sample transaction IDs for cancellation demonstration
CANCEL_TRANSACTION_LIST = ["TXN00200", "TXN00201"]