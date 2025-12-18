"""
User Lessons Progress Endpoint
==============================

Retorna todas as lições com status de concluída para o usuário.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Lesson, UserProgress
from app.schemas import LessonResponse
from typing import List

router = APIRouter()

@router.get("/user/{user_id}", response_model=List[dict])
def list_lessons_with_progress(user_id: int, db: Session = Depends(get_db)):
    lessons = db.query(Lesson).order_by(Lesson.nivel, Lesson.ordem).all()
    progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    completed = {p.lesson_id for p in progress if p.is_completed}
    result = []
    for idx, lesson in enumerate(lessons):
        is_completed = lesson.id in completed
        # Só libera se for a primeira lição, ou a anterior estiver concluída
        is_unlocked = idx == 0 or lessons[idx-1].id in completed
        result.append({
            **LessonResponse.from_orm(lesson).dict(),
            "is_completed": is_completed,
            "is_unlocked": is_unlocked
        })
    return result
