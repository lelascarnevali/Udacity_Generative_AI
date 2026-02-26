# 🦜 Desenvolvendo Soluções de IA Generativa com LangChain

## 🌍 O Papel do LangChain no Desenvolvimento com LLMs

Historicamente, integrar IA em aplicações exigia coletar vastos dados, contratar cientistas de dados, construir e treinar modelos especializados — um processo de semanas ou meses. Com os avanços em **LLMs** de provedores como OpenAI, Google e Anthropic, a paisagem mudou: os modelos interagem via APIs REST simples e executam diversas tarefas de PLN (chatbots, geração de conteúdo, tradução, análise de sentimento, Q&A, recomendação, dados sintéticos).

Porém, usar LLMs diretamente apresenta desafios:

| Desafio | Descrição |
|---|---|
| **Manipulação de Dados** | Terabytes espalhados por diferentes BDs e aplicações |
| **Janela de Contexto** | Limita o tamanho da requisição (200 a 5.000 palavras); LLMs são *stateless* |
| **Saída Não Estruturada** | LLMs não geram JSON nativamente — requer prompt engineering cuidadoso |

> 💡 **LangChain** resolve esses desafios com componentes pré-construídos para carregamento de dados, prompt templates, análise de saída e memória contextual.

---

## 🧩 Introdução ao LangChain

**LangChain** é um framework popular para construir aplicações com LLMs. Oferece componentes pré-construídos montáveis em **cadeias** reutilizáveis. Suporta Python, JavaScript e TypeScript — este material foca em **Python**.

O componente central é a abstração **LLM**, que oculta a implementação subjacente — o mesmo código funciona com OpenAI, Hugging Face, Google e Anthropic.

### Tipos de Modelos LangChain

| Tipo | Entrada | Saída | Uso Ideal |
|---|---|---|---|
| **Completion Models** | Texto | Extensão semântica | Completar/expandir textos |
| **Chat-Oriented Models** | Array de mensagens | Resposta de chat | Chatbots e aplicações interativas |

Ambos implementam a mesma interface base — consistência e flexibilidade para construir aplicações que trabalham com os dois tipos.

---

## ⚡ Utilizando o Componente LLM

Para utilizar o componente LLM do OpenAI no LangChain, inicialize um objeto `OpenAI` e passe um *prompt* para obter uma resposta.

**Conceitos Importantes**:

* **`completion_model_name` (GPT-3.5 Turbo Instruct)**: Modelo apropriado para cenários de conclusão de texto.
* **`temperature`**: Um parâmetro que controla a aleatoriedade das respostas da IA. Uma temperatura mais alta resulta em saídas mais variadas e criativas, enquanto uma configuração mais baixa produz respostas mais previsíveis.
* **`max_tokens`**: Um parâmetro que define o comprimento máximo da resposta da IA, crucial para controlar o tamanho da saída.

Exemplo de código para modelos de conclusão:

```python
from langchain_openai import OpenAI # Mudança para langchain_openai

completion_model_name = "gpt-3.5-turbo-instruct"
temperature = 0.0
completion_llm = OpenAI(model=completion_model_name, temperature=temperature, max_tokens=100) # 'model_name' foi alterado para 'model'

print("=== Completion Response ===")
print(completion_llm.invoke("You're a whimsical tour guide to France. Paris is a ")) # 'invoke' é o método moderno para chamar
```

Para **Modelos de Chat**, como o GPT 3.5 Turbo, o componente é `ChatOpenAI`. A inicialização é semelhante, mas em vez de passar um *prompt* diretamente, você passa um **array de mensagens**. Essas mensagens podem ser de diferentes tipos:

* **`SystemMessage`**: Define o comportamento ou persona do modelo (ex: "Você é um guia turístico francês").
* **`HumanMessage`**: Representa a entrada do usuário (ex: "Descreva Paris em um estilo caprichoso").
* **`AIMessage`**: Representa as respostas anteriores do modelo de IA (útil para manter o histórico da conversa).

Exemplo de uso do `ChatOpenAI`:

```python
from langchain_openai import ChatOpenAI # Mudança para langchain_openai
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage # Mudança para langchain_core.messages


chat_model_name = "gpt-3.5-turbo"
temperature = 0.0
chat_llm = ChatOpenAI(model=chat_model_name, temperature=temperature, max_tokens=100) # 'model_name' foi alterado para 'model'

messages = [
    SystemMessage(content="You are a French tour guide"),
    HumanMessage(content="Describe Paris in a whimsical style")
]

print("=== Chat Response ===")
print(chat_llm.invoke(messages)) # 'invoke' é o método moderno para chamar
```

Note que o parâmetro `temperature` pode ser ajustado para controlar a criatividade da resposta. Um `temperature` de 0.7, por exemplo, levará a uma saída mais variada e criativa.

```python
from langchain_openai import OpenAI # Mudança para langchain_openai

model_name = "gpt-3.5-turbo" # Este modelo é um modelo de chat, mas o exemplo de código original usa OpenAI para ele.
temperature = 0.7
llm = OpenAI(model=model_name, temperature=temperature, max_tokens=500) # 'model_name' foi alterado para 'model'

output = llm.invoke("What is Paris?") # 'invoke' é o método moderno para chamar
print("=== Response ===")
print(output)
```

---

## 📝 Utilizando Prompt Templates

**Prompt Templates** geram prompts estruturados e consistentes — funcionam como estênceis predefinidos em Python.

| Benefício | Descrição |
|---|---|
| **Estrutura e Consistência** | Prompts mantêm a mesma estrutura mesmo com detalhes diferentes |
| **Reusabilidade** | Templates reutilizáveis com inserção de detalhes específicos |
| **Partial Formatting** | Preenche partes do template enquanto mantém flexibilidade para outros |
| **Prompt Pipelining** | Monta partes de texto em ordem específica para prompts de chat |

**Tipos de prompt templates no LangChain:**

1.  **`PromptTemplate`**: Para *prompts* simples de entrada/saída.

    ```python
    from langchain.prompts import PromptTemplate

    template = PromptTemplate(
        template="Você é um guia turístico. Me conte algo interessante sobre {cidade}.",
        input_variables=["cidade"]
    )

    prompt = template.format(cidade="Paris")
    print(prompt)
    ```

2.  **`ChatPromptTemplate`**: Similar ao `PromptTemplate`, mas projetado para modelos de chat, permitindo diferentes tipos de mensagens (sistema, humano, etc.).

    ```python
    from langchain_core.prompts import ChatPromptTemplate # Mudança para langchain_core.prompts
    from langchain_core.messages import HumanMessage, SystemMessage # Mudança para langchain_core.messages

    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="Você é um assistente prestativo."),
            HumanMessage(content="Qual o capital de {pais}?")
        ]
    )

    messages = chat_template.format_messages(pais="Brasil")
    print(messages)
    ```

3.  **`FewShotPromptTemplate`**: Permite fornecer exemplos (*few-shot examples*) dentro do *prompt* para guiar o modelo a gerar respostas mais precisas. Isso é particularmente útil para tarefas que exigem um estilo ou formato de saída específico. Os exemplos são passados como uma lista de dicionários.

    ```python
    from langchain.prompts import FewShotPromptTemplate, PromptTemplate

    examples = [
        {"pergunta": "Qual a capital do Brasil?", "resposta": "Brasília."},
        {"pergunta": "Qual a capital da Argentina?", "resposta": "Buenos Aires."}
    ]

    example_formatter_template = "Pergunta: {pergunta}\nResposta: {resposta}"
    example_prompt = PromptTemplate(
        input_variables=["pergunta", "resposta"],
        template=example_formatter_template
    )

    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="Responda as seguintes perguntas com base nos exemplos:\n",
        suffix="Pergunta: {nova_pergunta}\nResposta:",
        input_variables=["nova_pergunta"],
        example_separator="\n\n"
    )

    prompt = few_shot_prompt.format(nova_pergunta="Qual a capital do Japão?")
    print(prompt)
    ```

---

## 🧠 Resolução de Problemas com Cadeias de Pensamento (CoT)

Em cenários onde LLMs falham em problemas complexos (ex: matemática), a técnica **Chain-of-Thought (CoT)** instrui o modelo a detalhar os passos do raciocínio antes da resposta final — melhorando a precisão.

Implementação no LangChain: combinar `FewShotPromptTemplate` com exemplos que demonstram raciocínio passo a passo.

Exemplo de estrutura de *prompt* para CoT:

```
Problema: [Problema de matemática]
Raciocínio:
1. Primeiro, [passo 1].
2. Em seguida, [passo 2].
3. Finalmente, [passo 3].
Resposta: [Resposta final]
```

Ao fornecer exemplos detalhados de raciocínio, o LLM é incentivado a seguir um processo semelhante para novos problemas, levando a soluções mais corretas.

---

## 🔗 Chains (Cadeias)

**Chains** são sequências de chamadas a componentes — permitem compor múltiplos elementos em fluxos de trabalho modulares. Uma chain pode incluir outras chains.

A combinação mais básica e comum é **PromptTemplate + LLM = LLMChain**.

| Benefício | Descrição |
|---|---|
| **Modularidade** | Divide tarefas complexas em componentes menores e reutilizáveis |
| **Flexibilidade** | Combináveis de diversas maneiras para diferentes necessidades |
| **Clareza** | Torna o fluxo de dados e operações mais transparente |

---

## 🎬 Demonstração de uma Chain Básica

Uma `LLMChain` combina `PromptTemplate` + `LLM` (ou `ChatModel`) — formata o prompt e envia ao LLM para obter a saída.

Exemplo de uso de uma `LLMChain`:

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# 1. Configurar o LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=1.2) # Temperatura de 1.2 para saída mais criativa/aleatória

# 2. Configurar o Prompt Template
prompt_template = PromptTemplate(
    input_variables=["story_type", "person"],
    template="Aja como Marvin, um Robô do Guia do Mochileiro das Galáxias. Me conte uma história {story_type} sobre {person}."
)

# 3. Criar a LLMChain
chain = LLMChain(llm=llm, prompt=prompt_template)

# 4. Invocar a Chain
response = chain.invoke({"story_type": "engraçada", "person": "um programador"})
print(response['text'])
```

Neste exemplo:
* O `ChatOpenAI` é inicializado com um `temperature` de 1.2 para incentivar uma saída mais aleatória e criativa.
* O `PromptTemplate` define a estrutura do *prompt* com *placeholders* para `story_type` e `person`.
* A `LLMChain` combina o `llm` e o `prompt_template`.
* Finalmente, `chain.invoke()` é usado para chamar a *chain*, passando os valores para os *placeholders* do *prompt*.

---

## 📊 Caso de Uso: Análise de Sentimento

LLMs podem analisar sentimento em avaliações de produtos e gerar saída em CSV para consumo por outras aplicações.

> 💡 **Dica:** Use `temperature=0` para garantir respostas determinísticas e aderentes ao formato solicitado. Combine prompt engineering com **Output Parsers** para transformar texto não estruturado em objetos estruturados.

Exemplo de *prompt* para análise de sentimento e geração de CSV:

```
Gerar um CSV com as seguintes colunas:
nome_da_avaliacao, sentimentos, resumo_da_avaliacao, entidades

Texto da avaliação: "Este produto é incrível! Adorei a funcionalidade."
```

Para garantir que o LLM forneça uma saída estruturada e que esta seja facilmente consumível, a combinação de *prompt engineering* com **Output Parsers** é essencial.

---

## 📂 Document Loaders (Carregadores de Documentos)

**Document Loaders** são abstrações para carregar documentos LangChain de diversas fontes (BDs, CSVs, Wikipedia, etc.).

Um **Documento LangChain** tem dois campos:
- **`page_content`**: dados principais (o texto)
- **`metadata`**: dicionário com metadados (fonte, data de criação, etc.)

Exemplo com `CSVLoader`:

```python
from langchain_community.document_loaders import CSVLoader

# Supondo que 'reviews.csv' seja um arquivo CSV com as avaliações
loader = CSVLoader(file_path='reviews.csv') # Inicializa um CSVLoader
documents = loader.load() # Realiza a leitura e processamento do arquivo

for doc in documents:
    print(f"Conteúdo: {doc.page_content}")
    print(f"Metadados: {doc.metadata}")
    print("-" * 20)
```

Os `Document Loaders` são o primeiro passo para trazer dados externos para o ecossistema LangChain, permitindo que os LLMs processem e interajam com essas informações.

---

## 🔧 Output Parsers (Analisadores de Saída)

As respostas dos LLMs são texto não estruturado — **Output Parsers** transformam esse texto em objetos estruturados (JSON, CSV) prontos para consumo.

A integração com **Pydantic** é poderosa: defina um esquema de dados e o parser garante que a saída do LLM se ajuste a ele.

Exemplo de uso de um `StructuredOutputParser` com Pydantic:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate # Mudança para langchain_core.prompts
from langchain_core.output_parsers import PydanticOutputParser # Mudança para langchain_core.output_parsers
from langchain_core.pydantic_v1 import BaseModel, Field # Mudança para langchain_core.pydantic_v1
from langchain_core.messages import HumanMessage, SystemMessage # Mudança para langchain_core.messages

# 1. Definir o modelo Pydantic para a saída desejada
class ReviewAnalysis(BaseModel):
    nome_da_avaliacao: str = Field(description="O nome da avaliação do produto")
    sentimentos: str = Field(description="Os sentimentos gerais expressos na avaliação (positivo, negativo, neutro)")
    resumo_da_avaliacao: str = Field(description="Um breve resumo da avaliação")
    entidades: list[str] = Field(description="Uma lista de entidades importantes mencionadas na avaliação")

# 2. Criar o parser a partir do modelo Pydantic
parser = PydanticOutputParser(pydantic_object=ReviewAnalysis)

# 3. Configurar o LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 4. Criar o Prompt Template com as instruções do parser
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="Você é um assistente útil que extrai informações de avaliações de produtos."),
        HumanMessage(content="Analise a seguinte avaliação e retorne a saída no formato JSON:\n{format_instructions}\n\nAvaliação: {review_text}")
    ]
).partial(format_instructions=parser.get_format_instructions()) # Injeta as instruções de formato do parser no prompt

# 5. Criar a Chain (Prompt + LLM + Parser)
chain = prompt | llm | parser

# 6. Invocar a Chain
review_text = "O novo smartphone é excelente! A bateria dura muito e a câmera é fantástica."
parsed_output = chain.invoke({"review_text": review_text})

print(parsed_output)
print(type(parsed_output))
```

Neste exemplo:
* Um modelo Pydantic `ReviewAnalysis` é definido para especificar a estrutura da saída esperada.
* `PydanticOutputParser` é usado para criar um parser a partir deste modelo.
* As instruções de formato geradas pelo parser (`parser.get_format_instructions()`) são injetadas no `ChatPromptTemplate`, informando ao LLM exatamente como formatar sua resposta.
* A `chain` é criada usando o operador `|` (pipe), que encadeia o *prompt*, o LLM e o parser. Isso garante que a saída do LLM seja automaticamente passada para o parser.
* A saída final `parsed_output` será um objeto Python que adere ao esquema `ReviewAnalysis`, permitindo fácil acesso aos dados estruturados.

Os Output Parsers são cruciais para transformar as capacidades de geração de texto dos LLMs em dados consumíveis e utilizáveis por aplicações de software.

---

## 🔎 Recuperação Aumentada de Geração (RAG)

**Retrieval Augmented Generation (RAG)** aprimora LLMs integrando-os com dados da empresa — aproveitando o poder dos modelos e as informações específicas do negócio.

### Pipeline RAG

```
Consulta do usuário
        ↓
  [Text Embedding Model]
        ↓
  Vetor de consulta
        ↓
  [Vector Storage — ChromaDB / Pinecone]
        ↓
  Top-k documentos semanticamente próximos
        ↓
  Consulta original + documentos recuperados → [LLM]
        ↓
  Resposta contextualizada e precisa
```

| Componente | Função |
|---|---|
| **Document Transformers** | Dividem documentos grandes em chunks menores para indexação mais precisa |
| **Text Embedding Models** | Convertem chunks em vetores que capturam significado semântico |
| **Vector Storage** | Armazena embeddings prontos para recuperação |
| **Retrievers** | Buscam chunks semanticamente relevantes para o LLM processar |

> 💡 O **Vector Store Index Creator** integra BDs vetoriais, embeddings e retrievers, simplificando a configuração de um sistema RAG.

**Exemplo de Código**:

```python
from langchain_community.indexes import VectorstoreIndexCreator # Mudança para langchain_community.indexes
from langchain_community.document_loaders.csv_loader import CSVLoader # Mudança para langchain_community.document_loaders.csv_loader

loader = CSVLoader(file_path='./tv-reviews.csv')

index = VectorstoreIndexCreator().from_loaders([loader])

query = "Based on the reviews in the context, tell me what people liked about the picture quality"
response = index.query(query) # 'query' é o método moderno para chamar
print(response)
```

O intercâmbio de separadores de caracteres, embeddings e bancos de dados vetoriais permite que o sistema imite a compreensão humana de contexto e nuances.

---

## 💾 Componente de Memória LangChain

Como LLMs são *stateless*, processam cada interação isoladamente. O **Componente de Memória LangChain** simula estado contínuo: armazena e recupera contexto conforme necessário, permitindo que LLMs "lembrem" detalhes além da janela de contexto imediata.

**`ConversationBufferMemory`** mantém histórico de mensagens de chat — cada mensagem do usuário e resposta do chatbot é registrada e fornecida como contexto nas chamadas subsequentes.

> 💡 **Exemplo:** Um chatbot perguntado sobre Paris fornece uma descrição. Na pergunta seguinte — "Como chego lá a partir de Nova York?" — sem citar Paris novamente — graças ao histórico completo, o chatbot interpreta corretamente a questão como "viajar de Nova York para Paris".

---

## 🔀 Tipos de Chains no LangChain

| Tipo de Chain | Propósito | Exemplo Prático |
|---|---|---|
| **Router Chain** | Sequências dinâmicas e não determinísticas baseadas em contexto | Chatbot que roteia consultas de eletrônicos, software ou eletrodomésticos para módulos especializados |
| **Sequential Chain** | Saída de uma etapa é entrada da próxima | Criar descrição de produto → gerar avaliação usando essa descrição |
| **Transformation Chain** | Altera/processa entradas em vários pontos da sequência | Extrair transcrição de vídeo → remover timestamps → resumir texto |

> 💡 Cada tipo de chain serve um propósito distinto — combinando-as, é possível construir aplicações de IA sofisticadas e sensíveis ao contexto.

---

## 🎯 Key Takeaways

- **LangChain** resolve os principais desafios de trabalhar com LLMs: dados dispersos, janela de contexto limitada e saída não estruturada.
- A abstração **LLM** do LangChain permite trocar de provedor (OpenAI → Anthropic → Google) sem alterar o código da aplicação.
- **Completion Models** recebem texto e estendem; **Chat Models** recebem arrays de mensagens e respondem em formato conversacional.
- **Prompt Templates** garantem estrutura, consistência e reusabilidade — use `FewShotPromptTemplate` para implementar **Chain-of-Thought**.
- **Chains** (LLMChain, RouterChain, SequentialChain) composem componentes em fluxos de trabalho modulares e reutilizáveis.
- **Document Loaders** + **Output Parsers** + **Pydantic** transformam dados externos em saídas estruturadas prontas para uso.
- **RAG** (Retrieval Augmented Generation) combina embeddings vetoriais + banco de dados vetorial + LLM para respostas informadas com dados privados da empresa.
- **ConversationBufferMemory** simula estado em LLMs stateless — essencial para chatbots com histórico de conversa.

---

[← Construindo Soluções com Bancos de Dados Vetoriais](2_Building_Solutions_with_Vector_Databases.md)