"""
Authentication Routes
=====================

Endpoints para registro, login e gerenciamento de usuários.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.core.config import settings
from app.models import User
from app.schemas import UserCreate, UserLogin, Token, UserResponse


router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registra um novo usuário.
    
    - Valida email único
    - Cria hash da senha
    - Retorna token de acesso
    """
    # Verificar se email já existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Criar novo usuário
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        nome=user_data.nome,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Gerar token
    access_token = create_access_token(data={"sub": str(new_user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": new_user
    }


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Autentica usuário e retorna token JWT.
    """
    # Buscar usuário
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    # Gerar token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str = Depends(lambda: None),  # Você pode adicionar um dependency para extrair token
    db: Session = Depends(get_db)
):
    """
    Retorna informações do usuário autenticado.
    
    Requer: Bearer token no header Authorization
    """
    # Este é um exemplo simplificado
    # Na prática, você deve implementar um dependency que extrai e valida o token
    
    # Exemplo de extração de token (implementar corretamente)
    # from fastapi.security import HTTPBearer
    
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Endpoint em desenvolvimento"
    )
