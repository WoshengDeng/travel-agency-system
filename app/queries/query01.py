# queries/query01.py
"""
Query 1: Multi‑modal route planning with recursive CTE.

This query allows users to find all possible combinations of public transportation
between a source and destination location within a given date range, with configurable
number of transfers and transportation types (plane, train, bus, ship).
"""

import datetime
import streamlit as st

from db.connection import run_sql


@st.fragment
def run_query1() -> None:
    """
    Render the UI and execute Query 1.

    Provides a form to select:
        - Departure and arrival locations (from session state location mapping)
        - Maximum number of transfers (1‑5)
        - Date range (start/end)
        - Transportation types (plane, train, bus, ship)

    On submission, builds a recursive CTE SQL query, executes it via run_sql(),
    and stores the result in session_state["query1_result"] for display.
    """
    print(f"{'-'*10} run_query1 {'-'*10}")

    query_container1 = st.container()
    st.markdown(
        "<h3 style='font-family:Arial; font-size:26px;'>Query1",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-family:Arial; font-size:18px;'>"
        "Description: Show all the possible combinations of selected "
        "public transportations from source location to target "
        "location with given StartDate and EndDate</p>",
        unsafe_allow_html=True,
    )

    input_col, output_col = st.columns([1, 2])

    with query_container1:
        with input_col:
            with st.form("query1"):
                src_location = st.selectbox(
                    "Departure Location",
                    options=st.session_state["locations"].keys(),
                )
                dest_location = st.selectbox(
                    "Arrival Location",
                    options=st.session_state["locations"].keys(),
                )
                num_transfers = st.selectbox(
                    "Num of transfers",
                    options=[1, 2, 3, 4, 5],
                )

                start_date = st.date_input(
                    "StartDate",
                    datetime.date(2025, 4, 27),
                    min_value=datetime.date(2025, 4, 27),
                    max_value=datetime.date(2025, 5, 3),
                )
                start_datetime = start_date.strftime("%Y-%m-%d 00:00:00")

                end_date = st.date_input(
                    "EndDate",
                    datetime.date(2025, 4, 27),
                    min_value=datetime.date(2025, 4, 27),
                    max_value=datetime.date(2025, 5, 4),
                )
                end_datetime = end_date.strftime("%Y-%m-%d 23:59:59")

                col1, col2 = st.columns(2)
                with col1:
                    use_plane = st.checkbox("Plane")
                with col2:
                    use_train = st.checkbox("Train")

                col3, col4 = st.columns(2)
                with col3:
                    use_bus = st.checkbox("Bus")
                with col4:
                    use_ship = st.checkbox("Ship")

                q1_submitted = st.form_submit_button("query")

                if q1_submitted:
                    transport_types = []
                    if use_plane:
                        transport_types.append("Plane")
                    if use_ship:
                        transport_types.append("Ship")
                    if use_train:
                        transport_types.append("Train")
                    if use_bus:
                        transport_types.append("Bus")

                    transport_str = ", ".join([f"'{t}'" for t in transport_types])
                    print("transport_str", transport_str)

                    q1 = f"""
                    WITH RECURSIVE route_chain AS (
                    -- Base case: Direct routes from the source
                    SELECT
                        r.ScheduledDeparture,
                        r.ScheduledArrival,
                        r.DestinationLocationID,
                        CAST(r.ScheduledDeparture AS CHAR(1000)) AS schedule_departure_path,
                        CAST(r.ScheduledArrival AS CHAR(1000)) AS scheduled_arrival_path,
                        CAST(r.SourceLocationID AS CHAR(1000)) AS source_location_path,
                        CAST(r.DestinationLocationID AS CHAR(1000)) AS dest_location_path,
                        CAST(r.TransportationID AS CHAR(1000)) AS transpotation_path,
                        0 AS depth,
                        CAST(r.RouteID AS CHAR(1000)) AS route_path
                    FROM route r
                    JOIN transportation t ON r.TransportationID = t.TransportationID
                    WHERE r.SourceLocationID = '{st.session_state['locations'][src_location]}'
                    AND r.ScheduledDeparture >= '{start_datetime}'
                    AND r.ScheduledArrival <= '{end_datetime}'
                    AND t.TYPE IN ({transport_str})

                    UNION ALL

                    SELECT
                        r.ScheduledDeparture,
                        r.ScheduledArrival,
                        r.DestinationLocationID,
                        CONCAT(rc.schedule_departure_path, '->', r.ScheduledDeparture),
                        CONCAT(rc.scheduled_arrival_path, '->', r.ScheduledArrival),
                        CONCAT(rc.source_location_path,'->',r.SourceLocationID),
                        CONCAT(rc.dest_location_path,'->',r.DestinationLocationID),
                        CONCAT(rc.transpotation_path, '->', r.TransportationID),
                        rc.depth + 1,
                        CONCAT(rc.route_path, '->', r.RouteID)
                    FROM route r
                    JOIN transportation t ON r.TransportationID = t.TransportationID
                    JOIN route_chain rc ON r.SourceLocationID = rc.DestinationLocationID
                    WHERE r.ScheduledDeparture >= rc.ScheduledArrival
                    AND r.ScheduledArrival <= '{end_datetime}'
                    AND rc.depth < {num_transfers}
                    AND t.TYPE IN ({transport_str})
                    )

                    SELECT *
                    FROM route_chain
                    WHERE DestinationLocationID = '{st.session_state['locations'][dest_location]}'
                    ORDER BY depth, ScheduledDeparture ASC
                    LIMIT {st.session_state['limit_number']};
                    """
                    result = run_sql(q1)
                    print(
                        "Source Location: ",
                        src_location,
                        st.session_state["locations"][src_location],
                    )
                    print(
                        "Destination Location: ",
                        dest_location,
                        st.session_state["locations"][dest_location],
                    )
                    print("StartDate:", type(start_datetime), start_datetime)
                    print("EndDate:", type(end_datetime), end_datetime)
                    print("num_transfers", num_transfers)
                    print(
                        f"Use plane: {use_plane}, Use ship: {use_ship}, "
                        f"Use bus: {use_bus}, Use train: {use_train}"
                    )
                    st.session_state["query1_result"] = result

        with output_col:
            if "query1_result" not in st.session_state:
                st.write("No result")
            else:
                for item in st.session_state["query1_result"]:
                    st.write(item)

    query_container1_sql = st.container()
    with query_container1_sql:
        with st.expander("Show SQL"):
            if "query1_result" not in st.session_state:
                st.write("Please first make a query")
            else:
                st.code(q1, language="sql")