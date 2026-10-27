from dataclasses import dataclass


@dataclass
class Department:
    department_id: int | None
    department_name: str


@dataclass
class Teacher:
    teacher_id: int | None
    full_name: str
    address: str | None
    position: str
    email: str
    phone: str
    department_id: int


@dataclass
class Discipline:
    discipline_id: int | None
    discipline_name: str
    hours_count: int
    control_type: str


@dataclass
class TeachingAssignment:
    assignment_id: int | None
    teacher_id: int
    discipline_id: int
    classroom_number: str