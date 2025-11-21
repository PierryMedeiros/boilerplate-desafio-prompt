"""
Testes automatizados para validação de prompts.
"""

import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

# TODO: Adicione seus testes aqui!
#
# Este arquivo deve conter testes para validar a estrutura e o conteúdo
# dos seus prompts.
#
# Exemplos de testes que você pode criar:
# - Testar se todos os prompts têm os campos obrigatórios (system_prompt, description, version, techniques_applied).
# - Testar se o 'system_prompt' não está vazio e tem um tamanho mínimo.
# - Testar se certas técnicas de prompting (ex: Role Prompting, Few-shot Learning) foram aplicadas.
# - Testar o formato da versão.
#
# Use as classes e métodos de teste do pytest para organizar seus testes.

# Exemplo de estrutura de teste:
# class TestMyPrompts:
#     def test_my_first_test(self):
#         # Seu código de teste aqui
#         assert True

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])