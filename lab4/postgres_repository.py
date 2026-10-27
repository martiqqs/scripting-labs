import psycopg
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from psycopg.rows import class_row

from lab4.domain import Teacher
from lab4.repository import DuplicateError, InvalidReferenceError

COLUMNS = "teacher_id, full_name, address, position, email, phone, department_id"
SELECT_TEACHERS = "SELECT " + COLUMNS + " FROM teachers"
RETURNING = " RETURNING " + COLUMNS


def _params(teacher: Teacher) -> tuple[str | int | None, ...]:
    return (
        teacher.full_name,
        teacher.address,
        teacher.position,
        teacher.email,
        teacher.phone,
        teacher.department_id,
    )


class PostgresTeacherRepository:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    def _connect(self) -> psycopg.Connection[Teacher]:
        return psycopg.connect(self._dsn, row_factory=class_row(Teacher))

    def list_all(self) -> list[Teacher]:
        with self._connect() as conn:
            query = SELECT_TEACHERS + " ORDER BY teacher_id"
            return conn.execute(query).fetchall()

    def get(self, teacher_id: int) -> Teacher | None:
        with self._connect() as conn:
            query = SELECT_TEACHERS + " WHERE teacher_id = %s"
            return conn.execute(query, (teacher_id,)).fetchone()

    def create(self, teacher: Teacher) -> Teacher:
        query = (
            "INSERT INTO teachers "
            "(full_name, address, position, email, phone, department_id) "
            "VALUES (%s, %s, %s, %s, %s, %s)" + RETURNING
        )
        try:
            with self._connect() as conn:
                row = conn.execute(query, _params(teacher)).fetchone()
        except UniqueViolation as exc:
            raise DuplicateError("Email already exists") from exc
        except ForeignKeyViolation as exc:
            raise InvalidReferenceError("Department does not exist") from exc
        if row is None:
            raise RuntimeError("INSERT returned no row")
        return row

    def update(self, teacher_id: int, teacher: Teacher) -> Teacher | None:
        query = (
            "UPDATE teachers SET full_name = %s, address = %s, position = %s, "
            "email = %s, phone = %s, department_id = %s "
            "WHERE teacher_id = %s" + RETURNING
        )
        try:
            with self._connect() as conn:
                return conn.execute(query, _params(teacher) + (teacher_id,)).fetchone()
        except UniqueViolation as exc:
            raise DuplicateError("Email already exists") from exc
        except ForeignKeyViolation as exc:
            raise InvalidReferenceError("Department does not exist") from exc

    def delete(self, teacher_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                "DELETE FROM teachers WHERE teacher_id = %s", (teacher_id,)
            )
            return cur.rowcount > 0
