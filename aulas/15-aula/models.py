from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Aluno(Base):
    __tablename__ = 'alunos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(50), nullable=False)
    
    inscriptions = relationship("Inscription", back_populates="aluno")
    
class Curso(Base):
    __tablename__ = 'cursos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)

    inscriptions = relationship("Inscription", back_populates="curso")
    
class Inscription(Base):
    __tablename__ = 'inscricoes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    
    aluno = relationship("Aluno", back_populates="inscricoes")
    curso = relationship("Curso", back_populates="inscricoes")