# queries/query06.py
"""
Query 6: Show the least frequent delayed public transportation.

This query calculates the delay ratio (number of delayed routes divided by total routes)
for each transportation type, and orders the results from lowest to highest delay ratio.
"""

import streamlit as st

from db.connection import run_sql


@st.fragment
def run_query6() -> None:
    """
    Render the UI and execute Query 6.

    Provides a simple form with a submit button. On submission, builds a SQL query
    that joins route and transportation tables, computes the delay ratio using a
    conditional count, and orders the results by DelayRatio ascending (least delayed first).
    """
    print(f"{'-'*10} run_query6 {'-'*10}")

    query_container6 = st.container()
    st.markdown(
        "<h3 style='font-family:Arial; font-size:26px;'>Query6",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-family:Arial; font-size:18px;'>"
        "Description: Show the least frequent delayed public "
        "transportation</p>",
        unsafe_allow_html=True,
    )

    input_col, output_col = st.columns([1, 2])

    with query_container6:
        with input_col:
            with st.form("query6"):
                q6_submitted = st.form_submit_button("query")

                if q6_submitted:
                    q6 = f"""
                    SELECT 
                        T.TYPE AS TransportationType,
                        COUNT(CASE WHEN R.STATUS = 'Delayed' THEN 1 END) * 1.0 / COUNT(*) AS DelayRatio
                    FROM route R
                    JOIN transportation T 
                    ON R.TransportationID = T.TransportationID
                    GROUP BY T.TYPE
                    ORDER BY DelayRatio ASC;
                    """
                    result = run_sql(q6)
                    st.session_state["query6_result"] = result

        with output_col:
            if "query6_result" not in st.session_state:
                st.write("No result")
            else:
                for item in st.session_state["query6_result"]:
                    st.write(item)

    query_container6_sql = st.container()
    with query_container6_sql:
        with st.expander("Show SQL"):
            if "query6_result" not in st.session_state:
                st.write("Please first make a query")
            else:
                st.code(q6, language="sql")