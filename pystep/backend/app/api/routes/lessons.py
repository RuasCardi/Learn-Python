"""
Lessons Routes
==============

Endpoints para gerenciar lições.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Lesson
from app.schemas import LessonResponse, LessonCreate


router = APIRouter()


@router.get("/", response_model=List[LessonResponse])
async def list_lessons(
    nivel: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todas as lições disponíveis.
    
    Query params:
    - nivel: Filtrar por nível específico
    - skip: Paginação (offset)
    - limit: Número máximo de resultados
    """
    query = db.query(Lesson).filter(Lesson.is_active == True)
    
    if nivel:
        query = query.filter(Lesson.nivel == nivel)
    
    lessons = query.order_by(Lesson.nivel, Lesson.ordem).offset(skip).limit(limit).all()
    return lessons


@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """
    Retorna detalhes de uma lição específica.
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lição não encontrada"
        )
    
    return lesson


@router.post("/", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(lesson_data: LessonCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova lição.
    
    (Admin only - adicionar autenticação depois)
    """
    new_lesson = Lesson(**lesson_data.dict())
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    
    return new_lesson
