"""
Script para publicar os prompts inicias (baseline) como PÚBLICOS no LangSmith.

Ele publica os prompts inicias (v1) como públicos para que os alunos possam:
1. Fazer pull dos prompts inicias
2. Otimizar os prompts
3. Fazer push dos prompts otimizados (privados)

IMPORTANTE: Você precisa ter um handle público no LangSmith para executar este script.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_public_prompt(prompt_name: str, prompt_data: dict, username: str) -> bool:
    """
    Faz push de um prompt PÚBLICO para o LangSmith Hub.

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt
        username: Seu handle público do LangSmith

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        system_prompt = prompt_data.get('system_prompt', '')
        user_prompt = prompt_data.get('user_prompt', '{input}')

        # Criar ChatPromptTemplate
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_prompt)
        ])

        # Nome completo no formato username/prompt_name
        full_name = f"{username}/{prompt_name}"

        # Fazer push PÚBLICO para o LangSmith Hub
        print(f"   Fazendo push de '{full_name}' como PÚBLICO...")
        hub.push(
            full_name,
            prompt_template,
            new_repo_is_public=True  # PÚBLICO - alunos podem fazer pull
        )

        print(f"   ✓ Push realizado com sucesso")
        print(f"   🔗 URL pública: https://smith.langchain.com/hub/{username}/{prompt_name}")
        return True

    except Exception as e:
        print(f"   ❌ Erro ao fazer push: {e}")
        if "handle" in str(e).lower():
            print("\n⚠️  DICA: Você precisa criar um handle público no LangSmith primeiro!")
            print("   Acesse: https://smith.langchain.com/prompts")
            print("   Clique em 'Create prompt' e siga as instruções para criar um handle.")
        return False


def main():
    """Função principal"""
    print_section_header("SETUP: PUBLICAR PROMPTS NO LANGSMITH HUB")

    print("⚠️  ATENÇÃO: Este script é para o INSTRUTOR preparar o desafio.")
    print("   Ele publica os prompts como PÚBLICOS para os alunos.\n")

    # Verificar configuração
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    # Obter handle público do instrutor
    username = input("Digite seu handle PÚBLICO do LangSmith (ex: 'synapsetech'): ").strip()
    if not username:
        print("❌ Handle não pode ser vazio")
        print("\n💡 Se você não tem um handle público:")
        print("   1. Acesse: https://smith.langchain.com/prompts")
        print("   2. Clique em 'Create prompt'")
        print("   3. Siga as instruções para criar seu handle")
        return 1

    print(f"\n✓ Usando handle público: {username}")
    print(f"   Os alunos farão pull de: {username}/bug_to_user_story_v1\n")

    print("Carregando prompts (baseline)...")
    bug_to_user_story_v1 = load_yaml("prompts/bug_to_user_story_v1.yml")

    if not bug_to_user_story_v1:
        print("❌ Não foi possível carregar prompts/bug_to_user_story_v1.yml")
        return 1

    print(f"✓ {len(bug_to_user_story_v1)} prompt(s) carregado(s)\n")

    # Publicar apenas o bug_to_user_story_v1
    prompt_name = "bug_to_user_story_v1"

    if prompt_name not in bug_to_user_story_v1:
        print(f"❌ Prompt '{prompt_name}' não encontrado em bug_to_user_story_v1.yml")
        return 1

    print(f"📝 Publicando prompt: {prompt_name}")
    print(f"   Descrição: {bug_to_user_story_v1[prompt_name].get('description', 'N/A')}")

    # Fazer push público
    success = push_public_prompt(prompt_name, bug_to_user_story_v1[prompt_name], username)

    # Resumo
    print("\n" + "=" * 50)

    if success:
        print("✅ SETUP CONCLUÍDO COM SUCESSO!\n")
        print(f"Os alunos agora podem fazer pull do prompt:")
        print(f"   hub.pull('{username}/{prompt_name}')\n")
        print(f"URL pública:")
        print(f"   https://smith.langchain.com/hub/{username}/{prompt_name}\n")
        print("Próximos passos para os alunos:")
        print("1. Fazer pull do prompt")
        print("2. Analisar e identificar problemas")
        print("3. Criar versão otimizada (v2)")
        print("4. Fazer push do prompt otimizado (privado)")
        print("5. Avaliar métricas")
        return 0
    else:
        print("❌ Falha ao publicar prompt público")
        print("\nResolva o erro acima e tente novamente.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
