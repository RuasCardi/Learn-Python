"""
Exercises Routes
================

Endpoints para gerenciar exercícios.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Exercise
from app.schemas import ExerciseResponse, ExerciseCreate


router = APIRouter()


@router.get("/", response_model=List[ExerciseResponse])
async def list_exercises(
    lesson_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Lista exercícios (opcionalmente filtrados por lição).
    """
    query = db.query(Exercise)
    
    if lesson_id:
        query = query.filter(Exercise.lesson_id == lesson_id)
    
    exercises = query.order_by(Exercise.ordem).all()
    return exercises


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """
    Retorna detalhes de um exercício específico.
    """
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercício não encontrado"
        )
    
    return exercise


@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(exercise_data: ExerciseCreate, db: Session = Depends(get_db)):
    """
    Cria um novo exercício.
    
    (Admin only - adicionar autenticação depois)
    """
    new_exercise = Exercise(**exercise_data.dict())
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    
    return new_exercise
