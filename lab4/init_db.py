from pathlib import Path

import psycopg

DSN = "postgresql://postgres:postgres@localhost:5432/postgres"
SQL_FILE = Path(__file__).parent / "init.sql"

COUNT_QUERY = """
SELECT 'departments' AS table_name, COUNT(*) FROM departments
UNION ALL
SELECT 'teachers', COUNT(*) FROM teachers
UNION ALL
SELECT 'disciplines', COUNT(*) FROM disciplines
UNION ALL
SELECT 'teaching_assignments', COUNT(*) FROM teaching_assignments
"""


def init_db() -> None:
    """Create tables and insert test data from init.sql."""
    script = SQL_FILE.read_text(encoding="utf-8")
    with psycopg.connect(DSN) as conn:
        conn.execute(script)
        rows = conn.execute(COUNT_QUERY).fetchall()
    total = 0
    for table_name, count in rows:
        print(f"{table_name}: {count}")
        total += count
    print(f"Total records: {total}")


if __name__ == "__main__":
    init_db()