from fastapi import APIRouter, HTTPException
from config import db

from schemas import Student
from typing import List, Dict, Any
from bson import ObjectId

router = APIRouter()

@router.post("/students", response_model=Student)
async def create_student(student: Student):
    student_dict = Dict(student)
    student_dict["id"] = str(ObjectId())
    db.students.insert_one(student_dict)
    return student

@router.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: str, student: Student):
    student_dict = Dict(student)
    db.students.update_one({"id": student_id}, {"$set": student_dict})
    return student

@router.delete("/students/{student_id}")
async def delete_student(student_id: str, response_model=Any):
    db.students.delete_one({"id": student_id})
    return {"message": "Aluno deletado com sucesso!"}

@router.get("/students", response_model=List[Student])
async def get_all_students():
    return List(db.students.find())

@router.get("/students/{student_id}", response_model=Student)
async def get_student_by_id(student_id: str):
    return Dict(db.students.find_one({"id": student_id}))