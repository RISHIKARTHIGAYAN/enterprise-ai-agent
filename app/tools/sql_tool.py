import sqlite3

from app.config import PROJECT_ROOT


DATABASE_PATH = PROJECT_ROOT / "data" / "db" / "enterprise.db"


class SQLTool:
    def __init__(self):
        DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def _get_connection(self):
        return sqlite3.connect(DATABASE_PATH)

    def _initialize_database(self):
        connection = self._get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS employees (
                    employee_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    role TEXT NOT NULL,
                    location TEXT NOT NULL,
                    years_at_company REAL NOT NULL
                )
                """
            )

            cursor.execute("SELECT COUNT(*) FROM employees")
            count = cursor.fetchone()[0]

            if count == 0:
                employees = [
                    (
                        1001,
                        "Alice",
                        "Engineering",
                        "Software Engineer",
                        "Bangalore",
                        3.5,
                    ),
                    (
                        1002,
                        "Bob",
                        "Engineering",
                        "ML Engineer",
                        "Chennai",
                        2.0,
                    ),
                    (
                        1003,
                        "Charlie",
                        "Finance",
                        "Financial Analyst",
                        "Mumbai",
                        4.0,
                    ),
                    (
                        1004,
                        "Diana",
                        "Human Resources",
                        "HR Manager",
                        "Bangalore",
                        6.0,
                    ),
                    (
                        1005,
                        "Ethan",
                        "Engineering",
                        "Data Engineer",
                        "Hyderabad",
                        1.5,
                    ),
                    (
                        1006,
                        "Fiona",
                        "Marketing",
                        "Marketing Specialist",
                        "Delhi",
                        2.5,
                    ),
                    (
                        1007,
                        "George",
                        "Finance",
                        "Accountant",
                        "Chennai",
                        5.0,
                    ),
                    (
                        1008,
                        "Hannah",
                        "Engineering",
                        "DevOps Engineer",
                        "Pune",
                        3.0,
                    ),
                ]

                cursor.executemany(
                    """
                    INSERT INTO employees (
                        employee_id,
                        name,
                        department,
                        role,
                        location,
                        years_at_company
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    employees,
                )

                connection.commit()

        finally:
            connection.close()

    def run(self, query: str):
        connection = self._get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()

            if cursor.description is None:
                return {
                    "tool": "sql",
                    "query": query,
                    "results": [],
                    "row_count": 0,
                }

            columns = [
                description[0]
                for description in cursor.description
            ]

            results = [
                dict(zip(columns, row))
                for row in rows
            ]

            return {
                "tool": "sql",
                "query": query,
                "results": results,
                "row_count": len(results),
            }

        except Exception as error:
            return {
                "tool": "sql",
                "query": query,
                "error": str(error),
            }

        finally:
            connection.close()

    def close(self):
        # Connections are created per operation,
        # so there is no persistent connection to close.
        pass