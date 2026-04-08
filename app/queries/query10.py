# queries/query10.py
"""
Query 10: Show the highest average ratings of locations.

This query computes an overall rating for each location by averaging ratings from:
- Transportation reviews (source/destination locations of routes used in trips)
- Restaurant ratings
- Activity ratings
- Accommodation ratings

Results are ordered by overall rating descending.
"""

import streamlit as st

from db.connection import run_sql


@st.fragment
def run_query10() -> None:
    """
    Render the UI and execute Query 10.

    Provides a simple form with a submit button. On submission, builds a complex
    SQL query that:
      1. Creates a trans_review CTE collecting ratings from routes linked to trips.
      2. Computes average ratings for transportation, restaurants, activities, and accommodations.
      3. Combines all ratings using CROSS JOIN LATERAL and averages them per location.
      4. Returns locations with rounded overall rating, ordered descending.
    Results are limited by session_state.limit_number.
    """
    print(f"{'-'*10} run_query10 {'-'*10}")

    query_container10 = st.container()
    st.markdown(
        "<h3 style='font-family:Arial; font-size:26px;'>Query10",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-family:Arial; font-size:18px;'>"
        "Show the highest average ratings of the locations, based on "
        "the review ratings corresponding to the transportations "
        "start from or end with the location, and the ratings of the "
        "restaurants, activities, accommodation in the city</p>",
        unsafe_allow_html=True,
    )

    input_col, output_col = st.columns([1, 2])

    with query_container10:
        with input_col:
            with st.form("query10"):
                q10_submitted = st.form_submit_button("query")

                if q10_submitted:
                    q10 = f"""
                    WITH trans_review AS (
                        SELECT r.SourceLocationID   AS LocationID,
                            rv.Rating
                        FROM route        AS r
                        JOIN trip_route   AS tr ON tr.RouteID      = r.RouteID
                        JOIN `transaction`AS t  ON t.TargetType    = 'Trip'
                                                AND t.TargetID     = tr.TripID
                        JOIN review       AS rv ON rv.TransactionID = t.TransactionID
                        WHERE r.SourceLocationID IS NOT NULL

                        UNION ALL

                        SELECT r.DestinationLocationID,
                            rv.Rating
                        FROM route        AS r
                        JOIN trip_route   AS tr ON tr.RouteID      = r.RouteID
                        JOIN `transaction`AS t  ON t.TargetType    = 'Trip'
                                                AND t.TargetID     = tr.TripID
                        JOIN review       AS rv ON rv.TransactionID = t.TransactionID
                        WHERE r.DestinationLocationID IS NOT NULL
                    ),

                    trans_avg  AS (SELECT LocationID, AVG(Rating) AS avg_trans_rating  FROM trans_review GROUP BY LocationID),
                    rest_avg   AS (SELECT LocationID, AVG(Rating) AS avg_rest_rating   FROM restaurant   GROUP BY LocationID),
                    act_avg    AS (SELECT LocationID, AVG(Rating) AS avg_act_rating    FROM activity     GROUP BY LocationID),
                    accom_avg  AS (SELECT LocationID, AVG(Rating) AS avg_accom_rating  FROM accommodation GROUP BY LocationID),

                    combined AS (
                        SELECT
                            l.LocationID,
                            l.City,
                            l.StateProvince,
                            l.Country,

                            AVG(val) AS overall_rating
                        FROM location AS l
                        LEFT JOIN trans_avg  ta ON ta.LocationID  = l.LocationID
                        LEFT JOIN rest_avg   ra ON ra.LocationID  = l.LocationID
                        LEFT JOIN act_avg    aa ON aa.LocationID  = l.LocationID
                        LEFT JOIN accom_avg  ca ON ca.LocationID  = l.LocationID

                        CROSS JOIN LATERAL (
                            SELECT ta.avg_trans_rating  AS val UNION ALL
                            SELECT ra.avg_rest_rating   UNION ALL
                            SELECT aa.avg_act_rating    UNION ALL
                            SELECT ca.avg_accom_rating
                        ) AS x
                        WHERE x.val IS NOT NULL            
                        GROUP BY l.LocationID
                    )

                    SELECT
                        LocationID,
                        City,
                        StateProvince,
                        Country,
                        ROUND(overall_rating, 2) AS overall_rating
                    FROM combined
                    ORDER BY overall_rating DESC
                    LIMIT {st.session_state['limit_number']};
                    """
                    result = run_sql(q10)
                    st.session_state["query10_result"] = result

        with output_col:
            if "query10_result" not in st.session_state:
                st.write("No result")
            else:
                for item in st.session_state["query10_result"]:
                    st.write(item)

    query_container10_sql = st.container()
    with query_container10_sql:
        with st.expander("Show SQL"):
            if "query10_result" not in st.session_state:
                st.write("Please first make a query")
            else:
                st.code(q10, language="sql")