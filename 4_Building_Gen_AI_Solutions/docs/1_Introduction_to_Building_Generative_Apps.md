# 🏗️ Introdução ao Desenvolvimento de Aplicações Generativas

## 🌐 O Cenário Evolutivo da IA Generativa

Bem-vindo à introdução ao desenvolvimento de aplicações e soluções de IA generativa. O foco principal é no design e desenvolvimento de recursos e aplicações que integram modelos de IA generativa. A IA generativa está se tornando uma parte essencial do desenvolvimento de software, impulsionando aplicações desde mecanismos de busca até o conteúdo de mídia que consumimos diariamente. Estes modelos aprimoram diversas funcionalidades de produtos de software, incluindo funções de busca, criação de conteúdo, chatbots, assistência interativa e recursos de personalização.

### IA Tradicional vs. IA Generativa

| Dimensão | IA Tradicional | IA Generativa |
|---|---|---|
| **Saída** | Classificação / previsão determinística | Conteúdo novo e coerente |
| **Treinamento** | Dataset específico por tarefa | Dataset massivo e generalista |
| **Flexibilidade** | Uma tarefa, um modelo | Multitarefa via linguagem natural |
| **Integração** | APIs e SDKs especializados | API REST simples via prompt |
| **Exemplo** | Detector de anomalias em radiografia | GPT gera laudos em linguagem natural |

Em 2017, o Google Brain introduziu a **arquitetura Transformer**, causando uma mudança de paradigma: ao contrário dos modelos tradicionais, os **modelos de fundação** são treinados em vastos conjuntos de dados e podem gerar dados coerentes e contextualmente relevantes.

---

## 🏛️ A Pilha Técnica da IA Generativa

A base técnica que habilita a IA generativa é uma **pilha em camadas** com três níveis:

```
┌─────────────────────────────────────────────────────┐
│          🖥️ CAMADA DE APLICAÇÃO (B2B / B2C)          │
│   Chatbots · Geração de conteúdo · Assistentes       │
├─────────────────────────────────────────────────────┤
│          🧠 CAMADA DE MODELO E PLATAFORMA            │
│   GPT · Gemini · Claude · Hugging Face · Fine-tuning │
├─────────────────────────────────────────────────────┤
│          ⚙️ CAMADA DE INFRAESTRUTURA E HARDWARE      │
│   GPUs / TPUs · Cloud (AWS, Azure, GCP) · Armazen.   │
└─────────────────────────────────────────────────────┘
```

| Camada | O que faz | Exemplos |
|---|---|---|
| **Infraestrutura** | Computa o treinamento e a inferência | GPUs, TPUs, cloud providers |
| **Modelo e Plataforma** | Algoritmos, redes neurais, APIs de IA | OpenAI API, Hugging Face, PyTorch |
| **Aplicação** | Interfaces para o usuário final | Chatbots, geradores de conteúdo, RAG |

> ⚠️ **A camada de aplicação é responsável por formatar entradas, detectar e mitigar saídas prejudiciais, tendenciosas ou enganosas** — o uso ético começa aqui.

---

## ⚠️ Os Desafios dos Modelos Generativos

A interação com LLMs ocorre exclusivamente através da **linguagem natural**. Ao contrário de funções de programação que retornam resultados reproduzíveis, os modelos generativos são **imprevisíveis** — o mesmo prompt pode gerar respostas diferentes a cada chamada.

Outro problema crítico é a **natureza sem estado** dos LLMs. Para criar um chatbot conversacional, é necessário enviar todas as mensagens anteriores na chamada de API — isso compõe a **janela de contexto**, que tem tamanho limitado em **tokens**. Ao atingir o limite, as mensagens mais antigas são descartadas, causando perda de contexto.

> 💡 **Insight:** Frameworks como LangChain fornecem componentes de **memória** para gerenciar a janela de contexto e simular estado em conversas longas.

---

## ✍️ Prompts e Engenharia de Prompt

A **criação de prompts** é um aspecto crucial na interação com LLMs. **Prompts** são declarações ou perguntas fornecidas ao modelo para gerar uma saída desejada.

**Exemplo prático — Diagnóstico de sintomas:**

```python
# Entrada bruta do usuário (checkboxes)
sintomas = ["febre", "tosse", "cansaço"]

# Engenharia de prompt na camada de aplicação
prompt = f"Quais são as potenciais doenças associadas a sintomas como {', '.join(sintomas)}?"

# O modelo responde; a aplicação pós-processa e exibe com aviso médico
```

A lógica da aplicação pré-processa a entrada bruta, engendra o prompt ideal e pós-processa a resposta do modelo antes de exibi-la ao usuário.

---

## 🚀 Recursos e Soluções de IA Generativa

Modelos generativos se destacam em **compreender contexto, filtrar informações relevantes e sintetizar dados** em narrativas coerentes.

### Novas Categorias de Aplicações

| Categoria | Descrição | Exemplos de Uso |
|---|---|---|
| **Geração de conteúdo** | Redigir artigos, marketing, análises | Canva, Writer.com |
| **Conversação natural** | Chatbots que lidam com consultas complexas | Atendimento ao cliente |
| **RAG** | Combina LLM + busca em documentos | Q&A sobre documentos internos |
| **Fine-tuning** | Especializa o modelo em dados de nicho | Modelos de código aberto customizados |
| **Integração em apps** | Recursos de IA em plataformas existentes | Microsoft 365 Copilot, Grammarly |

### ⚠️ Riscos e Desafios

> 🚨 **Regra crítica:** As saídas dos modelos **não garantem correção**. Modelos treinados em dados tendenciosos podem perpetuar estereótipos e gerar discriminação — estabeleça estruturas de avaliação e loops de feedback com revisores humanos.

- **Viés:** Dados de treinamento tendenciosos → saídas discriminatórias
- **Custos:** Chamadas de API, hospedagem de modelos, serviços de nuvem
- **Transparência:** Informe os usuários sobre capacidades e limitações do modelo
- **Privacidade:** Dados enviados via API podem ser expostos ao provedor do modelo

---

## 🧩 Componentes da Solução de IA Generativa

No cerne das soluções de IA generativa estão os **grandes modelos de linguagem (LLMs)**. Os principais componentes ao projetar aplicações com IA generativa incluem:

| Componente | Função | Tecnologias |
|---|---|---|
| **Interface do Usuário (UI)** | Ponte entre usuário e modelo | React, Gradio, Streamlit |
| **Lógica da Aplicação** | Processa entrada, gerencia fluxo, valida saída | LangChain, Python |
| **Bancos de Dados** | Histórico de usuário, dados RAG, busca semântica | PostgreSQL, ChromaDB, Pinecone |
| **APIs** | Conectam a serviços e modelos externos | OpenAI API, REST APIs |

> 💡 **Bancos de dados vetoriais** são essenciais para soluções RAG — armazenam embeddings para busca semântica eficiente. **Guard rails** e **frameworks de avaliação** na camada de lógica garantem respostas não tendenciosas e sem vazamento de dados.

---

## 📱 Exemplo: Geração de Posts para Mídias Sociais

Este tópico ilustra a criação de um recurso de mídia social onde um prompt é elaborado para gerar um post. A aplicação coleta: **nome do produto**, **persona do público-alvo** e **característica a promover**, então engendra o prompt e processa a resposta. Importante: o parâmetro `max_tokens` afeta diretamente o custo da chamada de API.

---

## 🤖 Construindo um Agente de Saúde e Bem-Estar

Um **agente de IA** é um programa de software que executa tarefas automatizadas imitando processos de tomada de decisão humanos. Como LLMs são capazes de raciocínio e planejamento, eles podem ser usados para criar agentes via **function calling** (OpenAI) ou **LangChain**.

### Ciclo ReAct do Agente

```
┌─────────────────────────────────────────────────┐
│                 CICLO DO AGENTE                  │
│                                                  │
│  🧠 THOUGHT → Analisa o problema e planeja       │
│       ↓                                          │
│  ⚡ ACTION  → Busca dados externos (APIs, DBs)   │
│       ↓                                          │
│  👁️ OBSERVE → Recebe resultado e refina          │
│       ↓                                          │
│  🔄 (repete até concluir a tarefa)               │
└─────────────────────────────────────────────────┘
```

| Fase | Descrição | Exemplo |
|---|---|---|
| **Thought** | Divide o problema em etapas gerenciáveis | "Preciso verificar a dieta e o histórico de saúde" |
| **Action** | Interage com fontes externas (DB, APIs, web) | Consulta banco de dados nutricional |
| **Observation** | Registra resultado e usa para raciocínios futuros | "Déficit calórico de 500 kcal/dia detectado" |

> 💡 A metodologia **ReAct (Reasoning and Acting)** combina rastros de raciocínio e ações específicas, permitindo que o agente busque ativamente novas informações e atualize seu entendimento.

---

## 🎯 Design de uma Solução de Gerenciamento de Projetos

Este capítulo aborda o design e a construção de um assistente de gerenciamento de projetos. O processo envolve três etapas:

**1. Definir as Tarefas:** Usar chamadas de função (function calling) para interagir com sistemas externos — recuperação de tarefas, relatórios, alocação de recursos e agendamento.

**2. Definir Histórias de Usuário:** Mapear a intenção do usuário para funções e parâmetros específicos. Exemplo: "Quais são minhas tarefas para hoje?" → identifica `user_id` e `data_atual` como parâmetros.

**3. Definir Prompts e Templates:** Fornecer instruções claras sobre as capacidades do assistente; usar templates para guiar o fluxo da conversa.

### Function Calling

> 💡 **Function calling** define um formato de resposta consistente, garantindo que a saída da IA se ajuste a uma estrutura predefinida que outros sistemas possam interpretar e utilizar facilmente — por exemplo, chamar uma API de clima em tempo real.

### Estratégias de Design de UI/UX

| Estratégia | Descrição |
|---|---|
| **Campos de Formulário** | Traduzem entradas do usuário em prompts estruturados; cada campo mapeia a um parâmetro do LLM |
| **Placeholders e tooltips** | Guiam o usuário sobre o formato esperado |
| **Reconhecimento de Intenção** | Analisa linguagem, mapeia para respostas/ações específicas |
| **Avatares** | Adicionam dimensão visual e pessoal; tornam interações mais envolventes |
| **Feedback e confirmação** | Cruciais para UIs conversacionais — o usuário precisa saber que foi entendido |

---

## 🎯 Key Takeaways

- A IA generativa é estruturada em **3 camadas**: infraestrutura, modelo/plataforma e aplicação — cada uma com responsabilidades distintas.
- LLMs são **stateless**: toda conversa contextual requer enviar o histórico completo na janela de contexto.
- **Engenharia de prompt** na camada de aplicação define a qualidade da resposta — entradas mal estruturadas geram saídas de baixa qualidade.
- Soluções GenAI eficazes combinam: **UI** → **lógica de aplicação** (com guard rails) → **LLM** → **bancos de dados vetoriais** para RAG.
- **Agentes ReAct** (Thought → Action → Observation) permitem que LLMs interajam com sistemas externos de forma autônoma.
- **Function calling** é essencial para integrar respostas de LLM com APIs e sistemas externos de forma estruturada.
- Estabeleça sempre **estruturas de avaliação** e **loops de feedback** para mitigar viés e garantir qualidade das saídas.

---

[Construindo Soluções com Bancos de Dados Vetoriais →](2_Building_Solutions_with_Vector_Databases.md)