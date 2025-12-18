"""
Execute Routes
==============

Endpoints para execução de código Python.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import User, Exercise, Submission
from app.schemas import CodeExecutionRequest, CodeExecutionResponse
from app.services.executor import executor
from app.services.ai_tutor import ai_tutor


router = APIRouter()


@router.post("/", response_model=CodeExecutionResponse)
async def execute_code(
    request: CodeExecutionRequest,
    db: Session = Depends(get_db)
):
    """
    Executa código Python do aluno e retorna resultado + feedback da IA.
    
    Fluxo:
    1. Busca exercício
    2. Executa código no sandbox
    3. Analisa com IA
    4. Salva submissão
    5. Atualiza XP (se passou)
    """
    
    # Buscar exercício
    exercise = db.query(Exercise).filter(Exercise.id == request.exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercício não encontrado"
        )
    
    # Executar código
    result = executor.test_code(
        code=request.code,
        expected_output=exercise.expected_output
    )
    
    # Contar tentativas do usuário neste exercício
    # (Simplificado: em produção, pegar user_id do token)
    attempt_number = 1
    
    # Análise da IA
    ai_feedback = ai_tutor.analyze_code(
        code=request.code,
        execution_result=result,
        exercise_description=exercise.descricao,
        expected_output=exercise.expected_output,
        attempt_number=attempt_number
    )
    
    # Salvar submissão no banco
    # submission = Submission(
    #     user_id=user_id,  # Pegar do token
    #     exercise_id=exercise.id,
    #     code=request.code,
    #     output=result["output"],
    #     error=result["error"],
    #     status=result["status"],
    #     passed=result.get("passed", False),
    #     execution_time=result["execution_time"],
    #     feedback=str(ai_feedback),
    #     attempt_number=attempt_number
    # )
    # db.add(submission)
    # db.commit()
    
    # Preparar resposta
    response = CodeExecutionResponse(
        output=result["output"],
        error=result["error"],
        status=result["status"],
        execution_time=result["execution_time"],
        passed=result.get("passed"),
        expected=result.get("expected"),
        actual=result.get("actual"),
        feedback=ai_feedback,
        xp_gained=ai_feedback.get("xp_gained", 0) if result.get("passed") else 0
    )
    
    return response


@router.post("/hint")
async def get_hint(
    exercise_id: int,
    current_code: str,
    db: Session = Depends(get_db)
):
    """
    Solicita uma dica da IA para o exercício atual.
    """
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercício não encontrado"
        )
    
    # Gerar dica com IA
    hint = ai_tutor.generate_hint(
        exercise_description=exercise.descricao,
        current_code=current_code
    )
    
    return {"hint": hint}
