# queries/query04.py
"""
Query 4: Show the most popular route in the past 30 days.

This query counts completed trip transactions within the last 30 days,
groups by route, and returns the routes with the highest usage count.
"""

import streamlit as st

from db.connection import run_sql


@st.fragment
def run_query4() -> None:
    """
    Render the UI and execute Query 4.

    Provides a simple form with a submit button. On submission, builds a SQL query
    that joins transaction, trip, trip_route, and route tables to count route usage
    for completed trips in the last 30 days. Results are ordered descending by
    usage count and limited by session_state.limit_number.
    """
    print(f"{'-'*10} run_query4 {'-'*10}")

    query_container4 = st.container()
    st.markdown(
        "<h3 style='font-family:Arial; font-size:26px;'>Query4",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-family:Arial; font-size:18px;'>"
        "Description: Show the most popular route in the past "
        "30 days</p>",
        unsafe_allow_html=True,
    )

    input_col, output_col = st.columns([1, 2])

    with query_container4:
        with input_col:
            with st.form("query4"):
                q4_submitted = st.form_submit_button("query")

                if q4_submitted:
                    q4 = f"""
                    SELECT 
                        R.RouteID,
                        COUNT(*) AS UsageCount
                    FROM transaction T
                    JOIN trip TR ON T.TargetID = TR.TripID
                    JOIN trip_route TRT ON TR.TripID = TRT.TripID
                    JOIN route R ON TRT.RouteID = R.RouteID
                    WHERE T.TargetType = 'Trip'
                        AND T.STATUS = 'Completed'
                        AND T.CreatedAt >= NOW() - INTERVAL 30 DAY
                    GROUP BY R.RouteID
                    ORDER BY UsageCount DESC
                    LIMIT {st.session_state['limit_number']};
                    """
                    result = run_sql(q4)
                    st.session_state["query4_result"] = result

        with output_col:
            if "query4_result" not in st.session_state:
                st.write("No result")
            else:
                for item in st.session_state["query4_result"]:
                    st.write(item)

    query_container4_sql = st.container()
    with query_container4_sql:
        with st.expander("Show SQL"):
            if "query4_result" not in st.session_state:
                st.write("Please first make a query")
            else:
                st.code(q4, language="sql")