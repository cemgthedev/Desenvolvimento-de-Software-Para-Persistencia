from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import *

app = FastAPI()

@app.post("/alunos")
def create_aluno(aluno: str, email: str, password: str, db: Session = Depends(get_db)):
    aluno = Aluno(name=aluno, email=email, password=password)
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno

@app.get("/alunos")
def get_alunos(db: Session = Depends(get_db)):
    alunos = db.query(Aluno).all()
    return alunos

@app.post("/cursos")
def create_curso(curso: str, description: str, db: Session = Depends(get_db)):
    curso = Curso(name=curso, description=description)
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso

@app.get("/cursos")
def get_cursos(db: Session = Depends(get_db)):
    cursos = db.query(Curso).all()
    return cursos

@app.post("/inscriptions")
def create_inscription(aluno_id: int, curso_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    
    if aluno and curso:
        inscricao = Inscription(aluno=aluno, curso=curso)
        db.add(inscricao)
        db.commit()
        db.refresh(inscricao)
        return inscricao
    
@app.get("/inscriptions")
def get_inscriptions(db: Session = Depends(get_db)):
    inscricoes = db.query(Inscription).all()
    return inscricoes