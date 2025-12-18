"""
Seed Script - População Inicial do Banco de Dados
==================================================

Popula o banco com lições e exercícios iniciais.
"""

from datetime import datetime
from app.core.database import SessionLocal, engine, Base
from app.models import Lesson, Exercise

# Criar todas as tabelas
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Limpar dados existentes (cuidado em produção!)
db.query(Exercise).delete()
db.query(Lesson).delete()
db.commit()

print("🌱 Populando banco de dados com lições iniciais...")

# ==================== NÍVEL 1 ====================

lesson1 = Lesson(
    nivel=1,
    titulo="Seu Primeiro Print",
    descricao="Aprenda a exibir mensagens na tela usando print()",
    conteudo="""
    <h3>🎯 Objetivo</h3>
    <p>Aprender a usar a função <code>print()</code> para exibir mensagens.</p>
    
    <h3>📝 O que é print()?</h3>
    <p>A função <code>print()</code> exibe texto na tela. É uma das funções mais básicas do Python!</p>
    
    <h3>💡 Exemplo</h3>
    <pre>print("Olá, mundo!")</pre>
    
    <p>O texto entre aspas será mostrado na tela.</p>
    """,
    ordem=1,
    xp_total=30
)
db.add(lesson1)
db.commit()

exercises_l1 = [
    Exercise(
        lesson_id=lesson1.id,
        titulo="Print Simples",
        descricao='Use print() para exibir: Olá, mundo!',
        codigo_inicial="# Escreva seu código aqui\n",
        expected_output="Olá, mundo!",
        dica="Use print() com o texto entre aspas",
        xp_reward=10,
        ordem=1,
        difficulty="easy"
    ),
    Exercise(
        lesson_id=lesson1.id,
        titulo="Print com seu nome",
        descricao='Use print() para exibir: Meu nome é Python',
        codigo_inicial="# Escreva seu código aqui\n",
        expected_output="Meu nome é Python",
        dica="Lembre-se das aspas ao redor do texto",
        xp_reward=10,
        ordem=2,
        difficulty="easy"
    ),
    Exercise(
        lesson_id=lesson1.id,
        titulo="Múltiplos Prints",
        descricao='Use dois prints para exibir:\nPython\nProgramming',
        codigo_inicial="# Escreva seu código aqui\n",
        expected_output="Python\nProgramming",
        dica="Use print() duas vezes, uma em cada linha",
        xp_reward=10,
        ordem=3,
        difficulty="easy"
    ),
]

for ex in exercises_l1:
    db.add(ex)

# ==================== NÍVEL 1 - LIÇÃO 2 ====================

lesson2 = Lesson(
    nivel=1,
    titulo="Variáveis - Guardando Valores",
    descricao="Aprenda a criar variáveis e guardar informações",
    conteudo="""
    <h3>🎯 Objetivo</h3>
    <p>Aprender a criar variáveis para armazenar dados.</p>
    
    <h3>📝 O que são Variáveis?</h3>
    <p>Variáveis são como "caixas" que guardam valores. Você dá um nome e coloca algo dentro.</p>
    
    <h3>💡 Exemplo</h3>
    <pre>nome = "João"
idade = 25
print(nome)</pre>
    
    <p>A variável <code>nome</code> guarda "João" e <code>idade</code> guarda 25.</p>
    """,
    ordem=2,
    xp_total=40
)
db.add(lesson2)
db.commit()

exercises_l2 = [
    Exercise(
        lesson_id=lesson2.id,
        titulo="Criar uma variável",
        descricao='Crie uma variável chamada "mensagem" com o valor "Python é legal" e use print() para exibi-la.',
        codigo_inicial="# Crie a variável mensagem\n\n# Exiba com print()\n",
        expected_output="Python é legal",
        dica="Use: mensagem = ...",
        xp_reward=15,
        ordem=1,
        difficulty="easy"
    ),
    Exercise(
        lesson_id=lesson2.id,
        titulo="Variável com número",
        descricao='Crie uma variável "ano" com valor 2024 e exiba.',
        codigo_inicial="# Crie a variável ano\n\n# Exiba com print()\n",
        expected_output="2024",
        dica="Números não precisam de aspas",
        xp_reward=15,
        ordem=2,
        difficulty="easy"
    ),
]

for ex in exercises_l2:
    db.add(ex)

# ==================== NÍVEL 2 ====================

lesson3 = Lesson(
    nivel=2,
    titulo="Operações Matemáticas",
    descricao="Aprenda a fazer contas com Python",
    conteudo="""
    <h3>🎯 Objetivo</h3>
    <p>Usar Python como uma calculadora!</p>
    
    <h3>📝 Operadores</h3>
    <ul>
        <li><code>+</code> : soma</li>
        <li><code>-</code> : subtração</li>
        <li><code>*</code> : multiplicação</li>
        <li><code>/</code> : divisão</li>
    </ul>
    
    <h3>💡 Exemplo</h3>
    <pre>resultado = 10 + 5
print(resultado)  # Exibe: 15</pre>
    """,
    ordem=1,
    xp_total=50
)
db.add(lesson3)
db.commit()

exercises_l3 = [
    Exercise(
        lesson_id=lesson3.id,
        titulo="Soma simples",
        descricao='Calcule 5 + 3 e exiba o resultado.',
        codigo_inicial="# Calcule 5 + 3\n",
        expected_output="8",
        dica="Use print(5 + 3)",
        xp_reward=10,
        ordem=1,
        difficulty="easy"
    ),
    Exercise(
        lesson_id=lesson3.id,
        titulo="Multiplicação",
        descricao='Calcule 7 * 6 e exiba o resultado.',
        codigo_inicial="# Calcule 7 * 6\n",
        expected_output="42",
        dica="Use o operador *",
        xp_reward=10,
        ordem=2,
        difficulty="easy"
    ),
    Exercise(
        lesson_id=lesson3.id,
        titulo="Conta completa",
        descricao='Calcule (10 + 5) * 2 e exiba.',
        codigo_inicial="# Calcule (10 + 5) * 2\n",
        expected_output="30",
        dica="Use parênteses para prioridade",
        xp_reward=15,
        ordem=3,
        difficulty="medium"
    ),
]

for ex in exercises_l3:
    db.add(ex)

# ==================== NÍVEL 2 - LIÇÃO 2 ====================

lesson4 = Lesson(
    nivel=2,
    titulo="Trabalhando com Texto",
    descricao="Aprenda a manipular strings (textos)",
    conteudo="""
    <h3>🎯 Objetivo</h3>
    <p>Aprender a juntar e manipular textos.</p>
    
    <h3>📝 Concatenação</h3>
    <p>Você pode juntar textos usando o <code>+</code></p>
    
    <h3>💡 Exemplo</h3>
    <pre>nome = "Maria"
saudacao = "Olá, " + nome
print(saudacao)  # Olá, Maria</pre>
    """,
    ordem=2,
    xp_total=45
)
db.add(lesson4)
db.commit()

exercises_l4 = [
    Exercise(
        lesson_id=lesson4.id,
        titulo="Juntar textos",
        descricao='Crie uma variável com "Eu" e outra com "programo". Junte as duas com espaço e exiba "Eu programo".',
        codigo_inicial="# Crie as variáveis e junte\n",
        expected_output="Eu programo",
        dica="Use o + para juntar strings",
        xp_reward=15,
        ordem=1,
        difficulty="medium"
    ),
]

for ex in exercises_l4:
    db.add(ex)

db.commit()

print("✅ Banco populado com sucesso!")
print(f"   - {db.query(Lesson).count()} lições criadas")
print(f"   - {db.query(Exercise).count()} exercícios criados")

db.close()
