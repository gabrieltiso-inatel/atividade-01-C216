from typing import List
from app.schemas.student import Student, StudentCreate
from app.db.connection import get_connection


class StudentService:
    async def list_all(self) -> List[Student]:
        conn = await get_connection()
        try:
            rows = await conn.fetch("SELECT * FROM students ORDER BY id")
            return [
                Student(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    course=row["course"],
                    registration=row["registration"]
                )
                for row in rows
            ]
        finally:
            await conn.close()

    async def find_by_id(self, student_id: str) -> Student | None:
        conn = await get_connection()
        try:
            row = await conn.fetchrow("SELECT * FROM students WHERE id=$1", student_id)
            if row:
                return Student(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    course=row["course"],
                    registration=row["registration"]
                )
            return None
        finally:
            await conn.close()

    async def create(self, student_data: StudentCreate) -> Student:
        conn = await get_connection()
        try:
            course = student_data.course

            # Get or initialize counter for this course
            counter_row = await conn.fetchrow(
                "SELECT counter FROM registration_counters WHERE course=$1",
                course
            )

            if counter_row:
                registration = counter_row["counter"] + 1
            else:
                registration = 1

            # Update counter
            await conn.execute(
                """
                INSERT INTO registration_counters (course, counter) VALUES ($1, $2)
                ON CONFLICT (course) DO UPDATE SET counter = $2
                """,
                course,
                registration
            )

            student_id = f"{course}{registration}"

            # Insert student
            row = await conn.fetchrow(
                """
                INSERT INTO students (id, name, email, course, registration)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING *
                """,
                student_id,
                student_data.name,
                student_data.email,
                course,
                registration
            )

            return Student(
                id=row["id"],
                name=row["name"],
                email=row["email"],
                course=row["course"],
                registration=row["registration"]
            )
        finally:
            await conn.close()

    async def update(self, student_id: str, student_data: StudentCreate) -> Student | None:
        conn = await get_connection()
        try:
            row = await conn.fetchrow(
                """
                UPDATE students
                SET name=$1, email=$2, course=$3
                WHERE id=$4
                RETURNING *
                """,
                student_data.name,
                student_data.email,
                student_data.course,
                student_id
            )

            if row:
                return Student(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    course=row["course"],
                    registration=row["registration"]
                )
            return None
        finally:
            await conn.close()

    async def delete(self, student_id: str) -> bool:
        conn = await get_connection()
        try:
            result = await conn.execute("DELETE FROM students WHERE id=$1", student_id)
            return result == "DELETE 1"
        finally:
            await conn.close()

    async def reset(self) -> None:
        conn = await get_connection()
        try:
            await conn.execute("DELETE FROM students")
            await conn.execute("DELETE FROM registration_counters")
        finally:
            await conn.close()
