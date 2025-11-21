"""
Crie aqui o script para fazer pull de prompts do LangSmith Prompt Hub.

Este script deve:
1. Conecta ao LangSmith usando credenciais do .env
2. Fazer o pull do prompt ruim do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.

Abaixo estão importações úteis que você pode usar.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()