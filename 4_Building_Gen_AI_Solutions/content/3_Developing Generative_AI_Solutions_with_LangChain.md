### 1. Introdução ao Desenvolvimento de Soluções de IA Generativa
Historicamente, a integração de capacidades de IA em aplicações era um desafio considerável. Isso envolvia a coleta de vastas quantidades de dados, a contratação de cientistas de dados e especialistas em aprendizado de máquina, a construção e treinamento de modelos especializados, e a avaliação de seu desempenho. Todo esse processo exigia tempo e recursos significativos, e poderia levar semanas, ou até meses.

Com os avanços recentes em **Modelos de Linguagem Grande (LLMs)** de provedores como OpenAI, Google e Anthropic, a paisagem da IA mudou drasticamente. Os LLMs são algoritmos de aprendizado profundo que podem realizar diversas tarefas de processamento de linguagem natural. Treinados em *datasets* massivos, eles podem reconhecer, resumir, traduzir, prever e gerar texto, e geralmente interagem via APIs REST simples.

Aplicações práticas de LLMs incluem *chatbots*, geração de conteúdo, tradução de idiomas, análise de sentimento, sumarização de texto, sistemas de perguntas e respostas, recomendações personalizadas e geração de dados sintéticos.

No entanto, o uso de LLMs apresenta seus próprios desafios:

* **Manipulação de Dados**: Desenvolvedores podem precisar lidar com terabytes de dados espalhados por diferentes bancos de dados e aplicações.
* **Limitação da Janela de Contexto**: Modelos LLM populares limitam o tamanho da requisição que podem processar (geralmente entre 200 a 5.000 palavras). LLMs, por natureza, são modelos sem estado (*stateless*), o que significa que não retêm informações de interações passadas nem possuem um entendimento inerente do contexto de negócio além do texto sendo analisado. Essa ausência de memória contextual pode limitar sua eficácia em tarefas que exigem uma compreensão de conversas ou interações estendidas. Eles analisam cada pedaço de texto isoladamente, carecendo da capacidade de referenciar trocas ou entradas anteriores, o que pode ser uma limitação crítica para tarefas sequenciais ou aplicações que exigem um diálogo contínuo.
* **Ausência de Saída Estruturada Nata**: LLMs não produzem nativamente dados em formatos estruturados como JSON. Essa limitação exige que os desenvolvedores instruam corretamente o LLM para produzir respostas em um formato estruturado que suas aplicações possam usar prontamente, o que requer formulação cuidadosa da *query* e potencial processamento adicional para obter a saída estruturada desejada.

É neste cenário que o **LangChain** se torna fundamental. LangChain é um *framework* popular que simplifica muitos dos problemas comuns que os desenvolvedores encontram ao trabalhar com LLMs, oferecendo um rico conjunto de instruções que simplificam o carregamento de dados de várias fontes, *prompts* de LLM templatizados, análise da saída do LLM e adição de memória contextual às interações com LLMs.

---
### 2. Introdução ao LangChain
**LangChain** é um *framework* popular projetado para desenvolvedores que constroem aplicações impulsionadas por grandes modelos de linguagem. Ele oferece um extenso conjunto de componentes pré-construídos que simplificam muitas tarefas comuns nessa área, além de um método para montar esses componentes em "cadeias" reutilizáveis. O LangChain pode ser utilizado com Python, JavaScript e TypeScript, mas neste material, o foco será exclusivamente em **Python**.

Um dos componentes mais cruciais no LangChain é a abstração chamada **LLM**, que oculta a implementação subjacente do modelo de linguagem grande. Isso permite que o mesmo código seja usado com modelos de diversos provedores, como OpenAI, Hugging Face, Google e Anthropic. Este componente é frequentemente referido simplesmente como "modelo", pois abstrai os Large Language Models.

Os LLMs no LangChain se dividem em duas categorias principais:

* **Modelos de Conclusão (*Completion Models*)**: Estes modelos recebem uma entrada de texto e fornecem uma extensão semântica. São ideais para tarefas que envolvem expandir ou completar um texto dado.
* **Modelos Orientados a Chat (*Chat-Oriented Models*)**: Projetados para conversas, estes modelos podem receber um diálogo entre um usuário e uma IA e fornecer conclusões ou respostas semânticas. São particularmente adequados para aplicações interativas.

Ambos os tipos de modelo, de conclusão e de chat, implementam a mesma interface base, o que confere consistência e flexibilidade na construção de aplicações que podem trabalhar com ambos os tipos de modelos.

---
### 3. Utilizando o Componente LLM
Para utilizar o componente LLM do OpenAI no LangChain, é necessário inicializar um objeto `OpenAI` e atribuí-lo a uma variável. Em seguida, essa variável pode ser usada como uma função Python, passando um *prompt* para ela para obter uma resposta.

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
### 4. Utilizando Prompt Templates
**Prompt Templates** são ferramentas essenciais para gerar respostas ou conteúdo estruturados e consistentes usando Large Language Models. Eles permitem que você forneça um formato específico e *placeholders* de contexto para a geração de texto, sendo úteis em várias aplicações, desde *chatbots* até a geração de conteúdo.

No seu cerne, *prompt templates* são muito semelhantes aos formatos de string. Em Python, eles funcionam como um estêncil, um padrão predefinido que ajuda a gerar a entrada para uma conversa com o modelo de linguagem.

A importância dos *prompt templates* reside em:

* **Estrutura e Consistência**: Eles garantem que os *prompts* mantenham a mesma estrutura, mesmo que os detalhes específicos (como cidade ou data) mudem. Essa consistência é crucial para garantir que o modelo de linguagem responda de forma previsível e confiável.
* **Reusabilidade**: Uma vez criados, os *templates* podem ser reutilizados quantas vezes forem necessárias, exigindo apenas a inserção de detalhes específicos.
* **Formatação Parcial (*Partial Formatting*)**: Permite preencher certas partes de um *template* (como um nome) enquanto deixa flexibilidade para adicionar outros detalhes (como um local) posteriormente.
* **Pipelining de Prompts (*Prompt Pipelining*)**: Envolve a montagem de diferentes partes de texto em uma ordem específica, sendo particularmente útil em *prompts* de chat onde cada mensagem pode precisar de uma elaboração individual.

Existem diferentes tipos de *prompt templates* no LangChain:

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
### 5. Resolução de Problemas com Cadeias de Pensamento
Em cenários onde os LLMs falham em resolver problemas complexos diretamente, como problemas de matemática, a técnica de **cadeia de pensamento (Chain-of-Thought - CoT)** pode ser empregada. A cadeia de pensamento envolve instruir o LLM a detalhar os passos do seu raciocínio antes de fornecer a resposta final. Isso ajuda o modelo a "pensar" de forma mais estruturada, melhorando a precisão de suas respostas.

Para implementar CoT no LangChain, podemos combinar o `FewShotPromptTemplate` com exemplos que demonstram o processo de raciocínio passo a passo.

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
### 6. Chains (Cadeias)
As **Chains** no LangChain são componentes fundamentais que permitem a composição de múltiplos componentes em um todo coerente. Imagine a criação de um hambúrguer perfeito: um único ingrediente é delicioso por si só, mas a combinação de vários ingredientes cria uma refeição muito mais rica. Essa analogia se aplica às *chains*: elas são uma maneira de costurar múltiplas funções e operações para alcançar uma saída desejada.

No seu cerne, uma *chain* é simplesmente uma sequência de chamadas para vários componentes. Esses componentes podem inclusive incluir outras *chains*, permitindo a construção de fluxos de trabalho complexos e modulares.

A combinação de um *prompt template* e um **LLM** é uma das *chains* mais básicas e comuns, conhecida como **LLMChain**. Essa *chain* permite que você formate um *prompt* usando o *template* e, em seguida, passe o *prompt* formatado para o LLM para obter uma resposta.

Os benefícios das *chains* incluem:

* **Modularidade**: Permitem dividir tarefas complexas em componentes menores e reutilizáveis.
* **Flexibilidade**: Podem ser combinadas de diversas maneiras para atender a diferentes necessidades.
* **Clareza**: Tornam o fluxo de dados e operações mais transparente.

---
### 7. Demostração de uma Chain Básica
Uma `LLMChain` é uma combinação poderosa de um `PromptTemplate` e um `LLM` (ou `ChatModel`). Ela facilita a passagem de entradas para um *prompt*, formatando-o e, em seguida, enviando-o para o LLM para obter uma saída.

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
### 8. Caso de Uso para Análise de Sentimento
Os LLMs podem ser usados para tarefas como análise de sentimento em avaliações de produtos, onde a saída precisa estar em um formato estruturado, como CSV, para facilitar o consumo por outras aplicações.

Para isso, é crucial instruir o LLM a gerar a saída no formato desejado e, em seguida, usar um **Output Parser** para transformar o texto gerado em um objeto estruturado. A temperatura do modelo deve ser definida como 0 para garantir respostas mais determinísticas e aderentes ao formato solicitado.

Exemplo de *prompt* para análise de sentimento e geração de CSV:

```
Gerar um CSV com as seguintes colunas:
nome_da_avaliacao, sentimentos, resumo_da_avaliacao, entidades

Texto da avaliação: "Este produto é incrível! Adorei a funcionalidade."
```

Para garantir que o LLM forneça uma saída estruturada e que esta seja facilmente consumível, a combinação de *prompt engineering* com **Output Parsers** é essencial.

---
### 9. Document Loaders (Carregadores de Documentos)
No LangChain, um **Document Loader** é uma abstração para carregar documentos LangChain a partir de diversas fontes de dados, como bancos de dados, arquivos CSV, Wikipedia, etc.

Um **Documento LangChain** é uma classe que encapsula conteúdo não estruturado, como texto simples. Ele consiste em:

* **`page_content`**: Um campo que contém os dados principais (o texto do documento).
* **`metadata`**: Um dicionário que armazena metadados associados ao documento (por exemplo, a fonte do documento, a data de criação, etc.).

Para carregar dados de um arquivo CSV, por exemplo, você pode usar um `CSVLoader`.

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
### 10. Output Parsers (Analisadores de Saída)
Uma vez que os dados são carregados e processados por um LLM, a resposta do LLM é tipicamente um texto não estruturado. No entanto, para desenvolvedores, trabalhar com texto não estruturado diretamente não é eficiente. Preferimos uma saída estruturada, como JSON ou CSV, como vimos no exemplo da geração de avaliações de TV.

Os **Output Parsers** no LangChain permitem que você transforme a saída não estruturada do LLM em objetos estruturados que suas aplicações podem usar facilmente. A integração do LangChain com a biblioteca **Pydantic** é um recurso poderoso que facilita isso.

Usando Pydantic, você pode definir um esquema (modelo de dados) para a saída desejada, e o Output Parser se encarregará de analisar a resposta do LLM para que ela se ajuste a esse esquema.

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
### 11. Recuperação Aumentada de Geração (RAG)
**Retrieval Augmented Generation (RAG)** é uma técnica que aprimora as capacidades de Large Language Models (LLMs) ao integrá-los com dados da empresa, como uma base de conhecimento. Isso permite que as aplicações aproveitem tanto o poder dos LLMs quanto as informações específicas contidas nos próprios dados da empresa.

**Como funciona**:

1.  **Consulta do Usuário**: O processo começa com uma consulta do usuário, que é usada para pesquisar em um **banco de dados vetorial**. Bancos de dados vetoriais são essenciais para armazenar dados e adicionar informações adicionais, semanticamente relevantes, ao LLM.
2.  **Recuperação de Documentos**: O sistema recupera documentos que são semanticamente mais próximos da consulta.
3.  **Contextualização com LLM**: Os documentos recuperados são passados junto com a consulta original para o LLM. Isso fornece ao LLM contexto extra e informações atualizadas, resultando em uma resposta mais informada e precisa.
4.  **Transformadores de Documentos (*Document Transformers*)**: Utilizados para preparar dados, dividindo-os em pedaços menores. Isso é benéfico para indexar grandes documentos e alcançar uma correspondência mais precisa entre a consulta do usuário e o conteúdo do documento.
5.  **Modelos de Embedding de Texto (*Text Embedding Models*)**: Convertem os pedaços de documento em **embeddings** que capturam o significado semântico dos dados. Embeddings são representações numéricas de texto em um espaço de alta dimensão, onde significados semelhantes são colocados próximos.
6.  **Armazenamento Vetorial (*Vector Storage*)**: É onde os embeddings são armazenados, prontos para recuperação.
7.  **Recuperadores (*Retrievers*)**: Buscam os pedaços semanticamente relevantes para o LLM processar.

O sistema RAG permite o uso eficiente de LLMs, evitando sobrecarregá-los com dados e garantindo uma saída precisa e acurada. O **Vector Store Index Creator** integra os bancos de dados vetoriais, embeddings e recuperadores, simplificando o processo de configuração de um sistema de recuperação de informações.

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
### 12. Componente de Memória LangChain
O **Componente de Memória LangChain** é uma solução projetada para abordar as limitações dos LLMs na manutenção da continuidade conversacional.

Como os LLMs são sem estado (*stateless*), eles geralmente processam cada interação isoladamente, sem memória de trocas passadas. Isso apresenta desafios, como uma janela de contexto limitada e a ausência de histórico de conversas em interações sequenciais. A memória ajuda a superar as limitações de contexto, armazenando e recuperando o contexto conforme necessário, permitindo que os LLMs "lembrem" detalhes importantes além de sua janela de contexto imediata.

**Simulando um Estado Mantido**:
O Componente de Memória LangChain aborda tanto a questão de manter o estado contínuo da conversa quanto de resumir o diálogo.

* Permite a recuperação de toda a conversa em um tamanho gerenciável ou seu resumo à medida que cresce.
* Retém relevância e contexto em interações longas.
* Garante que os LLMs possam acessar versões resumidas para manter a continuidade sem perder o contexto.
* Aprimora a entrada do usuário com contexto antes de executar a lógica central e para armazenar interações para referência futura após a resposta.

1.  **`ConversationBufferMemory`**: Este componente é essencial para manter um histórico de mensagens de chat, permitindo que o *chatbot* tenha uma compreensão contextual da conversa em andamento.
    * Quando um usuário envia uma mensagem, ela é adicionada ao histórico da conversa, e da mesma forma, as respostas do *chatbot* também são registradas. Isso ajuda a fornecer contexto para as mensagens subsequentes do *chatbot*.
    * O buffer de memória da conversa pode gerar o histórico de chat como um fluxo contínuo ou como uma lista.
    * A string armazenada de mensagens de chat fornece contexto essencial para o modelo de linguagem (LM) ao gerar sua próxima mensagem.

**Exemplo de Caso de Uso**:
Em uma demonstração, um *chatbot* básico é criado usando uma cadeia de conversação com memória. Após ser perguntado sobre Paris e fornecer uma descrição, o usuário pergunta como chegar lá a partir de Nova York, sem mencionar Paris novamente. Graças ao acesso ao histórico completo da conversa, o *chatbot* interpreta corretamente a segunda pergunta como uma questão sobre como viajar de Nova York para Paris, demonstrando a importância do histórico completo da conversa.

---
### 13. Tipos de Cadeias em IA
As *chains* no LangChain permitem orquestrar operações complexas, combinando múltiplos componentes. Existem diferentes tipos de *chains*, cada uma com um propósito distinto:

1.  **Router Chain (Cadeia de Roteamento)**
    * **Propósito**: Permite sequências dinâmicas e não determinísticas de operações com base nas saídas de etapas anteriores.
    * **Aplicação**: Adapta as interações com um Large Language Model com base no contexto ou tipo de pergunta.
    * **Exemplo**: Um *chatbot* que lida com consultas de clientes sobre eletrônicos, software e eletrodomésticos. Ele identifica o tipo de consulta e roteia para o mecanismo de resposta apropriado.

2.  **Sequential Chain (Cadeia Sequencial)**
    * **Propósito**: Facilita uma série de operações onde a saída de uma é a entrada para a próxima.
    * **Aplicação**: Útil para processos que necessitam de múltiplas chamadas de modelo de linguagem ou funções em uma ordem específica.
    * **Exemplo**: Criar uma descrição de produto seguida pela geração de uma avaliação usando essa descrição.

3.  **Transformation Chain (Cadeia de Transformação)**
    * **Propósito**: Envolve a alteração ou processamento de entradas em vários pontos de uma sequência operacional.
    * **Aplicação**: Usada para criar *pipelines* para tarefas específicas.
    * **Exemplo**: Extrair transcrições de vídeo, remover carimbos de data/hora e, em seguida, resumir o texto.

Cada uma dessas cadeias serve a um propósito distinto, permitindo aplicações mais sofisticadas e sensíveis ao contexto de modelos de IA em vários cenários.