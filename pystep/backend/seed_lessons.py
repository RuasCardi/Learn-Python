"""
Script para popular o banco de dados com lições e exercícios organizados
Níveis 1, 2 e 3 com 5 exercícios cada
"""

from app.core.database import SessionLocal, engine
from app.models import Base, Lesson, Exercise

# Criar tabelas
Base.metadata.create_all(bind=engine)

def clear_database():
    """Limpa o banco de dados"""
    db = SessionLocal()
    try:
        db.query(Exercise).delete()
        db.query(Lesson).delete()
        db.commit()
        print("✅ Banco de dados limpo!")
    finally:
        db.close()

def create_lessons_and_exercises():
    """Cria lições e exercícios organizados"""
    db = SessionLocal()
    
    try:
        # NÍVEL 1: Primeiros Passos com Python
        lesson1 = Lesson(
            nivel=1,
            titulo="Primeiros Passos com Python",
            descricao="Aprenda os conceitos básicos: print, variáveis e tipos de dados",
            conteudo="""
            <h3>Bem-vindo ao Python!</h3>
            <p>Python é uma linguagem de programação simples e poderosa.</p>
            <h4>Função print()</h4>
            <p>Use <code>print()</code> para exibir mensagens na tela:</p>
            <pre>print("Olá, Mundo!")</pre>
            <h4>Variáveis</h4>
            <p>Variáveis armazenam valores:</p>
            <pre>nome = "Python"
idade = 30</pre>
            """,
            ordem=1,
            xp_total=50,
            is_active=True
        )
        db.add(lesson1)
        db.commit()
        
        exercises_nivel1 = [
            {
                "titulo": "Olá, Mundo!",
                "descricao": "Exiba a mensagem 'Olá, Mundo!' na tela usando a função print().",
                "codigo_inicial": "# Escreva seu código aqui\n",
                "expected_output": "Olá, Mundo!",
                "input_data": "",
                "dica": "Use print('Olá, Mundo!')",
                "ordem": 1
            },
            {
                "titulo": "Seu Nome",
                "descricao": "Crie uma variável chamada 'nome' com seu nome e exiba-a com print().",
                "codigo_inicial": "# Crie uma variável 'nome'\n# Exiba ela com print()\n",
                "expected_output": "Python",
                "input_data": "",
                "dica": "nome = 'Python'\nprint(nome)",
                "ordem": 2
            },
            {
                "titulo": "Soma Simples",
                "descricao": "Calcule e exiba a soma de 5 + 3.",
                "codigo_inicial": "# Calcule 5 + 3 e exiba o resultado\n",
                "expected_output": "8",
                "input_data": "",
                "dica": "Use print(5 + 3)",
                "ordem": 3
            },
            {
                "titulo": "Duas Variáveis",
                "descricao": "Crie duas variáveis 'a = 10' e 'b = 20' e exiba a soma delas.",
                "codigo_inicial": "# Crie as variáveis a e b\n# Exiba a soma\n",
                "expected_output": "30",
                "input_data": "",
                "dica": "a = 10\nb = 20\nprint(a + b)",
                "ordem": 4
            },
            {
                "titulo": "Concatenação",
                "descricao": "Una as palavras 'Python' e 'Rocks' com um espaço entre elas e exiba o resultado.",
                "codigo_inicial": "# Una as palavras\n",
                "expected_output": "Python Rocks",
                "input_data": "",
                "dica": "print('Python' + ' ' + 'Rocks')",
                "ordem": 5
            }
        ]
        
        for ex in exercises_nivel1:
            exercise = Exercise(
                lesson_id=lesson1.id,
                titulo=ex["titulo"],
                descricao=ex["descricao"],
                codigo_inicial=ex["codigo_inicial"],
                expected_output=ex["expected_output"],
                input_data=ex["input_data"],
                dica=ex["dica"],
                ordem=ex["ordem"],
                xp_reward=10,
                difficulty="easy"
            )
            db.add(exercise)
        
        db.commit()
        print("✅ Nível 1 criado com sucesso!")
        
        # NÍVEL 2: Operações e Tipos de Dados
        lesson2 = Lesson(
            nivel=2,
            titulo="Operações e Tipos de Dados",
            descricao="Aprenda sobre operações matemáticas e diferentes tipos de dados",
            conteudo="""
            <h3>Operações em Python</h3>
            <h4>Operadores Matemáticos</h4>
            <ul>
                <li><code>+</code> soma</li>
                <li><code>-</code> subtração</li>
                <li><code>*</code> multiplicação</li>
                <li><code>/</code> divisão</li>
                <li><code>**</code> potência</li>
            </ul>
            <h4>Tipos de Dados</h4>
            <ul>
                <li><strong>int</strong>: números inteiros (5, 10, -3)</li>
                <li><strong>float</strong>: números decimais (3.14, 2.5)</li>
                <li><strong>str</strong>: texto ("Python", 'Olá')</li>
            </ul>
            """,
            ordem=2,
            xp_total=50,
            is_active=True
        )
        db.add(lesson2)
        db.commit()
        
        exercises_nivel2 = [
            {
                "titulo": "Multiplicação",
                "descricao": "Calcule e exiba o resultado de 7 * 6.",
                "codigo_inicial": "# Calcule 7 * 6\n",
                "expected_output": "42",
                "input_data": "",
                "dica": "print(7 * 6)",
                "ordem": 1
            },
            {
                "titulo": "Divisão",
                "descricao": "Calcule e exiba o resultado de 100 / 4.",
                "codigo_inicial": "# Calcule 100 / 4\n",
                "expected_output": "25.0",
                "input_data": "",
                "dica": "print(100 / 4)",
                "ordem": 2
            },
            {
                "titulo": "Potência",
                "descricao": "Calcule e exiba 2 elevado à 3 (2³).",
                "codigo_inicial": "# Calcule 2³\n",
                "expected_output": "8",
                "input_data": "",
                "dica": "Use o operador ** para potência: print(2 ** 3)",
                "ordem": 3
            },
            {
                "titulo": "Operações Combinadas",
                "descricao": "Calcule e exiba: (10 + 5) * 2.",
                "codigo_inicial": "# Calcule a expressão\n",
                "expected_output": "30",
                "input_data": "",
                "dica": "Use parênteses: print((10 + 5) * 2)",
                "ordem": 4
            },
            {
                "titulo": "Média de Três Números",
                "descricao": "Calcule a média de 8, 9 e 10. Exiba o resultado.",
                "codigo_inicial": "# Calcule a média\n",
                "expected_output": "9.0",
                "input_data": "",
                "dica": "Soma dividida por 3: print((8 + 9 + 10) / 3)",
                "ordem": 5
            }
        ]
        
        for ex in exercises_nivel2:
            exercise = Exercise(
                lesson_id=lesson2.id,
                titulo=ex["titulo"],
                descricao=ex["descricao"],
                codigo_inicial=ex["codigo_inicial"],
                expected_output=ex["expected_output"],
                input_data=ex["input_data"],
                dica=ex["dica"],
                ordem=ex["ordem"],
                xp_reward=10,
                difficulty="easy"
            )
            db.add(exercise)
        
        db.commit()
        print("✅ Nível 2 criado com sucesso!")
        
        # NÍVEL 3: Trabalhando com Strings
        lesson3 = Lesson(
            nivel=3,
            titulo="Trabalhando com Strings",
            descricao="Aprenda a manipular textos em Python",
            conteudo="""
            <h3>Strings em Python</h3>
            <p>Strings são sequências de caracteres (texto).</p>
            <h4>Criando Strings</h4>
            <pre>texto = "Python"
frase = 'Olá, Mundo!'</pre>
            <h4>Operações com Strings</h4>
            <ul>
                <li><code>+</code> concatenação (unir textos)</li>
                <li><code>*</code> repetição</li>
                <li><code>.upper()</code> deixa tudo MAIÚSCULO</li>
                <li><code>.lower()</code> deixa tudo minúsculo</li>
                <li><code>len()</code> retorna o tamanho</li>
            </ul>
            <h4>Exemplo</h4>
            <pre>nome = "python"
print(nome.upper())  # PYTHON
print(len(nome))     # 6</pre>
            """,
            ordem=3,
            xp_total=50,
            is_active=True
        )
        db.add(lesson3)
        db.commit()
        
        exercises_nivel3 = [
            {
                "titulo": "Maiúsculas",
                "descricao": "Crie uma variável com 'python' e exiba em maiúsculas.",
                "codigo_inicial": "# Transforme 'python' em maiúsculas\n",
                "expected_output": "PYTHON",
                "input_data": "",
                "dica": "Use .upper(): print('python'.upper())",
                "ordem": 1
            },
            {
                "titulo": "Tamanho do Texto",
                "descricao": "Exiba o tamanho (número de caracteres) da palavra 'programação'.",
                "codigo_inicial": "# Use len() para contar caracteres\n",
                "expected_output": "11",
                "input_data": "",
                "dica": "print(len('programação'))",
                "ordem": 2
            },
            {
                "titulo": "Repetição",
                "descricao": "Exiba a palavra 'Ha' repetida 3 vezes (HaHaHa).",
                "codigo_inicial": "# Repita 'Ha' 3 vezes\n",
                "expected_output": "HaHaHa",
                "input_data": "",
                "dica": "Use *: print('Ha' * 3)",
                "ordem": 3
            },
            {
                "titulo": "Nome Completo",
                "descricao": "Una 'João' e 'Silva' com um espaço entre eles.",
                "codigo_inicial": "# Una os nomes\n",
                "expected_output": "João Silva",
                "input_data": "",
                "dica": "print('João' + ' ' + 'Silva')",
                "ordem": 4
            },
            {
                "titulo": "Minúsculas",
                "descricao": "Transforme 'PYTHON' em minúsculas e exiba.",
                "codigo_inicial": "# Transforme em minúsculas\n",
                "expected_output": "python",
                "input_data": "",
                "dica": "Use .lower(): print('PYTHON'.lower())",
                "ordem": 5
            }
        ]
        
        for ex in exercises_nivel3:
            exercise = Exercise(
                lesson_id=lesson3.id,
                titulo=ex["titulo"],
                descricao=ex["descricao"],
                codigo_inicial=ex["codigo_inicial"],
                expected_output=ex["expected_output"],
                input_data=ex["input_data"],
                dica=ex["dica"],
                ordem=ex["ordem"],
                xp_reward=10,
                difficulty="easy"
            )
            db.add(exercise)
        
        db.commit()
        print("✅ Nível 3 criado com sucesso!")
        print("\n🎉 Todas as lições e exercícios foram criados!")
        print(f"📚 Total: 3 lições com 15 exercícios")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔄 Limpando banco de dados...")
    clear_database()
    print("\n📝 Criando lições e exercícios...")
    create_lessons_and_exercises()
