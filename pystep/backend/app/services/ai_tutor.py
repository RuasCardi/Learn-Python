"""
AI Tutor Service
=================

Sistema de feedback inteligente usando OpenAI.
Analisa código do aluno e fornece feedback personalizado.
"""

import json
from typing import Dict, Any, Optional
from openai import OpenAI

from app.core.config import settings


class AITutor:
    """
    IA Tutora que analisa código e fornece feedback pedagógico.
    
    Características:
    - Analisa lógica, não apenas sintaxe
    - Feedback progressivo (dicas ao invés de respostas)
    - Tom encorajador e didático
    - Detecta erros comuns de iniciantes
    """
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.model = settings.OPENAI_MODEL
    
    def analyze_code(
        self,
        code: str,
        execution_result: Dict[str, Any],
        exercise_description: str,
        expected_output: str,
        attempt_number: int = 1
    ) -> Dict[str, Any]:
        """
        Analisa o código do aluno e gera feedback inteligente.
        
        Args:
            code: Código escrito pelo aluno
            execution_result: Resultado da execução
            exercise_description: Descrição do exercício
            expected_output: Saída esperada
            attempt_number: Número da tentativa (para dicas progressivas)
            
        Returns:
            {
                "feedback": str,        # Feedback para o aluno
                "hint": str,           # Dica específica
                "encouragement": str,  # Mensagem encorajadora
                "severity": str,       # "success", "info", "warning", "error"
                "suggestions": list    # Sugestões de melhorias
            }
        """
        
        # Se não tiver API key, usar feedback básico
        if not self.client:
            return self._basic_feedback(execution_result, expected_output)
        
        # Se passou no teste, feedback positivo
        if execution_result.get("passed"):
            return self._success_feedback(code, execution_result)
        
        # Análise com IA
        return self._ai_analysis(
            code,
            execution_result,
            exercise_description,
            expected_output,
            attempt_number
        )
    
    def _basic_feedback(
        self,
        execution_result: Dict[str, Any],
        expected_output: str
    ) -> Dict[str, Any]:
        """Feedback básico sem IA (fallback)"""
        
        if execution_result["status"] == "error":
            return {
                "feedback": "❌ Seu código tem um erro. Leia a mensagem de erro com atenção.",
                "hint": "Verifique a sintaxe e tente novamente.",
                "encouragement": "Não desanime! Erros fazem parte do aprendizado.",
                "severity": "error",
                "suggestions": ["Revise a sintaxe do Python", "Leia a mensagem de erro"]
            }
        
        actual = execution_result.get("output", "").strip()
        expected = expected_output.strip()
        
        if actual != expected:
            return {
                "feedback": "⚠️ Seu código executa, mas a saída não está correta.",
                "hint": f"Esperado: '{expected}'\nObtido: '{actual}'",
                "encouragement": "Você está no caminho certo! Ajuste a lógica.",
                "severity": "warning",
                "suggestions": ["Compare sua saída com o esperado", "Revise a lógica"]
            }
        
        return {
            "feedback": "✅ Perfeito! Seu código está correto.",
            "hint": "",
            "encouragement": "Parabéns! Continue assim! 🎉",
            "severity": "success",
            "suggestions": []
        }
    
    def _success_feedback(
        self,
        code: str,
        execution_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Feedback para código que passou no teste"""
        
        # Analisar qualidade do código (opcional)
        suggestions = []
        
        if len(code.strip().split('\n')) > 10:
            suggestions.append("💡 Dica: Código mais conciso pode ser melhor")
        
        encouragements = [
            "🎉 Excelente trabalho!",
            "⭐ Muito bem! Você dominou este exercício!",
            "🚀 Perfeito! Continue assim!",
            "💪 Mandou bem! Próximo desafio!",
            "✨ Código aprovado! Você está evoluindo!"
        ]
        
        import random
        
        return {
            "feedback": "✅ Seu código está correto e funciona perfeitamente!",
            "hint": "",
            "encouragement": random.choice(encouragements),
            "severity": "success",
            "suggestions": suggestions,
            "xp_gained": 10 + (5 if not suggestions else 0)  # XP bônus para código limpo
        }
    
    def _ai_analysis(
        self,
        code: str,
        execution_result: Dict[str, Any],
        exercise_description: str,
        expected_output: str,
        attempt_number: int
    ) -> Dict[str, Any]:
        """Análise usando IA (OpenAI)"""
        
        # Construir prompt para a IA
        prompt = f"""Você é um professor de Python paciente e encorajador. Analise o código do aluno e forneça feedback construtivo.

**Exercício:**
{exercise_description}

**Saída Esperada:**
{expected_output}

**Código do Aluno:**
```python
{code}
```

**Resultado da Execução:**
Status: {execution_result['status']}
Saída: {execution_result.get('output', 'N/A')}
Erro: {execution_result.get('error', 'N/A')}

**Número da Tentativa:** {attempt_number}

**Instruções:**
1. Se for a primeira tentativa, dê uma dica GENÉRICA
2. Se for tentativa 2+, seja mais específico
3. NUNCA entregue a resposta completa
4. Use linguagem simples e encorajadora
5. Foque no PRÓXIMO PASSO que o aluno deve dar

Responda em JSON:
{{
  "feedback": "análise principal",
  "hint": "dica específica",
  "encouragement": "mensagem motivadora",
  "severity": "error|warning|info",
  "suggestions": ["sugestão 1", "sugestão 2"]
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um professor de Python especializado em ensino progressivo para iniciantes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            
            # Extrair JSON da resposta
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            result = json.loads(content.strip())
            return result
        
        except Exception as e:
            print(f"Erro na análise da IA: {e}")
            # Fallback para feedback básico
            return self._basic_feedback(execution_result, expected_output)
    
    def generate_hint(self, exercise_description: str, current_code: str) -> str:
        """
        Gera uma dica para o aluno sem entregar a resposta.
        
        Args:
            exercise_description: Descrição do exercício
            current_code: Código atual do aluno
            
        Returns:
            Dica textual
        """
        if not self.client:
            return "💡 Releia o enunciado com atenção e pense na lógica passo a passo."
        
        prompt = f"""Dê UMA dica sutil (não a resposta!) para este exercício de Python:

**Exercício:**
{exercise_description}

**Código Atual:**
```python
{current_code}
```

Responda com uma única frase que ajude sem entregar a solução."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Você é um professor que dá dicas sutis, nunca respostas diretas."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
        
        except:
            return "💡 Pense sobre a lógica: o que você precisa fazer primeiro?"


# Instância global
ai_tutor = AITutor()
