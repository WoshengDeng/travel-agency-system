# queries/query07.py
"""
Query 7: Show the remaining seats for a route.

This query retrieves available travel units (seats) for a selected route,
including unit number, seat type, and class.
"""

import streamlit as st

from db.connection import run_sql


@st.fragment
def run_query7() -> None:
    """
    Render the UI and execute Query 7.

    Provides a dropdown to select a route from session_state.seat_query_list.
    On submission, builds a SQL query that joins route_unit and travel_unit tables
    to fetch available units (IsAvailable = TRUE) for the selected route.
    Results are ordered by seat class and type, limited by session_state.limit_number.
    """
    print(f"{'-'*10} run_query7 {'-'*10}")

    query_container7 = st.container()
    st.markdown(
        "<h3 style='font-family:Arial; font-size:26px;'>Query7",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-family:Arial; font-size:18px;'>"
        "Description: Show the remaining seats for a route</p>",
        unsafe_allow_html=True,
    )

    input_col, output_col = st.columns([1, 2])

    with query_container7:
        with input_col:
            with st.form("query7"):
                route = st.selectbox(
                    "Route",
                    options=st.session_state.seat_query_list,
                )

                q7_submitted = st.form_submit_button("query")

                if q7_submitted:
                    q7 = f"""
                    SELECT
                        R.RouteID,
                        R.UnitNumber,
                        T.TYPE AS SeatType,
                        T.Class AS SeatClass
                    FROM route_unit AS R
                    JOIN travel_unit AS T
                        ON R.TransportationID = T.TransportationID
                        AND R.UnitNumber = T.UnitNumber
                    WHERE R.RouteID = '{route}' AND R.IsAvailable = TRUE
                    ORDER BY T.Class, T.TYPE
                    LIMIT {st.session_state['limit_number']};
                    """
                    result = run_sql(q7)
                    st.session_state["query7_result"] = result

        with output_col:
            if "query7_result" not in st.session_state:
                st.write("No result")
            else:
                for item in st.session_state["query7_result"]:
                    st.write(item)

    query_container7_sql = st.container()
    with query_container7_sql:
        with st.expander("Show SQL"):
            if "query7_result" not in st.session_state:
                st.write("Please first make a query")
            else:
                st.code(q7, language="sql")