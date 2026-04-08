# queries/query09.py
"""
Query 9: Show the total cost of a user account in the last year.

This query sums the total amount of completed transactions for a selected user
over the past 12 months, grouped by user ID.
"""

import streamlit as st

from db.connection import run_sql


@st.fragment
def run_query9() -> None:
    """
    Render the UI and execute Query 9.

    Provides a dropdown to select a user account from session_state.user_list.
    On submission, builds a SQL query that sums TotalAmount for completed
    transactions where CreatedAt is within the last year. Results are grouped
    by UserID and limited by session_state.limit_number.
    """
    print(f"{'-'*10} run_query9 {'-'*10}")

    query_container9 = st.container()
    st.markdown(
        "<h3 style='font-family:Arial; font-size:26px;'>Query9",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-family:Arial; font-size:18px;'>"
        "Description: Show the total cost of a user account"
        " in last one year</p>",
        unsafe_allow_html=True,
    )

    input_col, output_col = st.columns([1, 2])

    with query_container9:
        with input_col:
            with st.form("query9"):
                account = st.selectbox(
                    "Account",
                    options=st.session_state.user_list,
                )

                q9_submitted = st.form_submit_button("query")

                if q9_submitted:
                    q9 = f"""
                    SELECT T.UserID, SUM(T.TotalAmount)
                    FROM `transaction` AS T
                    WHERE T.UserID = '{account}'
                        AND T.STATUS = 'Completed'
                        AND t.CreatedAt >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                    GROUP BY T.UserID
                    LIMIT {st.session_state['limit_number']};
                    """
                    result = run_sql(q9)
                    st.session_state["query9_result"] = result

        with output_col:
            if "query9_result" not in st.session_state:
                st.write("No result")
            else:
                for item in st.session_state["query9_result"]:
                    st.write(item)

    query_container9_sql = st.container()
    with query_container9_sql:
        with st.expander("Show SQL"):
            if "query9_result" not in st.session_state:
                st.write("Please first make a query")
            else:
                st.code(q9, language="sql")