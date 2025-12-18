"""
Database Models
===============

Modelos SQLAlchemy para todas as entidades do sistema.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """Modelo de Usuário"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nome = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    xp = Column(Integer, default=0)
    nivel_atual = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    progress = relationship("UserProgress", back_populates="user")
    submissions = relationship("Submission", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email}>"


class Lesson(Base):
    """Modelo de Lição"""
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    nivel = Column(Integer, nullable=False, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    conteudo = Column(Text)  # Markdown ou HTML com explicação
    ordem = Column(Integer, nullable=False)
    xp_total = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    exercises = relationship("Exercise", back_populates="lesson", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lesson {self.nivel}.{self.ordem} - {self.titulo}>"


class Exercise(Base):
    """Modelo de Exercício"""
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    codigo_inicial = Column(Text, default="# Escreva seu código aqui\n")
    expected_output = Column(Text, nullable=False)
    input_data = Column(Text, default="")  # Dados de entrada (se houver)
    dica = Column(Text)
    xp_reward = Column(Integer, default=10)
    ordem = Column(Integer, nullable=False)
    difficulty = Column(String(50), default="easy")  # easy, medium, hard
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    lesson = relationship("Lesson", back_populates="exercises")
    submissions = relationship("Submission", back_populates="exercise")
    
    def __repr__(self):
        return f"<Exercise {self.id} - {self.titulo}>"


class UserProgress(Base):
    """Progresso do usuário nas lições"""
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    total_attempts = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = relationship("User", back_populates="progress")
    
    def __repr__(self):
        return f"<Progress User:{self.user_id} Lesson:{self.lesson_id}>"


class Submission(Base):
    """Submissões de código dos alunos"""
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    code = Column(Text, nullable=False)
    output = Column(Text)
    error = Column(Text)
    status = Column(String(50))  # success, error
    passed = Column(Boolean, default=False)
    execution_time = Column(Float)
    feedback = Column(Text)  # Feedback da IA
    attempt_number = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = relationship("User", back_populates="submissions")
    exercise = relationship("Exercise", back_populates="submissions")
    
    def __repr__(self):
        return f"<Submission {self.id} - User:{self.user_id} Ex:{self.exercise_id}>"


class Badge(Base):
    """Badges/Conquistas"""
    __tablename__ = "badges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(255))  # URL ou emoji
    condition = Column(String(255))  # Condição para desbloquear
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Badge {self.name}>"


class UserBadge(Base):
    """Badges conquistadas por usuários"""
    __tablename__ = "user_badges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserBadge User:{self.user_id} Badge:{self.badge_id}>"
