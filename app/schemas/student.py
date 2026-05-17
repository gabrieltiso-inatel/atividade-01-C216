from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    course: str


class Student(BaseModel):
    id: str
    name: str
    email: str
    course: str
    registration: int
