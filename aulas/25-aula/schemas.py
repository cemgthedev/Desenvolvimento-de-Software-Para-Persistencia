from pydantic import BaseModel, Field

from typing import Optional, List

class Teacher(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(min_length=3, max_length=100)
    specialty: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=20)
    
class Course(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=2000)
    workload: int = Field(ge=1)
    teacher_id: int
    students: Optional[List[str]] = []
    
class Student(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(min_length=3, max_length=100)
    email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=20)
    courses: Optional[List[str]] = []
    
class Classroom(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=2000)
    teacher_id: int
    course_id: int
    students: Optional[List[str]] = []
    
class Department(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=2000)
    chef_id: Optional[int]
    teachers: Optional[List[str]] = []
    classrooms: Optional[List[str]] = []