# queries/query05.py
"""
Query 5: Show the safest transportation type (ordered by accidents ascending).

This query counts the number of accidents associated with each transportation type,
using a LEFT JOIN to include types with zero accidents, and orders the results
from fewest to most accidents.
"""

import streamlit as st

from db.connection import run_sql


@st.fragment
def run_query5() -> None:
    """
    Render the UI and execute Query 5.

    Provides a simple form with a submit button. On submission, builds a SQL query
    that joins transportation and accident tables, groups by transportation type,
    and counts accident occurrences. Results are ordered by AccidentCount ascending
    (safest first) and displayed as raw tuples.
    """
    print(f"{'-'*10} run_query5 {'-'*10}")

    query_container5 = st.container()
    st.markdown(
        "<h3 style='font-family:Arial; font-size:26px;'>Query5",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-family:Arial; font-size:18px;'>"
        "Description: Show the safest transportation type "
        "(order by accidents asc)</p>",
        unsafe_allow_html=True,
    )

    input_col, output_col = st.columns([1, 2])

    with query_container5:
        with input_col:
            with st.form("query5"):
                q5_submitted = st.form_submit_button("query")

                if q5_submitted:
                    q5 = f"""
                    SELECT 
                        T.TYPE AS TransportationType,
                        COUNT(A.AccidentID) AS AccidentCount
                    FROM transportation T
                    LEFT JOIN accident A ON T.TransportationID = A.TransportationID
                    GROUP BY T.TYPE
                    ORDER BY AccidentCount ASC;
                    """
                    result = run_sql(q5)
                    st.session_state["query5_result"] = result

        with output_col:
            if "query5_result" not in st.session_state:
                st.write("No result")
            else:
                for item in st.session_state["query5_result"]:
                    st.write(item)

    query_container5_sql = st.container()
    with query_container5_sql:
        with st.expander("Show SQL"):
            if "query5_result" not in st.session_state:
                st.write("Please first make a query")
            else:
                st.code(q5, language="sql")