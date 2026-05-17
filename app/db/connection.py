import asyncpg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/students_db"
)


async def get_connection():
    """Get an async connection to PostgreSQL"""
    return await asyncpg.connect(DATABASE_URL)
