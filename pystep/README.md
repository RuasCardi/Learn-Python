# 🐍 PyStep - Plataforma Progressiva de Ensino de Python

> **Aprenda Python fazendo, com feedback inteligente em tempo real**

## 🎯 Visão Geral

PyStep é uma plataforma web interativa que ensina Python através de prática guiada por IA. O sistema oferece:

- ✨ **Aprendizado Progressivo**: Do zero ao avançado, passo a passo
- 🤖 **IA Tutora Integrada**: Feedback personalizado e inteligente
- 🎮 **Gamificação**: XP, níveis e conquistas
- 💻 **Editor Real**: Monaco Editor (VSCode no navegador)
- 🔒 **Execução Segura**: Sandbox isolado para código Python
- 📊 **Acompanhamento**: Progresso detalhado e métricas

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────┐
│           BROWSER (Cliente)                 │
│  React + Monaco Editor + TailwindCSS        │
└──────────────────┬──────────────────────────┘
                   │ REST API / WebSocket
┌──────────────────▼──────────────────────────┐
│        BACKEND (FastAPI + Python)           │
│  Auth │ Lessons │ Execute │ AI Tutor        │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│     SANDBOX + DATABASE + AI ENGINE          │
│  Isolated Execution │ SQLite │ OpenAI       │
└─────────────────────────────────────────────┘
```

## 📦 Estrutura do Projeto

```
pystep/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── core/           # Config, segurança, DB
│   │   ├── models/         # Modelos SQLAlchemy
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Lógica de negócio
│   │   │   ├── auth.py
│   │   │   ├── executor.py      # Sandbox Python
│   │   │   ├── ai_tutor.py      # IA feedback
│   │   │   └── lessons.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/               # React SPA
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── pages/         # Páginas
│   │   ├── hooks/         # Custom hooks
│   │   ├── services/      # API calls
│   │   ├── store/         # Estado global
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Pré-requisitos

- Python 3.10+
- Node.js 18+
- Docker (opcional)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API disponível em: `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App disponível em: `http://localhost:5173`

### Docker (Recomendado)

```bash
docker-compose up --build
```

## 🎮 Funcionalidades Principais

### 1. Sistema de Níveis Progressivos

- **Nível 1**: Conceitos básicos (print, variáveis)
- **Nível 2**: Operações e tipos
- **Nível 3**: Condicionais
- **Nível 4**: Loops
- **Nível 5**: Funções
- **Nível 6+**: Estruturas de dados, OOP, etc.

### 2. Execução Segura de Código

```python
# Sandbox isolado com:
- Timeout de 2 segundos
- Memória limitada (128MB)
- Sem acesso a sistema de arquivos
- Imports restritos
- Captura de stdout/stderr
```

### 3. IA Tutora Inteligente

A IA analisa:
- ✅ **Sintaxe**: Erros de código
- ✅ **Lógica**: Raciocínio do aluno
- ✅ **Boas Práticas**: Code style
- ✅ **Progressão**: Dicas personalizadas

**Exemplo de Feedback:**
```
❌ Seu código tem um pequeno erro de lógica.
💡 Dica: Você está somando, mas o exercício pede multiplicação.
🎯 Tente novamente! Você está quase lá.
```

### 4. Gamificação

- 🏆 **XP por exercício completado**
- ⭐ **Níveis progressivos**
- 🎖️ **Badges de conquistas**
- 📈 **Dashboard de progresso**

## 🔌 API Endpoints

### Autenticação
```
POST /api/auth/register    # Cadastro
POST /api/auth/login       # Login
GET  /api/auth/me          # Perfil do usuário
```

### Lições e Exercícios
```
GET  /api/lessons          # Listar lições
GET  /api/lessons/{id}     # Detalhes da lição
GET  /api/exercises/{id}   # Exercício específico
```

### Execução de Código
```
POST /api/execute          # Executar código Python
Body: {
  "code": "print('Hello')",
  "exercise_id": 1,
  "user_id": 1
}

Response: {
  "output": "Hello\n",
  "status": "success",
  "feedback": "Perfeito! 🎉",
  "xp_gained": 10
}
```

### Progresso
```
GET  /api/progress/{user_id}     # Progresso do usuário
POST /api/progress/complete      # Marcar exercício completo
```

## 🧪 Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno
- **SQLAlchemy**: ORM para banco de dados
- **Pydantic**: Validação de dados
- **JWT**: Autenticação
- **OpenAI API**: IA tutora
- **Docker**: Containerização

### Frontend
- **React 18**: Framework UI
- **Vite**: Build tool
- **Monaco Editor**: Editor de código
- **TailwindCSS**: Estilização
- **Zustand**: Gerenciamento de estado
- **Axios**: HTTP client
- **React Router**: Navegação

## 🔐 Segurança

- ✅ Autenticação JWT
- ✅ Execução sandbox isolada
- ✅ Rate limiting
- ✅ Validação de input
- ✅ CORS configurado
- ✅ Variáveis de ambiente

## 📊 Modelo de Dados

### User
```python
{
  "id": int,
  "email": str,
  "nome": str,
  "xp": int,
  "nivel_atual": int,
  "created_at": datetime
}
```

### Lesson
```python
{
  "id": int,
  "nivel": int,
  "titulo": str,
  "descricao": str,
  "ordem": int
}
```

### Exercise
```python
{
  "id": int,
  "lesson_id": int,
  "titulo": str,
  "descricao": str,
  "codigo_inicial": str,
  "expected_output": str,
  "dica": str,
  "xp_reward": int
}
```

## 🎯 Roadmap

### ✅ Fase 1 - MVP (Em Desenvolvimento)
- [x] Estrutura do projeto
- [x] Backend FastAPI
- [x] Execução sandbox
- [x] IA tutora básica
- [ ] Frontend React
- [ ] Sistema de autenticação
- [ ] Primeiras 10 lições

### 🟡 Fase 2 - Experiência
- [ ] Animações e transições
- [ ] Dashboard detalhado
- [ ] Sistema de badges
- [ ] IA mais inteligente
- [ ] Visualizações de código

### 🔵 Fase 3 - Escala
- [ ] App mobile (React Native)
- [ ] Certificados
- [ ] Comunidade/Fórum
- [ ] Desafios semanais
- [ ] Multiplayer coding

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Guilherme Cardinalli**

---

⭐ **Diferencial do PyStep**: Não é apenas teoria - é treinamento cognitivo de programador.
