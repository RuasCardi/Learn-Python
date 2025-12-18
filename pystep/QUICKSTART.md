# 🚀 GUIA DE INÍCIO RÁPIDO - PyStep

## ⚡ Início Rápido (3 minutos)

### Opção 1: Docker (Recomendado)

```bash
# 1. Clone o projeto
cd pystep

# 2. Configure variáveis de ambiente
cp backend/.env.example backend/.env
# Edite backend/.env e adicione sua OPENAI_API_KEY (opcional)

# 3. Inicie tudo com Docker
docker-compose up --build

# 4. Acesse:
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000
# - Documentação: http://localhost:8000/docs
```

### Opção 2: Desenvolvimento Local

#### Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Edite .env com suas configurações

# Popular banco de dados
python seed_db.py

# Iniciar servidor
uvicorn app.main:app --reload

# API rodando em: http://localhost:8000
```

#### Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar dev server
npm run dev

# App rodando em: http://localhost:5173
```

## 📋 Checklist Pós-Instalação

- [ ] Backend rodando em http://localhost:8000
- [ ] Frontend rodando em http://localhost:5173
- [ ] Documentação acessível em http://localhost:8000/docs
- [ ] Criar uma conta de teste
- [ ] Executar primeiro exercício
- [ ] Ver feedback da IA (se configurou OpenAI)

## 🔧 Configurações Importantes

### Backend (.env)

```bash
# Obrigatório
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///./pystep.db

# Opcional (para IA tutora)
OPENAI_API_KEY=sk-sua-chave-aqui
```

### Frontend (.env)

```bash
VITE_API_URL=http://localhost:8000/api
```

## 🐛 Resolução de Problemas

### Backend não inicia

```bash
# Verificar Python
python --version  # Deve ser 3.10+

# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

### Frontend não inicia

```bash
# Limpar cache e reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Erro de CORS

Verifique se `CORS_ORIGINS` no `.env` do backend inclui a URL do frontend.

### IA não funciona

Se você não tem API key da OpenAI, o sistema usa feedback básico automaticamente.

## 📚 Próximos Passos

1. **Adicionar mais lições**: Edite `backend/seed_db.py`
2. **Customizar frontend**: Modifique componentes em `frontend/src`
3. **Implementar autenticação completa**: Adicionar middleware JWT
4. **Deploy**: Ver seção de deployment no README principal

## 🆘 Precisa de Ajuda?

- Documentação da API: http://localhost:8000/docs
- Erros do backend: Verifique logs no terminal
- Erros do frontend: Abra DevTools do navegador (F12)

---

**🎉 Tudo funcionando? Comece a aprender Python agora!**
