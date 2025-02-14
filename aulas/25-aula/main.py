from fastapi import APIRouter
from student_routes import router as student_routes

router = APIRouter()
router.name = "Alunos"

router.include_router(student_routes)