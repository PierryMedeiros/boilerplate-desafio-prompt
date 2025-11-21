"""
Crie aqui o script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script deve:
1. Ler os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Validar os prompts
3. Fazer push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()