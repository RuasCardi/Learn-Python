"""
Progress Routes
===============

Endpoints para acompanhar progresso do aluno.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import UserProgress, User
from app.schemas import ProgressResponse, UserProgressSummary


router = APIRouter()


@router.get("/{user_id}", response_model=UserProgressSummary)
async def get_user_progress(user_id: int, db: Session = Depends(get_db)):
    """
    Retorna resumo completo do progresso do usuário.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Calcular estatísticas
    # (Implementação simplificada)
    
    return {
        "total_xp": user.xp,
        "nivel_atual": user.nivel_atual,
        "lessons_completed": 0,
        "total_lessons": 0,
        "exercises_completed": 0,
        "total_exercises": 0,
        "success_rate": 0.0,
        "recent_activity": []
    }


@router.post("/complete")
async def mark_lesson_complete(
    user_id: int,
    lesson_id: int,
    db: Session = Depends(get_db)
):
    """
    Marca uma lição como completa.
    """
    # Implementação simplificada
    return {"message": "Lição marcada como completa"}
