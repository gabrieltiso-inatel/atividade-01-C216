from fastapi import FastAPI
from app.routes.student_routes import router as student_router
from app.middlewares.logging import log_requests
from app.middlewares.custom_header import add_custom_header

app = FastAPI(
    title="Student Management API",
    description="API for student management with CRUD operations",
    version="1.0.0"
)

app.middleware("http")(log_requests)
app.middleware("http")(add_custom_header)

app.include_router(student_router)


@app.get("/")
def root():
    return {"message": "API working 🚀"}