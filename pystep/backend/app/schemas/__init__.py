"""
Pydantic Schemas
================

Schemas para validação de entrada/saída da API.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ============= USER SCHEMAS =============

class UserBase(BaseModel):
    email: EmailStr
    nome: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    xp: int
    nivel_atual: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ============= LESSON SCHEMAS =============

class LessonBase(BaseModel):
    nivel: int
    titulo: str
    descricao: str
    conteudo: Optional[str] = None
    ordem: int


class LessonCreate(LessonBase):
    pass


class LessonResponse(LessonBase):
    id: int
    xp_total: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= EXERCISE SCHEMAS =============

class ExerciseBase(BaseModel):
    titulo: str
    descricao: str
    codigo_inicial: str = "# Escreva seu código aqui\n"
    expected_output: str
    input_data: str = ""
    dica: Optional[str] = None
    xp_reward: int = 10
    ordem: int
    difficulty: str = "easy"


class ExerciseCreate(ExerciseBase):
    lesson_id: int


class ExerciseResponse(ExerciseBase):
    id: int
    lesson_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= EXECUTION SCHEMAS =============

class CodeExecutionRequest(BaseModel):
    code: str
    exercise_id: int
    input_data: str = ""


class CodeExecutionResponse(BaseModel):
    output: str
    error: str
    status: str  # "success" ou "error"
    execution_time: float
    passed: Optional[bool] = None
    expected: Optional[str] = None
    actual: Optional[str] = None
    feedback: Optional[dict] = None
    xp_gained: Optional[int] = 0


# ============= PROGRESS SCHEMAS =============

class ProgressBase(BaseModel):
    lesson_id: int
    is_completed: bool = False


class ProgressCreate(ProgressBase):
    user_id: int


class ProgressResponse(ProgressBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None
    total_attempts: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserProgressSummary(BaseModel):
    """Resumo do progresso do usuário"""
    total_xp: int
    nivel_atual: int
    lessons_completed: int
    total_lessons: int
    exercises_completed: int
    total_exercises: int
    success_rate: float
    recent_activity: List[dict]


# ============= SUBMISSION SCHEMAS =============

class SubmissionResponse(BaseModel):
    id: int
    exercise_id: int
    code: str
    passed: bool
    feedback: Optional[str]
    attempt_number: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= HINT REQUEST =============

class HintRequest(BaseModel):
    exercise_id: int
    current_code: str
