### 1. Introdução

Este curso tem como objetivo principal capacitar o aluno a construir um **chatbot de perguntas e respostas (Q&A) personalizado** utilizando a tecnologia **OpenAI**. Diferentemente dos modelos de conclusão de texto genéricos da OpenAI, o foco aqui é criar um bot capaz de fornecer respostas altamente precisas e relevantes, especialmente para **dados recentes** que podem não ter sido incluídos no treinamento original do modelo. Para isso, o fluxo de trabalho envolve a comparação da pergunta do usuário com um **conjunto de dados personalizado** para identificar contextos relevantes, que são então usados para construir um **prompt customizado** para o modelo de texto da OpenAI. O curso explora as ferramentas e técnicas necessárias para desenvolver esse chatbot, com atividades práticas para consolidar o aprendizado.

---
### 2. OpenAI e Prompt Engineering

A **OpenAI**, fundada em 2015, é uma renomada empresa de pesquisa em inteligência artificial, conhecida por seus modelos como **DALL-E** e **ChatGPT**. Seus modelos de linguagem são extremamente eficazes na compreensão e geração de texto, e sua API permite resolver uma vasta gama de tarefas relacionadas ao processamento de linguagem natural. A interação fundamental com esses modelos se dá através de **prompts de texto**.

**Prompt Engineering** é a arte de criar prompts eficazes para direcionar os modelos de IA a produzir as respostas desejadas. Existem duas abordagens principais:

* **Prompt Engineering Iterativo (Manual)**: Consiste em um processo de tentativa e erro, onde o usuário insere um prompt, analisa o resultado e o ajusta manualmente até obter a resposta desejada. Essa abordagem depende fortemente da habilidade e intuição do usuário.
* **Prompt Engineering Automatizado**: Essa abordagem minimiza a dependência da habilidade do usuário. Em vez de reformular a pergunta repetidamente, um sistema automatizado gera o prompt ideal para o modelo. No contexto deste curso, isso significa criar um prompt que incorpora **informações de contexto** relevantes, extraídas de um conjunto de dados personalizado. Isso é crucial para superar as limitações de dados de treinamento dos modelos, que geralmente têm uma data de corte (por exemplo, 2021), permitindo respostas mais precisas e específicas.

Para interagir com os modelos da OpenAI em Python, é necessário importar a biblioteca `openai` e configurar a chave da API, que autentica as requisições.

```python
import openai

# Configuração da chave da API da OpenAI
# Substitua "SUA_CHAVE_AQUI" pela sua chave real da API
openai.api_key = "SUA_CHAVE_AQUI"
```

---
### 3. Coleta de Dados

A base para um chatbot personalizado é um **conjunto de dados personalizado**. Este dataset é essencial para fornecer ao modelo o **contexto** necessário para gerar respostas diferenciadas. Um dataset personalizado pode incluir:

* **Novos dados**: Informações que não estavam presentes no treinamento original do modelo, como eventos pós-corte de treinamento (ex: após 2021).
* **Informações privadas**: Dados que não estavam publicamente disponíveis durante o treinamento do modelo.

As fontes para esses dados podem ser variadas:

* **Fontes dinâmicas da web (APIs)**: Ideais para acessar dados atualizados e em constante mudança, como wikis ou feeds de notícias. A desvantagem é a dependência da disponibilidade e formato da API.
* **Arquivos estáticos**: Documentos baixados e armazenados localmente, como planilhas, documentos Word ou arquivos de texto. Oferecem maior estabilidade para o código, mas as informações podem se tornar desatualizadas.

Este curso se concentra na coleta de dados a partir de **fontes de dados da web**.

---
### 4. Coleta de Dados com a Biblioteca Requests

A biblioteca **Requests** do Python é a ferramenta fundamental para recuperar dados da web. O processo de coleta de dados envolve os seguintes passos:

1.  **Definir a URL e os parâmetros da API**: É necessário especificar o endereço base da API (por exemplo, `https://en.wikipedia.org/w/api.php`) e os parâmetros específicos para a consulta (como `action`, `format`, `titles`, `prop`, `explaintext`). Esses parâmetros ditam qual informação será buscada e em que formato.
2.  **Fazer a requisição HTTP**: A função `requests.get()` é utilizada para enviar a solicitação à API, que retornará uma resposta.
3.  **Processar a resposta JSON**: As APIs geralmente retornam dados em formato JSON. É crucial navegar pela estrutura aninhada do JSON para extrair a informação desejada (por exemplo, `response.json()['query']['pages'][primeiro_resultado]['extract']`). Frequentemente, isso exige **encadear comandos Python** para acessar os dados específicos.

O exemplo prático utilizado no curso é a página da Wikipedia para o ano de 2022, escolhida especificamente porque os dados de treinamento dos modelos da OpenAI terminam em 2021, ilustrando a necessidade de dados recentes.

```python
import requests

# URL da API da Wikipedia para buscar informações
API_URL = "https://en.wikipedia.org/w/api.php"

# Parâmetros para a requisição:
# - action=query: Indica que queremos consultar a API.
# - format=json: Especifica que queremos a resposta em formato JSON.
# - titles=2022: Define o título da página a ser consultada (a página "2022").
# - prop=extracts: Solicita o conteúdo textual da página.
# - explaintext=True: Garante que o texto seja retornado em formato puro, sem formatação Wiki.
params = {
    "action": "query",
    "format": "json",
    "titles": "2022",
    "prop": "extracts",
    "explaintext": True,
}

# Realiza a requisição HTTP GET à API da Wikipedia
response = requests.get(API_URL, params=params)

# Converte a resposta JSON em um dicionário Python
data = response.json()

# Extrai o conteúdo principal da página "2022"
# A estrutura JSON pode ser aninhada, então navegamos até o texto desejado.
# list(data["query"]["pages"].keys())[0] pega o ID da página, que pode variar.
page_id = list(data["query"]["pages"].keys())[0]
text_content = data["query"]["pages"][page_id]["extract"]

# Exibe os primeiros 500 caracteres do texto coletado para verificação
print(text_content[:500])
```

---
### 5. Limpeza de Dados com Pandas

Antes que um conjunto de dados possa ser utilizado para personalizar um chatbot, ele precisa ser carregado e limpo em um formato que seja facilmente manipulável e utilizável. A biblioteca **Pandas** é a ferramenta ideal para essa finalidade, permitindo a manipulação de dados em formato de **planilha**, com linhas e colunas organizadas em **DataFrames**. As etapas essenciais de limpeza de dados incluem:

1.  **Carregar os dados**: O primeiro passo é importar os dados brutos (por exemplo, de um arquivo CSV ou de uma resposta de API) para um DataFrame do Pandas.
2.  **Remover linhas irrelevantes ou vazias**: Identificar e descartar quaisquer dados que não agreguem valor às respostas do chatbot, como linhas completamente vazias ou informações que não são contexto útil.
3.  **Renomear colunas**: É fundamental garantir que a coluna principal que contém o texto esteja consistentemente nomeada (geralmente como `text`), o que padroniza o acesso aos dados.
4.  **Limpeza de texto**: Este é um passo crítico que envolve o processamento do texto para remover caracteres indesejados (como quebras de linha ou caracteres especiais), duplicatas ou inconsistências. Isso pode ser feito através de:
    * Uso de **expressões regulares** para identificar e remover padrões específicos.
    * Divisão de textos longos em partes menores, se necessário, para otimizar o processamento.
    * Tratamento de informações de data para garantir que cada entrada de texto esteja corretamente associada à sua data, mantendo a cronologia se aplicável.
5.  **Reindexar o DataFrame**: Após todas as operações de limpeza, é uma boa prática resetar o índice do DataFrame para uma sequência numérica limpa, garantindo a organização e o acesso eficiente aos dados.

O objetivo final é ter um **DataFrame** limpo e bem estruturado, onde cada linha representa uma unidade de contexto valiosa e pronta para ser usada pelo chatbot. A coluna `text` deve estar impecável para a geração de embeddings.

```python
import pandas as pd
import re

# Cria um DataFrame de exemplo com o texto coletado do passo anterior.
# Em um cenário real, você carregaria os dados de um arquivo (CSV, Excel, etc.).
df = pd.DataFrame({"raw_text": [text_content]})

# 1. Remover linhas irrelevantes ou vazias (exemplo: remove linhas onde 'raw_text' é nulo)
df.dropna(subset=["raw_text"], inplace=True)

# 2. Renomear colunas para um nome padrão, como 'text'
df.rename(columns={"raw_text": "text"}, inplace=True)

# 3. Limpeza de texto:
# - re.sub(r'\s+', ' ', x): Substitui sequências de espaços em branco (incluindo quebras de linha) por um único espaço.
# - .strip(): Remove espaços em branco do início e do fim da string.
df["text"] = df["text"].apply(lambda x: re.sub(r'\s+', ' ', x).strip())

# 4. Reindexar o DataFrame: Reseta o índice para uma sequência numérica limpa, útil após remoção de linhas.
df.reset_index(drop=True, inplace=True)

# Exibe as primeiras linhas do DataFrame limpo para verificar o resultado
print(df.head())
```

---
### 6. Traduzindo Palavras em Números

Para que os computadores possam processar e "compreender" a linguagem natural, é essencial converter palavras e frases em representações numéricas. Contudo, essa tradução não pode ser arbitrária; ela deve capturar as **relações de significado** inerentes aos dados, permitindo que os modelos de IA identifiquem padrões e determinem o conteúdo mais relevante.

Alguns métodos de tradução numérica, embora existentes, são inadequados para modelos de linguagem avançados:

* **ASCII**: Atribui um código numérico a cada caractere. É muito limitado, pois não consegue capturar as relações semânticas entre as palavras. Por exemplo, "gato" e "cachorro", apesar de serem animais, não teriam nenhuma proximidade numérica aparente.
* **One-hot encoding**: Trata cada palavra como uma categoria única e cria um vetor de números binários (0s e 1s). Para cada palavra no vocabulário do modelo, uma coluna é criada; a presença da palavra é indicada por 1, e a ausência por 0.
    * **Vantagens**: Evita a suposição incorreta de ordem implícita que pode ocorrer com códigos ASCII.
    * **Problemas**:
        * **Dimensionalidade alta**: Para vocabulários grandes, cria um número excessivo de colunas, tornando o modelo ineficiente e com alto consumo de memória.
        * **Não captura significado**: Palavras com significados semelhantes não são representadas como "próximas" no espaço numérico, pois cada palavra é tratada como uma entidade isolada, sem correlação semântica com outras.

É evidente que métodos mais sofisticados são necessários para capturar a **semântica** das palavras e permitir que os modelos de IA entendam o significado subjacente da linguagem.

---
### 7. Embeddings de Texto

Os métodos tradicionais como ASCII e one-hot encoding são insuficientes para chatbots porque não conseguem capturar as complexas relações de significado entre as palavras. A solução para essa limitação são os **embeddings de texto**.

**Embeddings** são representações numéricas de palavras ou frases em um **espaço vetorial de tamanho fixo**. A premissa central é que palavras ou frases com significados semanticamente semelhantes estarão **próximas** umas das outras nesse espaço vetorial, enquanto aquelas com significados diferentes estarão mais distantes.

* **Dimensionalidade controlada**: Ao contrário do one-hot encoding, que resulta em vetores esparsos e de alta dimensionalidade, os embeddings permitem controlar o tamanho do vetor, geralmente variando de centenas a milhares de dimensões, mas com um número fixo e gerenciável.
* **Captura de semântica**: Modelos de embedding são treinados para que a **distância** entre os vetores de palavras reflita a similaridade de seus significados. Por exemplo, a distância vetorial entre "rei" e "rainha" pode ser similar à distância entre "homem" e "mulher", demonstrando relações análogas. Essa propriedade permite que o modelo compreenda nuances de significado e contexto.
* **Armazenamento eficiente**: Em vez de criar uma coluna separada para cada dimensão, os embeddings são geralmente armazenados em uma única coluna do DataFrame, contendo uma lista de todos os valores numéricos que compõem o vetor.
* **Modelos pré-treinados**: Podemos aproveitar modelos de embedding pré-treinados, como os oferecidos pela OpenAI. Esses modelos já aprenderam a mapear palavras e frases para suas representações semânticas a partir de vastos volumes de texto, economizando o tempo e o recurso de treinar um modelo de embedding do zero.

---
### 8. Criando um Índice de Embeddings para Nosso Chatbot

Com os dados devidamente estruturados e limpos, o próximo passo crucial é a criação de um **índice de embeddings**. Este índice é o mecanismo que permitirá ao chatbot localizar rapidamente os contextos mais relevantes para qualquer consulta do usuário.

O processo de construção do índice envolve as seguintes etapas:

1.  **Carregar os dados**: Reabrir o DataFrame que contém os dados limpos, assegurando que o índice seja carregado corretamente, por exemplo, usando `index_col=0` ao ler um arquivo CSV com Pandas.
2.  **Gerar Embeddings**:
    * Para cada item de texto no DataFrame, é feita uma chamada à API de embeddings da OpenAI.
    * A API retorna um **vetor numérico** (o embedding) para cada texto. É importante observar que o modelo `text-embedding-ada-002` da OpenAI gera embeddings de 1.536 dimensões.
    * Esses embeddings são então armazenados em uma nova coluna no DataFrame, geralmente nomeada `embedding`, onde cada entrada é uma lista de números.
    * É fundamental processar as respostas da API, extraindo apenas os valores do embedding e desconsiderando metadados adicionais. Uma **list comprehension** é uma técnica eficiente para processar a lista de respostas em lotes.
    * Para otimizar o processo e evitar problemas de limite de taxa (rate-limiting) ao lidar com grandes volumes de dados, as chamadas à API de embeddings são geralmente realizadas em **lotes (batches)** (por exemplo, 100 textos por requisição).
3.  **Construir o índice**: O DataFrame, agora enriquecido com a coluna de embeddings, serve como o próprio índice. Quando uma nova pergunta é feita, seu embedding será gerado e comparado com os embeddings armazenados neste índice para identificar os textos semanticamente mais semelhantes.

Ter os embeddings diretamente no DataFrame agiliza o processo de busca de similaridade, tornando o chatbot mais eficiente na recuperação de informações contextuais.

```python
import openai
import pandas as pd
import numpy as np # Importar numpy para array para manipulação eficiente de vetores

# Nome do modelo de embedding que será utilizado. Este é o modelo recomendado pela OpenAI.
EMBEDDING_MODEL_NAME = "text-embedding-ada-002"

# Função para obter embeddings para uma lista de textos
def get_embeddings_batch(texts, model_name):
    """
    Realiza uma chamada à API da OpenAI para obter embeddings para uma lista de textos.
    """
    response = openai.Embedding.create(
        input=texts,
        model=model_name
    )
    # Retorna apenas a lista de vetores de embedding
    return [embedding["embedding"] for embedding in response["data"]]

# Gerar embeddings para a coluna 'text' do DataFrame
# Recomenda-se processar em lotes para evitar exceder o limite de requisições da API
# e para gerenciar melhor o consumo de recursos.
batch_size = 100 # Número de textos processados por requisição à API
embeddings = []
for i in range(0, len(df), batch_size):
    # Seleciona um lote de textos do DataFrame
    batch_texts = df["text"].iloc[i : i + batch_size].tolist()
    # Obtém os embeddings para o lote de textos
    batch_embeddings = get_embeddings_batch(batch_texts, EMBEDDING_MODEL_NAME)
    # Adiciona os embeddings gerados à lista principal
    embeddings.extend(batch_embeddings)

# Adiciona a lista de embeddings como uma nova coluna no DataFrame
df["embedding"] = embeddings

# Opcional: Salvar o DataFrame com os embeddings para uso futuro,
# evitando a necessidade de gerá-los novamente.
df.to_csv("dados_com_embeddings.csv")

# Exibe as primeiras linhas do DataFrame, incluindo a nova coluna 'embedding'
print(df.head())
print(f"Shape do DataFrame com embeddings: {df.shape}")
```

---
### 9. Busca Semântica de Texto

Com os embeddings do nosso conjunto de dados devidamente criados, podemos agora implementar a **busca semântica de texto** para encontrar os dados mais relevantes para as consultas dos usuários.

A **busca semântica** difere fundamentalmente de uma **busca por palavra-chave**:

* **Busca por palavra-chave**: Opera por correspondência exata de termos. Por exemplo, uma busca por "reparo de torneira pingando" retornaria apenas documentos que contêm precisamente essas palavras. É uma busca literal e não considera o significado.
* **Busca semântica**: Compreende o **significado** e o **contexto** da consulta. Se o usuário perguntar "Como consertar um vazamento na pia?", uma busca semântica seria capaz de encontrar resultados sobre "reparo de torneira pingando", mesmo que as palavras exatas não estejam presentes, porque o significado subjacente é semelhante. Essa capacidade de inferir o sentido torna a busca muito mais poderosa e flexível.

A busca semântica é realizada através do cálculo da **similaridade** entre o embedding da pergunta do usuário e os embeddings de todos os textos presentes no nosso conjunto de dados. A métrica mais comum e eficaz para isso é a **similaridade de cosseno** (ou sua inversa, a **distância de cosseno**).

* **Similaridade de Cosseno**: Mede o cosseno do ângulo entre dois vetores no espaço vetorial.
    * Valores próximos de 1 indicam alta similaridade (ângulos pequenos entre os vetores), significando que os textos têm um significado muito parecido.
    * Valores próximos de -1 indicam baixa similaridade (ângulos grandes), sugerindo significados opostos.
    * Valores próximos de 0 indicam ortogonalidade, ou seja, que não há uma relação linear aparente entre os significados.
* **Distância de Cosseno**: É calculada como $1 - \text{Similaridade de Cosseno}$.
    * Um valor de **0** indica que os vetores são idênticos em direção (similaridade máxima).
    * Um valor de **1** indica que os vetores são ortogonais (sem relação).
    * Um valor de **2** indica que os vetores têm direções opostas (similaridade mínima).

Para a busca semântica em nosso chatbot, buscamos os textos com a **menor distância de cosseno** (ou, equivalentemente, a maior similaridade de cosseno) em relação à pergunta, pois esses são os que carregam o significado mais próximo da consulta.

---
### 10. Encontrando a Distância de Cosseno em Python

Para aplicar o conceito de distância de cosseno no nosso conjunto de dados personalizado e encontrar os textos mais relevantes, seguimos os seguintes passos em Python:

1.  **Gerar o embedding da pergunta**: A primeira ação é converter a pergunta formulada pelo usuário em um vetor de embedding. Isso é feito utilizando a mesma API de embeddings da OpenAI (`text-embedding-ada-002`) que foi empregada para gerar os embeddings do conjunto de dados. É crucial usar o mesmo modelo para garantir que os espaços vetoriais sejam compatíveis.
2.  **Calcular a distância de cosseno**: Uma vez que temos o embedding da pergunta, a função `distances_from_embeddings` (disponível na biblioteca `openai.embeddings_utils` ou implementações similares) é utilizada. Esta função calcula a distância de cosseno entre o embedding da pergunta e cada um dos embeddings presentes no nosso DataFrame.
    * Ela recebe o embedding da pergunta, a lista de embeddings do DataFrame (que deve ser convertida para um formato serializável, como uma lista de listas de números) e o `distance_metric` especificado como `"cosine"`.
    * O resultado dessa operação é uma **matriz de distância de cosseno**, onde cada valor representa a distância entre a pergunta e um texto específico do dataset.
3.  **Classificar por similaridade**: Os valores da matriz de distância são então usados para classificar os textos do nosso DataFrame. A ordenação é feita do mais similar para o menos similar à pergunta. Como uma **menor distância de cosseno indica maior similaridade**, o DataFrame é ordenado em ordem ascendente com base nesta coluna.
4.  **Selecionar os contextos mais relevantes**: Finalmente, para compor o prompt do modelo de linguagem, são selecionados os `n` textos com as menores distâncias de cosseno. Esses são os considerados os mais relevantes para a pergunta do usuário.

Este processo é fundamental para garantir que apenas as informações mais pertinentes do nosso conjunto de dados personalizado sejam utilizadas como contexto para o modelo de conclusão de texto da OpenAI, resultando em respostas mais precisas e personalizadas. Funções como `cosine_distance` da biblioteca `scipy.spatial.distance` ou `distances_from_embeddings` da `openai.embeddings_utils` são as ferramentas programáticas para realizar esses cálculos.

```python
import openai
import pandas as pd
from openai.embeddings_utils import distances_from_embeddings, get_embedding
import numpy as np # Importar numpy para array, útil para garantir o formato correto dos embeddings

# Definir o nome do modelo de embedding a ser utilizado (o mesmo usado para gerar os embeddings do DF)
EMBEDDING_MODEL_NAME = "text-embedding-ada-002"


def get_rows_sorted_by_relevance(question, df_with_embeddings):
    """
    Gera o embedding da pergunta do usuário, calcula a distância de cosseno
    entre a pergunta e todos os embeddings no DataFrame, e retorna o DataFrame
    ordenado pela relevância (menor distância = maior relevância).

    Args:
        question (str): A pergunta feita pelo usuário.
        df_with_embeddings (pd.DataFrame): O DataFrame contendo a coluna 'text'
                                           e a coluna 'embedding' (vetores numéricos).

    Returns:
        pd.DataFrame: O DataFrame original com uma nova coluna 'distances' e
                      ordenado pela relevância em relação à pergunta.
    """
    # 1. Gerar o embedding da pergunta do usuário
    question_embedding = get_embedding(question, EMBEDDING_MODEL_NAME)

    # 2. Calcular a distância de cosseno entre o embedding da pergunta e cada embedding no DataFrame.
    # df_with_embeddings["embedding"].tolist() garante que a função receba uma lista de listas de floats.
    df_with_embeddings["distances"] = distances_from_embeddings(
        question_embedding,
        df_with_embeddings["embedding"].tolist(),
        distance_metric="cosine" # Especifica a métrica de distância a ser usada
    )

    # 3. Classificar o DataFrame pela coluna 'distances' em ordem ascendente.
    # Menor distância significa maior similaridade, então queremos os menores valores primeiro.
    df_sorted = df_with_embeddings.sort_values("distances", ascending=True)

    return df_sorted

```

---
### 11. Busca de Texto Semântica em Python

Após o cálculo das distâncias de cosseno, a etapa seguinte é identificar e extrair as linhas do DataFrame que demonstram a menor distância em relação à pergunta do usuário. Essas linhas representam os textos com maior **relevância semântica** para a consulta.

A implementação em Python segue estes passos:

1.  **Combinar distâncias e dados**: Adiciona-se uma nova coluna ao DataFrame original, contendo os valores de distância de cosseno calculados para cada texto em relação à pergunta. Isso associa diretamente a métrica de similaridade ao seu respectivo conteúdo textual.
2.  **Ordenar o DataFrame**: O DataFrame é então ordenado com base nesta nova coluna de distâncias, em ordem **ascendente**. Essa ordenação garante que os textos mais relevantes (aqueles com a menor distância de cosseno) apareçam no topo da lista.
3.  **Selecionar os top-N resultados**: Para evitar o envio de informações excessivas e potencialmente irrelevantes ao modelo de linguagem, um número predefinido de resultados mais relevantes (por exemplo, os 5 ou 10 primeiros textos) é selecionado. Essa seleção dos "top-N" resulta em um contexto conciso e focado.

É importante ressaltar que, embora a distância de cosseno seja um excelente indicador de relevância semântica, ela não impõe uma ordem cronológica ou lógica perfeita. Por exemplo, a quinta linha mais relevante em termos de significado pode ser, cronologicamente, o primeiro evento mencionado no dataset. A distância de cosseno reflete a similaridade de significado, não a ordem temporal ou a exatidão factual isolada. No entanto, para o objetivo de fornecer um contexto rico e pertinente ao modelo de linguagem, essa relevância semântica é de suma importância.

A função `get_rows_sorted_by_relevance` encapsula essa lógica, realizando o embedding da pergunta, calculando as distâncias e retornando o DataFrame ordenado. O código para esta seção é a mesma função `get_rows_sorted_by_relevance` apresentada na seção 10, que já realiza todas essas etapas.

---
### 12. Compondo um Prompt de Texto

Com o contexto relevante devidamente identificado e extraído do nosso conjunto de dados personalizado, o próximo passo crucial é integrá-lo a um **prompt de texto** que será submetido ao modelo de conclusão de texto da OpenAI. A construção deste prompt é essencial para guiar o modelo a utilizar as informações fornecidas e a gerar uma resposta apropriada e contextualizada.

Um prompt de texto típico para um chatbot de Q&A baseado em contexto segue uma estrutura bem definida:

* **Instrução clara**: O prompt deve começar com uma instrução explícita e direta para o modelo, como "Responda à pergunta com base no contexto abaixo." Esta instrução define a tarefa do modelo.
* **Regra de falha**: É vital incluir uma instrução sobre o que o modelo deve fazer caso a pergunta não possa ser respondida utilizando apenas o contexto fornecido. Por exemplo, "Se a pergunta não puder ser respondida com base no contexto, diga 'Não sei'." Esta regra previne que o modelo "alucine" ou invente respostas quando a informação necessária não está disponível no contexto.
* **Seção de Contexto**: Uma seção claramente delimitada no prompt onde o texto relevante, obtido através da busca semântica no nosso conjunto de dados, é inserido. Esta é a "alimentação" do modelo com os dados específicos que ele deve considerar.
* **A Pergunta**: A pergunta original feita pelo usuário, que o modelo deve, então, responder utilizando o contexto que lhe foi fornecido.

A eficácia deste passo reside em como os embeddings, criados nas etapas anteriores, são utilizados para fornecer ao bot o contexto necessário. Essa abordagem permite que o modelo de linguagem gere respostas que são não apenas coerentes, mas também altamente precisas e personalizadas de acordo com os dados específicos que lhe foram apresentados.

---
### 13. Quantidade de Dados a Incluir no Contexto

Uma consideração crítica ao compor o prompt é determinar a **quantidade ideal de dados** a serem incluídos no contexto. Embora os dados recuperados estejam ordenados por relevância, a inclusão de "tudo" não é eficiente nem logisticamente viável.

A limitação primária da quantidade de dados é imposta pelo conceito de **tokens**:

* **Token**: Um token é a unidade básica de processamento de texto utilizada pelos modelos de **Processamento de Linguagem Natural (PLN)**. Um token pode ser uma palavra completa, uma parte de uma palavra ou até mesmo um caractere especial, dependendo do algoritmo de tokenização específico do modelo. Por exemplo, a palavra "cachorro" pode ser um token, ou "ca" e "chorro" podem ser tokens separados.
* **Limite de tokens do modelo**: Cada modelo de IA possui um limite máximo de tokens que pode processar em uma única requisição. Este limite é abrangente, incluindo tanto o **prompt de entrada** (que engloba as instruções, o contexto fornecido e a pergunta do usuário) quanto a **resposta esperada** que será gerada pelo modelo.

É absolutamente essencial compreender e respeitar o limite de tokens do modelo escolhido. Utilizar a maior quantidade de dados possível dentro desse limite permite que o modelo tenha mais informações para gerar uma resposta rica e detalhada. Contudo, exceder esse limite resultará em um erro da API ou no truncamento da entrada, o que pode comprometer a qualidade e a completude da resposta.

---
### 14. Usando Tokens na OpenAI

A OpenAI estabelece seus preços de uso dos modelos com base no consumo de **tokens**, e cada modelo possui um limite específico de tokens que pode processar por requisição. Por exemplo, o modelo `text-davinci-003` tinha um limite aproximado de 4.100 tokens, e o `gpt-3.5-turbo-instruct` tem um limite de 4.096 tokens. Este limite é de suma importância, pois engloba tanto o **prompt customizado** (que inclui as instruções, a pergunta e o contexto relevante extraído do nosso dataset) quanto a **resposta gerada pelo modelo**.

Para gerenciar o uso de tokens de forma eficiente e maximizar a quantidade de contexto que pode ser fornecida ao modelo sem exceder os limites, a OpenAI disponibiliza uma biblioteca Python especializada, o **Tiktoken**.

* **Tiktoken**: Esta biblioteca permite calcular com precisão o número de tokens em uma determinada string de texto para um modelo específico. É uma ferramenta indispensável para garantir que o prompt completo (instruções + contexto + pergunta) não ultrapasse o limite máximo de tokens do modelo, evitando erros e truncamentos.
* **Codificação**: A função `tiktoken.encoding_for_model()` é utilizada para obter o objeto de codificação correto, que mapeia texto para tokens numéricos para o modelo desejado (por exemplo, `text-davinci-003` ou `gpt-3.5-turbo-instruct`).
* **Contagem de tokens**: Uma vez obtido o objeto de codificação, o método `encode()` é aplicado à string de entrada. Ele retorna uma lista de IDs de tokens. O número total de tokens é simplesmente o comprimento dessa lista.

Ao empregar o `tiktoken`, é possível iterar sobre os resultados da busca semântica, adicionando incrementalmente contexto ao prompt até que o limite de tokens seja atingido. Essa abordagem garante que o modelo receba o máximo de informações relevantes possível, otimizando a qualidade e a completude da resposta gerada.

```python
import tiktoken

# Define o nome do modelo de Completion que será usado.
# É importante que este nome corresponda ao modelo real para a contagem correta de tokens.
COMPLETION_MODEL_NAME = "gpt-3.5-turbo-instruct"

# Obtém o codificador (encoder) específico para o modelo de Completion.
# Este encoder sabe como o modelo divide o texto em tokens.
encoding = tiktoken.encoding_for_model(COMPLETION_MODEL_NAME)

# Exemplo simples de contagem de tokens para uma string.
text_to_encode = "Olá, como posso ajudar hoje?"
tokens = encoding.encode(text_to_encode) # Converte a string em uma lista de IDs de token.
num_tokens = len(tokens) # O número de tokens é o tamanho dessa lista.

print(f"O texto '{text_to_encode}' tem {num_tokens} tokens.")

# Exemplo de contagem de tokens para uma string que simula um prompt completo.
prompt_example = (
    "Responda à pergunta com base no contexto abaixo.\n\n"
    "Contexto: A capital da França é Paris.\n\n"
    "Pergunta: Qual a capital da França?"
)
num_tokens_prompt = len(encoding.encode(prompt_example))
print(f"O prompt de exemplo tem {num_tokens_prompt} tokens.")
```

---
### 15. Compondo um Prompt de Texto com Contagem Máxima de Tokens

Para construir um prompt de texto que otimize o aproveitamento do limite de tokens de um modelo OpenAI, é fundamental integrar a lógica de seleção de contexto baseada em similaridade com a contagem de tokens fornecida pela biblioteca `tiktoken`.

O processo envolve os seguintes passos:

1.  **Definir um template de prompt**: Começa-se com uma string de template que contém as instruções fixas para o modelo. Estas instruções devem guiar o comportamento desejado, como "Responda à pergunta com base no contexto abaixo." e uma regra de falha clara, por exemplo, "Se a pergunta não puder ser respondida com base no contexto, diga 'Não sei'."
2.  **Iterar sobre os contextos relevantes**: Em seguida, o processo percorre os resultados da busca semântica, que já estão ordenados por relevância (ou seja, aqueles com a menor distância de cosseno à pergunta do usuário).
3.  **Adicionar contexto incrementalmente**: Para cada fragmento de texto relevante (`text`) obtido da busca:
    * O texto é temporariamente adicionado ao prompt.
    * O número de tokens do prompt atualizado é calculado usando `tiktoken`.
    * Verifica-se se o número total de tokens (prompt atual + tokens esperados para a resposta) excede o limite máximo do modelo. Se o limite for excedido, a adição de mais contexto é interrompida (`break`), garantindo que o modelo tenha espaço suficiente para gerar uma resposta.
4.  **Formatação do contexto**: Para que o modelo interprete o contexto de forma clara e limpa, os fragmentos de texto devem ser concatenados de maneira apropriada. Em vez de simplesmente unir uma lista de strings (o que resultaria em chaves, aspas e vírgulas desnecessárias), é preferível utilizar o método `join()` do Python para criar uma única string. Um separador como uma quebra de linha (`\n`) ou um delimitador mais robusto como `\n\n###\n\n` torna o prompt mais legível e estruturado para o modelo.
5.  **Finalizar o prompt**: A pergunta original do usuário é adicionada ao final do prompt, garantindo que o modelo saiba exatamente qual questão ele deve responder utilizando o contexto fornecido.

Essa abordagem permite a criação de um prompt dinâmico que inclui a quantidade máxima de contexto relevante sem exceder os limites do modelo, otimizando significativamente a qualidade e a precisão da resposta gerada. A função `create_prompt` exemplifica essa lógica, combinando a contagem de tokens com a inclusão estratégica de contexto.

```python
import tiktoken
import pandas as pd
import numpy as np # Necessário para arrays, se os embeddings no DF forem np.array

# (Assumindo que df já foi carregado e tem a coluna 'embedding' com os vetores numéricos)
# (Assumindo que a função get_rows_sorted_by_relevance do Passo 10/11 está definida)

# Nome do modelo de Completion (para contagem de tokens)
COMPLETION_MODEL_NAME = "gpt-3.5-turbo-instruct"
# Encoder para contagem de tokens
encoding = tiktoken.encoding_for_model(COMPLETION_MODEL_NAME)

def create_prompt(question, df_with_embeddings, max_prompt_tokens):
    """
    Cria um prompt otimizado para o modelo de Completion, incluindo contexto relevante
    limitado pelo número máximo de tokens.

    Args:
        question (str): A pergunta feita pelo usuário.
        df_with_embeddings (pd.DataFrame): O DataFrame com os textos e seus embeddings.
        max_prompt_tokens (int): O número máximo de tokens que o prompt pode ter.

    Returns:
        str: O prompt final formatado com instruções, contexto e a pergunta.
    """
    # 1. Template base do prompt com instruções fixas
    prompt_template = (
        "Responda à pergunta com base no contexto abaixo. "
        "Se a pergunta não puder ser respondida com base no contexto, diga 'Não sei'.\n\n"
        "Contexto:\n"
    )

    # 2. Obter os resultados mais relevantes do DataFrame, já ordenados por similaridade
    # Usamos .copy() para não modificar o DataFrame original ao adicionar a coluna 'distances'
    df_relevant_sorted = get_rows_sorted_by_relevance(question, df_with_embeddings.copy())

    context_text_chunks = []
    # Calcula os tokens iniciais do template e da pergunta (partes que sempre estarão no prompt)
    current_tokens = len(encoding.encode(prompt_template + question))

    # 3. Iterar sobre os chunks de texto mais relevantes e adicioná-los ao contexto
    for i, row in df_relevant_sorted.iterrows():
        text_chunk = row["text"]
        
        # Estima os tokens que este chunk de texto adicionaria ao prompt,
        # incluindo um separador para melhorar a legibilidade para o modelo.
        chunk_tokens_with_separator = len(encoding.encode(text_chunk + "\n\n###\n\n"))

        # Verifica se adicionar este chunk excederia o limite máximo de tokens do prompt
        if current_tokens + chunk_tokens_with_separator > max_prompt_tokens:
            break # Se exceder, para de adicionar contexto
        
        context_text_chunks.append(text_chunk)
        current_tokens += chunk_tokens_with_separator

    # 4. Juntar os chunks de contexto selecionados em uma única string
    # Usar "\n\n###\n\n" como separador ajuda o modelo a diferenciar os blocos de contexto.
    final_context_string = "\n\n###\n\n".join(context_text_chunks)

    # 5. Compor o prompt final: template + contexto + pergunta
    full_prompt = f"{prompt_template}{final_context_string}\n\nPergunta: {question}"
    
    return full_prompt

```

---
### 16. Consultando um Modelo de Conclusão

O estágio final na construção do chatbot envolve o envio do **prompt customizado** ao modelo de conclusão de texto da OpenAI e a recuperação da resposta gerada. Esta etapa é relativamente direta, uma vez que a maior parte do trabalho complexo – incluindo coleta de dados, limpeza, geração de embeddings e composição do prompt – já foi concluída.

Para interagir com o modelo, utiliza-se a API da OpenAI da seguinte forma:

1.  **Importar a biblioteca OpenAI**: Certificar-se de que a biblioteca `openai` está importada no ambiente de desenvolvimento.
2.  **Configurar a chave da API**: A chave de autenticação da OpenAI deve ser definida, geralmente através de `openai.api_key`. Esta chave valida as requisições à API.
3.  **Chamar o método `Completion.create()`**: Este é o método principal para interagir com os modelos de conclusão. Os argumentos essenciais incluem:
    * `model`: Especifica qual modelo de linguagem será utilizado (por exemplo, `gpt-3.5-turbo-instruct`). A escolha do modelo impacta o desempenho e o custo.
    * `prompt`: A string do prompt customizado que foi cuidadosamente construído, contendo as instruções, o contexto relevante e a pergunta do usuário.
    * `temperature`: Um parâmetro de 0 a 1 que controla a "criatividade" ou aleatoriedade da resposta. Valores mais baixos (próximos de 0.0, como 0.0 ou 0.2) produzem respostas mais determinísticas, factuais e consistentes, o que é geralmente preferível para um chatbot de Q&A factual. Valores mais altos resultam em respostas mais diversas e "criativas", mas potencialmente menos precisas.
    * `max_tokens`: O número máximo de tokens que a resposta gerada pode conter. É crucial definir este valor considerando o limite total de tokens do modelo e os tokens já utilizados pelo prompt para evitar truncamentos.
    * Outros parâmetros como `top_p`, `frequency_penalty`, e `presence_penalty` podem ser ajustados para refinar ainda mais o comportamento do modelo, influenciando a diversidade e a originalidade das palavras escolhidas na resposta.
4.  **Extrair a resposta**: A resposta da API é um objeto JSON. O texto principal da resposta pode ser acessado tipicamente através de `response.choices[0].text`. Além disso, metadados como o uso de tokens podem ser acessados via `response["usage"]`.

É importante notar que os modelos da OpenAI são **estocásticos**, o que significa que podem não retornar a mesma resposta para o mesmo prompt, mesmo com os mesmos parâmetros de inferência. Portanto, para análises e ajustes, é mais eficiente manipular uma resposta já obtida do que fazer novas chamadas desnecessárias à API. Além disso, as chamadas a `create()` consomem tokens da sua conta OpenAI, exigindo um gerenciamento cuidadoso do uso.

Com a execução deste processo, o chatbot personalizado será capaz de receber uma pergunta, buscar o contexto mais relevante em seu conjunto de dados, formatar um prompt inteligente e, por fim, obter uma resposta precisa e informada do modelo de linguagem, demonstrando a eficácia da abordagem de Geração Aumentada por Recuperação (RAG - Retrieval Augmented Generation).

```python
import openai
import pandas as pd
import numpy as np # Para lidar com arrays numéricos dos embeddings
import tiktoken # Para contagem de tokens

# (Assumindo que o DataFrame 'df' com a coluna 'embedding' já foi carregado e preparado)
# (Assumindo que as funções get_rows_sorted_by_relevance e create_prompt estão definidas)

# Define o nome do modelo de Completion que será consultado
COMPLETION_MODEL_NAME = "gpt-3.5-turbo-instruct"

def answer_question(question, df_with_embeddings, max_prompt_tokens=1800, max_answer_tokens=150):
    """
    Função principal para responder a uma pergunta usando o fluxo de Geração Aumentada por Recuperação (RAG).

    Args:
        question (str): A pergunta feita pelo usuário.
        df_with_embeddings (pd.DataFrame): O DataFrame contendo os textos e seus embeddings.
        max_prompt_tokens (int): O número máximo de tokens para o prompt de entrada do modelo.
        max_answer_tokens (int): O número máximo de tokens que a resposta gerada pode ter.

    Returns:
        str: A resposta gerada pelo modelo da OpenAI, ou uma string vazia em caso de erro.
    """
    # 1. Cria o prompt customizado, incluindo o contexto relevante, limitado por tokens
    prompt = create_prompt(question, df_with_embeddings, max_prompt_tokens)

    try:
        # 2. Chama a API de Completion da OpenAI
        response = openai.Completion.create(
            model=COMPLETION_MODEL_NAME, # O modelo de linguagem a ser usado
            prompt=prompt,               # O prompt que contém a pergunta e o contexto
            temperature=0.0,             # Controla a aleatoriedade da resposta (0.0 = mais determinística)
            max_tokens=max_answer_tokens # Limite de tokens para a resposta gerada
        )
        # 3. Extrai o texto da resposta gerada pelo modelo
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(f"Ocorreu um erro ao chamar a API da OpenAI: {e}")
        return "Desculpe, não consegui gerar uma resposta no momento."

```