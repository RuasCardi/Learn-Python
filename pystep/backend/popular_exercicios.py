# Script para popular o banco de dados com mais exercícios de Python
# Salve como popular_exercicios.py na pasta backend

from app.db.session import SessionLocal
from app.models.exercise import Exercise
from app.models.lesson import Lesson

# Exercícios exemplo
exercicios = [
    {
        "titulo": "Imprima Olá, Mundo!",
        "descricao": "Exiba a frase 'Olá, Mundo!' na tela.",
        "entrada_exemplo": "",
        "saida_esperada": "Olá, Mundo!",
        "dica": "Use a função print()."
    },
    {
        "titulo": "Soma de dois números",
        "descricao": "Leia dois números e exiba a soma.",
        "entrada_exemplo": "2 3",
        "saida_esperada": "5",
        "dica": "Use input() e print()."
    },
    {
        "titulo": "Concatene duas strings",
        "descricao": "Leia duas palavras e exiba-as juntas, separadas por espaço.",
        "entrada_exemplo": "casa azul",
        "saida_esperada": "casa azul",
        "dica": "Use + e ' ' para juntar."
    }
]

def popular_exercicios():
    db = SessionLocal()
    # Associa todos à primeira lição existente
    lesson = db.query(Lesson).first()
    for ex in exercicios:
        novo = Exercise(
            lesson_id=lesson.id if lesson else 1,
            titulo=ex["titulo"],
            descricao=ex["descricao"],
            entrada_exemplo=ex["entrada_exemplo"],
            saida_esperada=ex["saida_esperada"],
            dica=ex["dica"]
        )
        db.add(novo)
    db.commit()
    db.close()
    print("Exercícios adicionados!")

if __name__ == "__main__":
    popular_exercicios()
