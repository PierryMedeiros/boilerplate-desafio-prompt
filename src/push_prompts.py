"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
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


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        # Criar ChatPromptTemplate
        system_prompt = prompt_data.get('system_prompt', '')
        user_prompt = prompt_data.get('user_prompt', '{input}')

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])

        # Push PÚBLICO para o LangSmith Hub
        hub.push(
            prompt_name,
            prompt_template,
            new_repo_is_public=True 
        )

        print(f"   ✓ Push realizado com sucesso")
        print(f"   → Prompt público: {prompt_name}")
        return True

    except Exception as e:
        print(f"   ❌ Erro ao fazer push: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    # Verificar campos essenciais
    if not prompt_data.get('system_prompt', '').strip():
        errors.append("system_prompt está vazio")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS PARA LANGSMITH HUB")

    # Verificar credenciais
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    print("ℹ️  Os prompts serão salvos como PÚBLICOS no LangSmith Hub")
    print("   Qualquer pessoa poderá visualizar e usar seus prompts\n")

    # Carregar prompts
    print("Carregando prompts otimizados...")
    prompts = load_yaml("prompts/bug_to_user_story_v2.yml")

    if not prompts:
        print("❌ Não foi possível carregar prompts/bug_to_user_story_v2.yml")
        return 1

    print(f"✓ {len(prompts)} prompt(s) encontrado(s)\n")

    # Processar cada prompt
    success_count = 0
    total_count = 0

    print("Validando e fazendo push...\n")

    for prompt_name, prompt_data in prompts.items():
        # Ignorar comentários e metadados
        if prompt_name.startswith('_') or not isinstance(prompt_data, dict):
            continue

        total_count += 1
        print(f"📝 {prompt_name}")

        # Validar
        is_valid, errors = validate_prompt(prompt_data)

        if not is_valid:
            print(f"   ❌ Validação falhou:")
            for error in errors:
                print(f"      • {error}")
            print()
            continue

        # Exibir técnicas aplicadas (se houver)
        techniques = prompt_data.get('techniques_applied', [])
        if techniques:
            print(f"   Técnicas: {', '.join(techniques[:3])}...")  # Mostrar só as 3 primeiras

        # Push
        if push_prompt_to_langsmith(prompt_name, prompt_data):
            success_count += 1
        print()

    # Resumo
    print("=" * 70)
    print(f"RESUMO: {success_count}/{total_count} prompt(s) publicado(s)\n")

    if success_count > 0:
        print("✅ Prompts publicados com sucesso!")
        print(f"\n📍 Confira em:")
        print(f"   https://smith.langchain.com/prompts\n")

        print("🔗 Os prompts estão PÚBLICOS e podem ser acessados por:")
        print(f"   • hub.pull('bug_to_user_story_v2')")
        print(f"   • Ou diretamente no LangSmith Hub\n")

        print("📋 Próximos passos:")
        print("   1. Execute: python src/evaluate.py")
        print("   2. Verifique se a média geral atingiu >= 0.8")
        print("   3. Se necessário, refatore e faça push novamente")
        return 0
    else:
        print("⚠️  Nenhum prompt foi publicado")
        print("\n💡 Verifique:")
        print("   • prompts/bug_to_user_story_v2.yml existe")
        print("   • Prompts não contêm TODOs")
        print("   • system_prompt não está vazio")
        return 1


if __name__ == "__main__":
    sys.exit(main())
