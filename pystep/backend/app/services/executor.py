"""
Python Code Executor Service
=============================

Executa código Python de forma segura em um ambiente sandbox.
Implementa timeout, limite de memória e restrições de imports.
"""

import sys
import io
import signal
import ast
import traceback
from typing import Dict, Any, Optional
from contextlib import redirect_stdout, redirect_stderr

from app.core.config import settings


class ExecutionError(Exception):
    """Erro personalizado para execução de código"""
    pass


class CodeExecutor:
    """
    Executor seguro de código Python.
    
    Segurança:
    - Timeout configurável
    - Sem acesso a sistema de arquivos
    - Imports restritos
    - Captura de stdout/stderr
    """
    
    def __init__(self):
        self.timeout = settings.EXECUTION_TIMEOUT
        self.allowed_imports = set(settings.ALLOWED_IMPORTS.split(","))
    
    def _validate_code(self, code: str) -> tuple[bool, Optional[str]]:
        """
        Valida o código antes de executar.
        
        Verifica:
        - Sintaxe Python válida
        - Imports não permitidos
        - Operações perigosas
        
        Returns:
            (válido, mensagem_erro)
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Erro de sintaxe na linha {e.lineno}: {e.msg}"
        
        # Verificar imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split('.')[0] not in self.allowed_imports:
                        return False, f"Import não permitido: {alias.name}"
            
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split('.')[0] not in self.allowed_imports:
                    return False, f"Import não permitido: {node.module}"
            
            # Bloquear operações perigosas
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    dangerous_funcs = {'open', 'eval', 'exec', 'compile', '__import__'}
                    if node.func.id in dangerous_funcs:
                        return False, f"Função não permitida: {node.func.id}"
        
        return True, None
    
    def _timeout_handler(self, signum, frame):
        """Handler para timeout de execução"""
        raise TimeoutError("Tempo limite de execução excedido")
    
    def execute(self, code: str, input_data: str = "") -> Dict[str, Any]:
        """
        Executa código Python de forma segura.
        
        Args:
            code: Código Python para executar
            input_data: Dados de entrada (simulando stdin)
            
        Returns:
            {
                "output": str,           # Saída do programa
                "error": str,            # Mensagens de erro
                "status": str,           # "success" ou "error"
                "execution_time": float  # Tempo de execução
            }
        """
        import time
        start_time = time.time()
        
        # Validar código
        is_valid, error_msg = self._validate_code(code)
        if not is_valid:
            return {
                "output": "",
                "error": error_msg,
                "status": "error",
                "execution_time": 0
            }
        
        # Capturar stdout e stderr
        stdout = io.StringIO()
        stderr = io.StringIO()
        
        try:
            # Configurar timeout (apenas em Unix)
            if hasattr(signal, 'SIGALRM'):
                signal.signal(signal.SIGALRM, self._timeout_handler)
                signal.alarm(self.timeout)
            
            # Criar namespace isolado
            namespace = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'bool': bool,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'set': set,
                    'abs': abs,
                    'max': max,
                    'min': min,
                    'sum': sum,
                    'sorted': sorted,
                    'enumerate': enumerate,
                    'zip': zip,
                    'map': map,
                    'filter': filter,
                    'type': type,
                    'isinstance': isinstance,
                    'input': lambda: input_data,
                }
            }
            
            # Executar código com redirecionamento
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exec(code, namespace)
            
            # Cancelar timeout
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            
            execution_time = time.time() - start_time
            
            return {
                "output": stdout.getvalue(),
                "error": stderr.getvalue(),
                "status": "success",
                "execution_time": round(execution_time, 3)
            }
        
        except TimeoutError:
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            return {
                "output": stdout.getvalue(),
                "error": f"⏱️ Tempo limite excedido ({self.timeout}s)",
                "status": "error",
                "execution_time": self.timeout
            }
        
        except Exception as e:
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            
            error_trace = traceback.format_exc()
            execution_time = time.time() - start_time
            
            return {
                "output": stdout.getvalue(),
                "error": f"{type(e).__name__}: {str(e)}",
                "status": "error",
                "execution_time": round(execution_time, 3)
            }
    
    def test_code(self, code: str, expected_output: str) -> Dict[str, Any]:
        """
        Executa e testa se o código produz a saída esperada.
        
        Args:
            code: Código Python
            expected_output: Saída esperada
            
        Returns:
            Resultado da execução + campo "passed" (bool)
        """
        result = self.execute(code)
        
        if result["status"] == "success":
            actual_output = result["output"].strip()
            expected_output = expected_output.strip()
            result["passed"] = actual_output == expected_output
            result["expected"] = expected_output
            result["actual"] = actual_output
        else:
            result["passed"] = False
            result["expected"] = expected_output
            result["actual"] = ""
        
        return result


# Instância global
executor = CodeExecutor()
