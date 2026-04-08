# queries/query08.py
"""
Query 8: Find hotels whose average price is closest to a user's average accommodation cost.

This query computes the average accommodation spending of a selected user over the past year,
then compares it with the average base price of hotels (rooms) and BNBs. It returns hotels
with the smallest absolute difference between their average price and the user's average cost.
"""

import streamlit as st

from db.connection import run_sql


@st.fragment
def run_query8() -> None:
    """
    Render the UI and execute Query 8.

    Provides a dropdown to select a user account from session_state.user_list.
    On submission, builds a SQL query that:
      1. Computes the user's average transaction amount for accommodation (past year).
      2. Computes average prices for rooms (hotels) and BNBs.
      3. Cross joins the user average with accommodation averages.
      4. Filters only hotels (via INNER JOIN hotel) and orders by price difference.
    Results are limited by session_state.limit_number.
    """
    print(f"{'-'*10} run_query8 {'-'*10}")

    query_container8 = st.container()
    st.markdown(
        "<h3 style='font-family:Arial; font-size:26px;'>Query8",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-family:Arial; font-size:18px;'>"
        "Description: Show the hotels, whose average price is the "
        "closest to the average accommodation costs "
        "for a given passenger account over recent 1 year.</p>",
        unsafe_allow_html=True,
    )

    input_col, output_col = st.columns([1, 2])

    with query_container8:
        with input_col:
            with st.form("query8"):
                account = st.selectbox(
                    "Account",
                    options=st.session_state.user_list,
                )

                q8_submitted = st.form_submit_button("query")

                if q8_submitted:
                    q8 = f"""
                    WITH user_avg AS (
                        SELECT AVG(T.TotalAmount) AS avg_cost
                        FROM `transaction` AS T
                        WHERE T.UserID = '{account}'
                        AND T.TargetType = 'Accommodation'
                        AND T.STATUS = 'Completed'
                        AND T.CreatedAt >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) 
                    ),
                    accommodation_avg AS (
                        SELECT R.AccommodationID, AVG(R.BasePrice) AS avg_price
                        FROM room AS R
                        GROUP BY R.AccommodationID
                        UNION ALL
                        SELECT bnb.AccommodationID, AVG(bnb.BasePrice) AS avg_price
                        FROM bnb
                        GROUP BY bnb.AccommodationID
                    )
                    SELECT 
                        A.AccommodationID,
                        A.ContactPhone,  
                        A.Rating,
                        AA.avg_price,
                        ABS(AA.avg_price - U.avg_cost) AS price_diff
                    FROM accommodation_avg AA
                    CROSS JOIN user_avg U
                    JOIN accommodation A ON AA.AccommodationID = A.AccommodationID
                    INNER JOIN hotel H ON A.AccommodationID = H.AccommodationID  
                    ORDER BY price_diff
                    LIMIT {st.session_state['limit_number']};
                    """
                    result = run_sql(q8)
                    st.session_state["query8_result"] = result

        with output_col:
            if "query8_result" not in st.session_state:
                st.write("No result")
            else:
                for item in st.session_state["query8_result"]:
                    st.write(item)

    query_container8_sql = st.container()
    with query_container8_sql:
        with st.expander("Show SQL"):
            if "query8_result" not in st.session_state:
                st.write("Please first make a query")
            else:
                st.code(q8, language="sql")