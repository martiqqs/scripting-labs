from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Response, status

from lab4.domain import Teacher
from lab4.postgres_repository import PostgresTeacherRepository
from lab4.repository import DuplicateError, InvalidReferenceError, TeacherRepository
from lab4.schemas import TeacherIn

DSN = "postgresql://postgres:postgres@localhost:5432/postgres"

app = FastAPI(title="Кафедра БІТ API")


def get_repository() -> TeacherRepository:
    return PostgresTeacherRepository(DSN)


RepoDep = Annotated[TeacherRepository, Depends(get_repository)]


def to_domain(data: TeacherIn, teacher_id: int | None = None) -> Teacher:
    return Teacher(
        teacher_id=teacher_id,
        full_name=data.full_name,
        address=data.address,
        position=data.position,
        email=data.email,
        phone=data.phone,
        department_id=data.department_id,
    )


@app.get("/teachers")
def list_teachers(repo: RepoDep) -> list[Teacher]:
    return repo.list_all()


@app.get("/teachers/{teacher_id}")
def get_teacher(teacher_id: int, repo: RepoDep) -> Teacher:
    teacher = repo.get(teacher_id)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@app.post("/teachers", status_code=status.HTTP_201_CREATED)
def create_teacher(data: TeacherIn, repo: RepoDep) -> Teacher:
    try:
        return repo.create(to_domain(data))
    except DuplicateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except InvalidReferenceError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: int, data: TeacherIn, repo: RepoDep) -> Teacher:
    try:
        teacher = repo.update(teacher_id, to_domain(data, teacher_id))
    except DuplicateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except InvalidReferenceError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@app.delete("/teachers/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id: int, repo: RepoDep) -> Response:
    if not repo.delete(teacher_id):
        raise HTTPException(status_code=404, detail="Teacher not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
