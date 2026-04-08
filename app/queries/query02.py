# queries/query02.py
"""
Query 2: Show travel history for a given passenger account.

This query retrieves all trip records (TripID, total cost, start/end dates)
associated with a selected user account from the transaction table.
"""

import streamlit as st

from db.connection import run_sql


@st.fragment
def run_query2() -> None:
    """
    Render the UI and execute Query 2.

    Provides a dropdown to select a user account from session_state.user_list.
    On submission, builds a SQL query to fetch the user's completed trip
    transactions, executes it via run_sql(), and stores the result in
    session_state["query2_result"] for display.
    """
    print(f"{'-'*10} run_query2 {'-'*10}")

    query_container2 = st.container()
    st.markdown(
        "<h3 style='font-family:Arial; font-size:26px;'>Query2",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-family:Arial; font-size:18px;'>"
        "Description: Show all the travel history records for a "
        "given passenger account</p>",
        unsafe_allow_html=True,
    )

    input_col, output_col = st.columns([1, 2])

    with query_container2:
        with input_col:
            with st.form("query2"):
                account = st.selectbox(
                    "Accounts",
                    options=st.session_state.user_list,
                )

                q2_submitted = st.form_submit_button("query")

                if q2_submitted:
                    q2 = f"""
                    SELECT
                        Tr.TripID AS TripID,
                        Tr.TotalCost AS Cost,
                        Tr.StartDate AS StartDate,
                        Tr.EndDate AS EndDate
                    FROM `transaction` T
                    JOIN trip Tr ON T.TargetID = Tr.TripID
                    WHERE T.UserID = '{account}' AND T.TargetType = 'Trip'
                    LIMIT {st.session_state['limit_number']};
                    """
                    result = run_sql(q2)
                    st.session_state["query2_result"] = result

        with output_col:
            if "query2_result" not in st.session_state:
                st.write("No result")
            else:
                for item in st.session_state["query2_result"]:
                    st.write(item)

    query_container2_sql = st.container()
    with query_container2_sql:
        with st.expander("Show SQL"):
            if "query2_result" not in st.session_state:
                st.write("Please first make a query")
            else:
                st.code(q2, language="sql")