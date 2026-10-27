from typing import Protocol

from lab4.domain import Teacher


class RepositoryError(Exception):
    """Base error of the storage layer."""


class DuplicateError(RepositoryError):
    """A record with the same unique value already exists."""


class InvalidReferenceError(RepositoryError):
    """The record refers to a related record that does not exist."""


class TeacherRepository(Protocol):
    def list_all(self) -> list[Teacher]: ...

    def get(self, teacher_id: int) -> Teacher | None: ...

    def create(self, teacher: Teacher) -> Teacher: ...

    def update(self, teacher_id: int, teacher: Teacher) -> Teacher | None: ...

    def delete(self, teacher_id: int) -> bool: ...
