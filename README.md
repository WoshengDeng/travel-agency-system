# Travel Agency System with Advanced SQL Analytics

## 1. Overview

This project implements a database-driven travel booking system that simulates real-world business scenarios, including transportation, itineraries, accommodations, transactions, and user reviews. The system is built on a relational database model with over 30 entities, designed using EER modeling and fully mapped to a MySQL schema with well-defined primary/foreign keys and integrity constraints.

On top of the database, a set of advanced SQL queries is developed to support complex operations such as multi-leg route planning, analytical reporting, and business data exploration. These queries leverage techniques including recursive CTEs, nested CTEs, window functions, cross joins, and multi-table joins.

To enhance usability, a lightweight interactive interface is implemented using Python and Streamlit, enabling users to explore data and execute queries through a simple visual interface.

**Demo:**  
https://drive.google.com/file/d/19V6AITCCCwUWKZT393pC5ziiz50tApOR/view?usp=drive_link

## 2. Tech Stack

- **Database:** MySQL 8.0  
  - Advanced SQL: Recursive CTEs (`WITH RECURSIVE`), Nested CTEs, Window Functions, Complex Joins  

- **Backend / Data Access:**  
  - Python  
  - mysql-connector-python  

- **Frontend / Interface:**  
  - Streamlit (interactive data exploration & query visualization)

## 3. Key SQL Design Highlights

This project implements 10 advanced queries covering recursive pathfinding, personalized recommendations, multi‑source rating aggregation, and statistical analysis. Below are four representative examples:

| Query | Business Goal | Core SQL Features | Design Highlights |
|-------|---------------|-------------------|--------------------|
| **Query 1** | Multi‑modal route planning (plane, train, bus, ship) with transfer limit and date range | `WITH RECURSIVE`, path concatenation, depth control | Uses a recursive CTE to simulate graph traversal. Dynamically injects source/destination, time window, and allowed transport types. Returns all feasible paths ordered by depth and departure time. |
| **Query 6** | Rank transportation types by delay ratio (least delayed first) | Conditional aggregation, floating‑point ratio calculation | Counts delayed routes per transport type and divides by total routes using `COUNT(CASE WHEN ...) * 1.0 / COUNT(*)`. Orders by delay ratio ascending to identify the most punctual options. |
| **Query 8** | Recommend hotels whose average price is closest to a user’s historical accommodation spending | Multiple CTEs, `UNION ALL`, `CROSS JOIN`, `ABS()` sorting | First computes the user’s average accommodation cost over the past year. Then separately averages prices for hotel rooms and BNBs. A cross join pairs the user’s average with each accommodation’s average, sorting by absolute price difference for personalized ranking. |
| **Query 10** | Generate an overall quality score for each location (combining ratings from transportation, restaurants, activities, and accommodations) | `CROSS JOIN LATERAL`, multi‑source `UNION ALL`, multiple `LEFT JOIN`s | Averages ratings from four sources (transportation reviews, restaurants, activities, accommodations). Uses `CROSS JOIN LATERAL` to flatten the four averages into rows, then groups by location to compute the overall average. Demonstrates MySQL 8.0+ LATERAL syntax in practice. |

For the remaining queries (travel history, transaction cancellation, most popular routes, safest transport type, available seats, user total cost, etc.), please refer to the complete SQL files under [`/queries`](queries/advanced_queries.sql) and the corresponding Python modules in [`/app/queries`](app/queries).

## 4. Database Design

The system models a realistic travel agency with **30 entities**, covering transportation, accommodation, trips, transactions, reviews, and customer support. The design follows a rigorous data modeling process:

- **EER Model** – Defined entities, attributes, relationships, and inheritance hierarchies (e.g., `transportation` specialized into `plane`, `ship`, `train`, `bus`, `car`; `accommodation` specialized into `hotel` and `bnb`).  
- **Mapping to Relational Schema** – Transformed the EER model into a set of relational tables with primary keys, foreign keys, and integrity constraints (e.g., CHECK constraints for status values, date ordering, and positive capacities).  
- **Polymorphic Associations** – Used a `TargetID` + `TargetType` pattern in the `transaction` table to reference different target types (`Trip`, `Accommodation`, `Restaurant`, etc.), enabling a flexible payment and review system.  
- **Advanced Constraints** – Enforced business rules such as `ScheduledDeparture < ScheduledArrival`, `StartDate <= EndDate`, and recursive foreign key references for route–unit relationships.

For the complete EER diagram and relational schema, see:
- [`docs/eer_diagram.png`](docs/eer_diagram.png) – Entity‑relationship model with inheritance.  
- [`docs/relational_schema.pdf`](docs/relational_schema.pdf) – Detailed table definitions, keys, and constraints.

## 5. System Architecture

The project follows a clear separation of concerns, dividing the system into three logical layers:

- **Database Layer** – MySQL 8.0+ stores all 30 entities, enforces integrity constraints, and executes complex queries (recursive CTEs, window functions, etc.).  
- **Application Layer** – Streamlit (Python) serves as the interactive frontend. The code is modularized into database connection handlers, configuration constants, and per‑query UI modules.  
- **Artifacts Layer** – Design documentation (EER diagram, relational schema) and demonstration assets are kept separately for easy reference.

Below is the complete directory structure:

```text
travel-agency-system/
├── README.md                # Project overview and documentation
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies for the app
│
├── database/               # Database schema and initial data
│   ├── schema.sql          # DDL: tables, constraints, relationships
│   └── seed.sql            # Sample data for testing and demo
│
├── queries/                # Standalone advanced SQL queries
│   └── advanced_queries.sql # Core SQL logic showcased in README
│
├── app/                    # Streamlit application (interface layer)
│   ├── streamlit_app.py    # Main entry point for the app
│   ├── config.py           # Configuration (DB settings, constants)
│   │
│   ├── db/                 # Database connection and initialization
│   │   ├── __init__.py
│   │   ├── connection.py   # MySQL connection handling
│   │   └── init_db.py      # Database initialization utilities
│   │
│   ├── queries/            # Python-wrapped SQL queries (modularized)
│   │   ├── __init__.py
│   │   ├── query01.py
│   │   ├── query02.py
│   │   ├── ...
│   │   └── query10.py
│   │
│   └── utils/              # Helper functions and shared utilities
│       ├── __init__.py
│       └── helpers.py
│
└── docs/                   # Design documentation
    ├── eer_diagram.png     # EER model diagram
    └── relational_schema.pdf # Relational schema design
```

**Key Design Choices:**

- **Modular queries** – Each of the 10 advanced queries lives in its own Python module under `app/queries/`, making the codebase maintainable and scalable.  
- **Centralized configuration** – All hard‑coded values (location IDs, test user accounts, display limits) are stored in `config.py`.  
- **Session state management** – Streamlit’s session state holds the database connection and query results, enabling responsive UI without redundant execution.  
- **SQL as documentation** – The complete set of queries is also available as a standalone `advanced_queries.sql` file for quick inspection outside the Python environment.

## 6. How to Run

The project can be run locally with a MySQL instance and Python environment.

**Requirements:**
- MySQL 8.0+
- Python 3.8+

**Steps:**
```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py