"""
FastAPI Main Application
=========================

Ponto de entrada principal da API PyStep.
Configura rotas, middleware e inicialização.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import auth, lessons, exercises, execute, progress, user_lessons


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup: Criar tabelas do banco
    Base.metadata.create_all(bind=engine)
    print("🚀 PyStep API iniciada!")
    print(f"📚 Banco de dados: {settings.DATABASE_URL}")
    yield
    # Shutdown
    print("👋 PyStep API encerrada")


# Inicializar FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Plataforma progressiva de ensino de Python com IA",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rotas principais
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(lessons.router, prefix="/api/lessons", tags=["Lições"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["Exercícios"])
app.include_router(execute.router, prefix="/api/execute", tags=["Execução"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progresso"])
app.include_router(user_lessons.router, prefix="/api/lessons", tags=["Lições do Usuário"])


@app.get("/")
async def root():
    """Endpoint raiz - health check"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "message": "🐍 PyStep API - Aprenda Python fazendo!"
    }


@app.get("/health")
async def health_check():
    """Health check para monitoramento"""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


# Handler de erros global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Captura exceções não tratadas"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.DEBUG else "Ocorreu um erro interno"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
