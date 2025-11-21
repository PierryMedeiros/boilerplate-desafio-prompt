# Desafio Final: Otimizador de Prompts com Testes Automatizados

🎯 **Objetivo**

Você atuará como um Prompt Engineer focado em qualidade. Sua missão é garantir que o prompt principal seja robusto, testável e altamente eficaz, utilizando testes automatizados para validar a estrutura e métricas de IA para validar o conteúdo.

Você deve:

- Analisar o prompt "ruim" que está no arquivo `prompts/bug_to_user_story_v1.yml`, e no arquivo `prompts/bug_to_user_story_v2.yml` desenvolver o prompt novo.
- Criar Testes Automatizados para validar a estrutura e as regras de negócio do seu prompt.
- Otimizar o Prompt novo aplicando técnicas avançadas (Few-shot, CoT, Role Playing) até passar nos testes.
- Publicar (Push) a versão otimizada no LangSmith.
- Atingir nota mínima de **0.9 (90%)** nas métricas de avaliação automática.

---

🖥️ **Exemplo de Fluxo no Terminal**

```bash
# 1. Publicar sua versão otimizada no Hub
python src/push_prompts.py

# 2. Avaliar a performance com métricas de IA
python src/evaluate.py

# 3. Rodar seus testes (inicialmente vão falhar ou passar dependendo do seu progresso)
pytest tests/test_prompts.py -v
```

```text
Executando avaliação dos prompts...
================================
Prompt: bug_to_user_story_v2
- Tone Score: 0.94
- Acceptance Criteria: 0.96
- Completeness: 0.93
================================
Status: APROVADO ✓ - Todas as métricas atingiram o mínimo de 0.9
```

---

🛠️ **Tecnologias & Ferramentas**

- **Linguagem:** Python 3.9+
- **Framework de Teste:** Pytest
- **Engenharia de Prompt:** LangChain & LangSmith Hub
- **Formato:** YAML (para estruturação dos prompts)

---

🔑 **Configuração de Acesso (Obrigatório)**

Para que os scripts funcionem, você precisará configurar as chaves de API no arquivo `.env`:

1.  **OpenAI (Recomendado)**
    - Crie uma API Key: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
    - Modelos usados: `gpt-4o-mini` (geração) e `gpt-4o` (avaliação)
    - Custo estimado: ~$1-3 USD

2.  **Gemini (Opção Gratuita)**
    - Crie uma API Key: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
    - Modelos usados: `gemini-1.5-flash`
    - Limite: 15 req/min (pode haver lentidão na avaliação em lote)

3.  **LangSmith (Plataforma de Prompts)**
    - Crie uma conta e uma API Key: [https://smith.langchain.com/](https://smith.langchain.com/)
    - Necessário para baixar o prompt base e subir sua versão final.

---

📝 **Passo a Passo do Desafio**

**1. Configuração e Pull (Infraestrutura Pronta)**

O repositório já contém os scripts necessários em `src/`. Sua primeira ação é trazer o problema para sua máquina.

**O que você deve fazer:**

- Fazer o fork e clone do repositório.
- Instalar dependências: `pip install -r requirements.txt`.
- Configurar o `.env` com suas chaves.
- Executar:
  ```bash
  python src/pull_prompts.py
  ```
  Isso irá baixar o conteúdo para `prompts/bug_to_user_story_v1.yml`.

**2. Implementação dos Testes (Sua tarefa de código)**

Antes de otimizar o prompt, você deve garantir que ele siga regras estritas. Você escreverá o código de teste que valida o seu prompt.

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

**3. Otimização do Prompt (Sua tarefa de Engenharia)**

Agora que os testes existem, você deve trabalhar na solução.

**O que você deve fazer:**

- Analise o prompt ruim em `prompts/bug_to_user_story_v1.yml`.
- Edite o arquivo `prompts/bug_to_user_story_v2.yml` criando sua versão otimizada.
- Aplique pelo menos **duas** das seguintes técnicas:
  - **Few-shot Learning:** Adicione exemplos reais de bugs -> user stories.
  - **Chain of Thought (CoT):** Instrua o modelo a pensar passo a passo antes de responder.
  - **Role Prompting:** Reforce a autoridade e o contexto da persona.
  - **Delimitadores:** Use marcações claras para separar instruções de dados.
- Preencha o campo `techniques_applied` no YAML com as técnicas que você usou.

*Dica: Use o arquivo `dataset.py` para ver exemplos de bugs que serão usados na avaliação.*

**4. Publicação e Avaliação (Infraestrutura Pronta)**

Com o prompt otimizado e passando nos testes unitários, é hora de ver como ele se sai contra métricas de IA.

**O que você deve fazer:**

- Subir sua versão para o Hub:
  ```bash
  python src/push_prompts.py
  ```
- Rodar a avaliação de qualidade:
  ```bash
  python src/evaluate.py
  ```

**Critério de Aprovação:** Você deve atingir uma nota média superior a **0.9** em todas as métricas:

- **Tone Score:** O tom é profissional?
- **Acceptance Criteria:** Gerou critérios de aceite válidos?
- **User Story Format:** Seguiu o padrão "Como um... Quero... Para..."?
- **Completeness:** Não perdeu nenhuma informação do bug original?

*Caso a nota seja baixa, volte ao Passo 3, ajuste o prompt, faça o push novamente e reavalie.*

---

📂 **Estrutura do Projeto**

```text
desafio-prompt-engineer/
├── prompts/
│   ├── bug_to_user_story_v1.yml  # (Gerado pelo pull) Prompt ruim original
│   └── bug_to_user_story_v2.yml  # <--- VOCÊ EDITA ESTE ARQUIVO (O Prompt)
│
├── src/                          # (CÓDIGO PRONTO - NÃO EDITAR)
│   ├── pull_prompts.py           # Script de download
│   ├── push_prompts.py           # Script de upload
│   ├── evaluate.py               # Script de avaliação
│   └── ...
│
├── tests/
│   └── test_prompts.py           # <--- VOCÊ EDITA ESTE ARQUIVO (Os Testes)
│
├── requirements.txt
└── README.md
```

---

📦 **Entregáveis**

- **Repositório GitHub** contendo:
  - Arquivo `tests/test_prompts.py` com os testes implementados.
  - Arquivo `prompts/bug_to_user_story_v2.yml` com o prompt otimizado.
  - `README.md` atualizado com a seção **"Técnicas Utilizadas"** explicando suas escolhas.

- **Link do LangSmith Hub:**
  - O script `push_prompts.py` vai gerar um link público do seu prompt. Inclua-o no `README.md`.

- **Evidência de Execução:**
  - Screenshot do terminal mostrando os testes passando (`pytest`).
  - Screenshot do terminal mostrando as notas da avaliação (`evaluate.py`) acima de 0.9.

Boa sorte! Transforme bugs caóticos em User Stories impecáveis! 🚀