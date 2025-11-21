"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Faz pull dos prompts do LangSmith Prompt Hub.

    Returns:
        Dict com os prompts ou None se erro
    """
    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return None

    print("Fazendo pull dos prompts do LangSmith...")
    print("=" * 50)

    prompts = {}

    # Configurar username (pode ser workspace ou usuário público)
    username_langsmith = os.getenv("USERNAME_LANGSMITH_HUB", "fullcycle")

    # Lista de prompts para baixar
    prompt_names = [
        (f"{username_langsmith}/bug_to_user_story_v1", "bug_to_user_story_v1"),
        # (f"{username_langsmith}/outro_prompt", "outro_prompt_local"),
    ]

    for hub_name, local_name in prompt_names:
        try:
            print(f"📥 Baixando: {hub_name}...")
            prompt = hub.pull(hub_name)

            prompt_dict = {
                "description": f"Prompt baixado de {hub_name}",
                "version": "v1",
                "tags": ["downloaded", "baseline"]
            }

            # Extrair system_prompt e user_prompt
            if hasattr(prompt, 'messages') and prompt.messages:
                for i, msg in enumerate(prompt.messages):
                    if i == 0:  # Primeira mensagem é system
                        prompt_dict["system_prompt"] = msg.prompt.template if hasattr(msg.prompt, 'template') else str(msg)
                    elif i == 1:  # Segunda mensagem é user
                        prompt_dict["user_prompt"] = msg.prompt.template if hasattr(msg.prompt, 'template') else str(msg)
            elif hasattr(prompt, 'template'):
                prompt_dict["system_prompt"] = ""
                prompt_dict["user_prompt"] = prompt.template
            else:
                prompt_dict["system_prompt"] = str(prompt)
                prompt_dict["user_prompt"] = "{input}"

            if "user_prompt" not in prompt_dict:
                prompt_dict["user_prompt"] = "{input}"

            prompts[local_name] = prompt_dict
            print(f"   ✓ {hub_name} baixado com sucesso")

        except Exception as e:
            error_msg = str(e).lower()
            print(f"   ⚠️  Erro ao baixar {hub_name}")

            if "not found" in error_msg or "404" in error_msg:
                print(f"   → Prompt não encontrado no LangSmith Hub")
                print(f"   → Verifique se o nome está correto: {hub_name}")
                print(f"   → Ou se USERNAME_LANGSMITH_HUB está correto no .env: {username_langsmith}")
            else:
                print(f"   → Erro: {e}")

    return prompts if prompts else None


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH")

    prompts = pull_prompts_from_langsmith()

    if prompts:
        output_path = "prompts/bug_to_user_story_v1.yml"
        if save_yaml(prompts, output_path):
            print(f"\n✅ Prompts baixados salvos em {output_path}")
            print(f"   Total: {len(prompts)} prompt(s)")

            print("\n📋 Preview:")
            for name in prompts.keys():
                print(f"   - {name}")
        else:
            print(f"\n❌ Falha ao salvar prompts")
            return 1
    else:
        print("\n⚠️  NOTA: Não foi possível baixar prompts do LangSmith.")
        print("\nPossíveis causas:")
        print("  1. Prompts não existem no Hub com os nomes especificados")
        print("  2. USERNAME_LANGSMITH_HUB incorreto no .env")
        print("  3. LANGSMITH_API_KEY sem permissão de acesso")
        print("\nSolução:")
        print("  - Verifique as variáveis no .env")
        print("  - Confirme que os prompts existem em: https://smith.langchain.com/prompts")
        print("  - Use os prompts de exemplo fornecidos localmente")

    print("\n" + "=" * 50)
    print("Próximos passos:")
    print("1. Analise os prompts em prompts/bug_to_user_story_v1.yml")
    print("2. Refatore-os em prompts/bug_to_user_story_v2.yml")
    print("3. Execute: python src/push_prompts.py")
    print("4. Execute: python src/evaluate.py")

    return 0


if __name__ == "__main__":
    sys.exit(main())
