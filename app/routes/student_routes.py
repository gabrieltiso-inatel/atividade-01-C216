from fastapi import APIRouter, HTTPException
from app.schemas.student import Student, StudentCreate
from app.services.student_service import StudentService

router = APIRouter()
service = StudentService()


@router.get("/api/v1/alunos/", response_model=list[Student])
async def list_students():
    return await service.list_all()


@router.get("/api/v1/alunos/{student_id}", response_model=Student)
async def get_student(student_id: str):
    student = await service.find_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/api/v1/alunos/", response_model=Student)
async def create_student(student: StudentCreate):
    return await service.create(student)


@router.patch("/api/v1/alunos/{student_id}", response_model=Student)
async def update_student(student_id: str, student: StudentCreate):
    updated = await service.update(student_id, student)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@router.delete("/api/v1/alunos/{student_id}")
async def delete_student(student_id: str):
    success = await service.delete(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}


@router.delete("/api/v1/alunos/")
async def reset_students():
    await service.reset()
    return {"message": "All students have been deleted"}
