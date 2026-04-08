# queries/query03.py
"""
Query 3: Cancel a pending or completed transaction.

This query updates the status of a given transaction to 'Cancelled',
then displays the transaction record before and after the cancellation.
"""

import streamlit as st

from db.connection import run_sql


@st.fragment
def run_query3() -> None:
    """
    Render the UI and execute Query 3.

    Provides a dropdown to select a test transaction ID from
    session_state.cancel_transaction_list. On submission:
      1. Selects the transaction details (before cancellation)
      2. Updates the status to 'Cancelled' (if currently 'Pending' or 'Completed')
      3. Selects the transaction details again (after cancellation)

    Both before and after results are stored in session_state
    ("query3_before_result", "query3_after_result") for display.
    """
    print(f"{'-'*10} run_query3 {'-'*10}")

    query_container3 = st.container()
    st.markdown(
        "<h3 style='font-family:Arial; font-size:26px;'>Query3",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-family:Arial; font-size:18px;'>"
        "Description: Cancel a pending or completed transaction, "
        "given the TransactionID</p>",
        unsafe_allow_html=True,
    )

    input_col, output_col = st.columns([1, 2])

    with query_container3:
        with input_col:
            with st.form("query3"):
                transaction_id = st.selectbox(
                    "Test TransactionID",
                    options=st.session_state.cancel_transaction_list,
                )

                q3_submitted = st.form_submit_button("query")

                if q3_submitted:
                    q3_select = f"""
                    SELECT 
                        TransactionID,
                        UserID,
                        TotalAmount,
                        Currency,
                        PaymentMethod,
                        STATUS,
                        UpdatedAt
                    FROM `transaction`
                    WHERE TransactionID = '{transaction_id}';
                    """
                    result_before = run_sql(q3_select)

                    q3 = f"""
                    UPDATE `transaction`
                    SET STATUS = 'Cancelled',
                        UpdatedAt = NOW()
                    WHERE TransactionID = '{transaction_id}'
                    AND STATUS IN ('Pending','Completed');
                    """
                    _ = run_sql(q3)

                    result_after = run_sql(q3_select)

                    st.session_state["query3_before_result"] = result_before
                    st.session_state["query3_after_result"] = result_after

        with output_col:
            if "query3_after_result" not in st.session_state:
                st.write("No result")
            else:
                st.write("Before cancelling:")
                for item in st.session_state["query3_before_result"]:
                    st.write(item)
                st.write("After cancelling:")
                for item in st.session_state["query3_after_result"]:
                    st.write(item)

    query_container3_sql = st.container()
    with query_container3_sql:
        with st.expander("Show SQL"):
            if "query3_after_result" not in st.session_state:
                st.write("Please first make a query")
            else:
                st.code(q3, language="sql")