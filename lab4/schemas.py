import re

from pydantic import BaseModel, Field, field_validator

EMAIL_RE = re.compile(r"^[a-z]+\.[a-z]+@lpnu\.ua$")
PHONE_RE = re.compile(r"^\+380[0-9]{9}$")


class TeacherIn(BaseModel):
    full_name: str = Field(min_length=3, max_length=150)
    address: str | None = None
    position: str = Field(min_length=2, max_length=50)
    email: str
    phone: str
    department_id: int

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not EMAIL_RE.fullmatch(value):
            raise ValueError("email must look like name.surname@lpnu.ua")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not PHONE_RE.fullmatch(value):
            raise ValueError("phone must start with +380 and have 9 more digits")
        return value
