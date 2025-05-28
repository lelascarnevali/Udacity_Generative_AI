### 1. Introdução a Datasets para Modelos de Linguagem Grande (LLMs)

Modelos de Linguagem Grande (LLMs) podem ser treinados para diversas tarefas, como geração de resumos de livros ou resposta a perguntas sobre vulnerabilidades de cibersegurança. Para **ajustar (fine-tune)** um LLM a uma tarefa específica, é essencial ter um dataset apropriado. Muitos LLMs atuais são proficientes em **resposta a perguntas zero-shot**, o que significa que podem responder a perguntas para as quais não foram explicitamente treinados, exibindo propriedades emergentes. Essa capacidade é particularmente útil em domínios abertos, onde as respostas podem ser inferidas a partir de datasets comuns como a Wikipédia, mesmo sem dados explícitos para a pergunta exata.

---
### 2. Coleta de Dados da Internet

Idealmente, os dados para treinar modelos viriam de fontes internas, bem formatadas e fáceis de usar. No entanto, na prática, essas fontes são raras. Geralmente, lida-se com dados externos mal formatados ou incompletos, que precisam ser complementados ou usados diretamente. Após a coleta, o objetivo é produzir um dataset bem formatado.

Existem duas abordagens principais para coletar dados da internet:

* **APIs (Application Programming Interfaces)**: São interfaces projetadas para acesso programático a dados hospedados. Geralmente, é necessário registrar-se e obter uma chave de API. As requisições a APIs costumam retornar dados estruturados, como documentos JSON ou XML. APIs são excelentes para coleta de dados e são frequentemente integradas a sistemas maiores, com suporte para coleta.

* **Web Scraping**: É o processo de extrair dados de websites diretamente, sem o uso de APIs. Embora legal em muitos casos (com raras exceções), o scraping nem sempre é bem-vindo. É crucial verificar a licença de quaisquer dados coletados e, em caso de dúvida, consultar um advogado, especialmente para dados de código com licenciamento complexo.

    Para o scraping básico, pode-se usar as bibliotecas Python `requests` e `BeautifulSoup`.

    O **`requests`** é usado para enviar requisições HTTP, como requisições GET para obter o conteúdo de uma página web. Um `status_code` entre 200-299 indica sucesso, enquanto 400-599 indica erros (ex: 404 para página não encontrada, 403 para acesso proibido).

    ```python
    # Fazendo uma requisição GET
    response = requests.get('https://www.example.com')

    # Imprime o código de status
    print(response.status_code)

    # Imprime o conteúdo da resposta
    print(response.text)
    ```

    **`BeautifulSoup`** é um parser HTML em Python, ideal para navegar e extrair informações de documentos HTML, mesmo aqueles "malcheirosos" ou "sopa de tags" (HTML não estruturado). Ele permite encontrar tags específicas usando métodos como `.find()` (retorna a primeira ocorrência) e `.find_all()` (retorna todas as ocorrências), e extrair o texto com `.text`.

    ```python
    from bs4 import BeautifulSoup
    import requests

    # Exemplo: Fazendo uma requisição GET e parseando com BeautifulSoup
    response = requests.get('https://www.udacity.com/')
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontra a primeira tag <h1> na página
    h1_tag = soup.find('h1')

    # Imprime o texto da primeira tag <h1>
    print(h1_tag.text)
    ```

    **HTML (Hypertext Markup Language)** é a linguagem para criar documentos web. É uma coleção de tags, como `<div>` (para agrupar conteúdo), `<h1>` a `<h4>` (cabeçalhos), `<img>` (imagens), `<p>` (parágrafos), `<span>` (agrupamento de texto para estilo) e `<a>` (links). HTML permite uma estrutura hierárquica para o conteúdo.

    **JSON (JavaScript Object Notation)** é um formato para comunicação de informações, ideal para dados complexos, e **XML (Extensible Markup Language)** é uma alternativa popular ao JSON para comunicação de dados. Diferente do HTML, JSON e XML não são usados para compor a estrutura de um site, mas permitem aninhar elementos e informações entre tags.

    Para cenários mais avançados de scraping, onde `requests` e `BeautifulSoup` são insuficientes (devido a `robots.txt`, anti-scraping, anti-DDoS ou conteúdo dinâmico), pode-se recorrer a bibliotecas como `Scrapy` e `Selenium`.

    **Selenium** é uma estrutura de automação de navegador que simula a navegação de um usuário real. Isso é útil porque o site vê um navegador "normal" originando a requisição, tornando-a menos provável de ser bloqueada. Frequentemente, usa-se um navegador "headless" (sem interface gráfica) para economizar recursos.

    ```python
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")

    # É necessário especificar o caminho para o chromedriver no seu sistema
     driver = webdriver.Chrome(options=options, executable_path='/path/to/chromedriver')
     driver.get("https://www.udacity.com/")

     page_source = driver.page_source
     with open("udacity_home.html", "w") as f:
         f.write(page_source)

     driver.quit()
    ```
    No código acima, `options.headless = True` é fundamental para evitar a abertura de uma janela do navegador, o que é crucial ao raspar muitas páginas ou em sistemas com recursos limitados. `options.add_argument()` pode ser usado para passar argumentos adicionais, como o tamanho da janela, para tornar o sistema mais "real". Após a requisição GET bem-sucedida, o conteúdo da página está em `driver.page_source`. É uma boa prática executar `driver.quit()` para evitar problemas de escopo e liberar recursos.

---
### 3. Avaliação da Qualidade dos Dados

Enquanto cientistas de dados e engenheiros de Machine Learning lidam principalmente com dados tabulares (como em planilhas), onde a qualidade dos dados se refere a valores ausentes, campos inconsistentes e tratamento de valores categóricos, os Grandes Modelos de Linguagem (LLMs) são diferentes. Eles trabalham com entradas e saídas não numéricas, focando em duas propriedades principais para a modelagem de linguagem:

* O texto deve ser **sintática e semanticamente normal** para a tarefa.
* A fonte dos dados deve ser **confiável**.

A qualidade dos dados é crucial. Dados ruins levam a modelos ruins ("garbage in, garbage out"). É mais fácil lidar com problemas de dados como erros de digitação, espaços indesejados e caracteres ausentes em arquivos de origem do que em objetos `Dataset` processados. Para tarefas de LLM, é mais importante ter dados limpos do que grandes volumes de dados.

---
### 4. Limpeza de Dados

A limpeza de dados é um passo essencial após a coleta, especialmente quando se lida com dados raspados da web. Embora seja fácil coletar HTML de uma página, o desafio é o que fazer com ele depois. O conteúdo HTML bruto geralmente não é legível e contém muitas tags e scripts irrelevantes.

Um exemplo prático de limpeza de dados envolve extrair informações específicas, como biografias de pessoas, de um documento HTML. Para isso, é necessário identificar as tags HTML que contêm a informação desejada (por exemplo, uma tag `<p>` dentro de uma `<div>` com uma classe específica).

As etapas comuns na limpeza de dados textuais incluem:

* **Remoção de Tags HTML**: Eliminar tags HTML que não contribuem para o conteúdo textual significativo.
* **Tratamento de Pontuação e Caracteres Especiais**: Remover ou normalizar pontuações e outros caracteres que podem interferir na análise.
* **Conversão para Minúsculas**: Padronizar o texto para minúsculas para evitar que o mesmo termo seja tratado como diferente (ex: "Palavra" e "palavra").
* **Remoção de Stop Words**: Remover palavras comuns que não adicionam muito significado (ex: "e", "o", "de").
* **Lematização ou Stemming**: Reduzir as palavras à sua forma base (lema ou radical) para que variações da mesma palavra sejam tratadas como uma só.
* **Tratamento de Espaços em Branco**: Remover espaços extras ou inconsistentes.
* **Normalização de Acentos e Diacríticos**: Converter caracteres acentuados para suas versões sem acento.

Ferramentas como a biblioteca `BeautifulSoup` podem ser usadas para extrair o texto limpo das tags HTML.

```python
import re
from bs4 import BeautifulSoup

def clean_html(html_content):
    """Remove HTML tags from a string."""
    soup = BeautifulSoup(html_content, 'html.parser')
    clean_text = soup.get_text()
    return clean_text

def remove_punctuation(text):
    """Remove punctuation from a string."""
    return re.sub(r'[^\w\s]', '', text)

def to_lowercase(text):
    """Convert text to lowercase."""
    return text.lower()

# Exemplo de uso:
html_doc = """
<html>
<body>
    <div class="bio-container">
        <p>This is a <b>sample</b> bio with <i>some</i> text and <a href="#">a link</a>.</p>
        <script>alert('hello');</script>
        <span>Another part of the bio.</span>
    </div>
</body>
</html>
"""

# Supondo que 'html_doc' é o conteúdo HTML obtido
cleaned_text = clean_html(html_doc)
no_punctuation_text = remove_punctuation(cleaned_text)
final_text = to_lowercase(no_punctuation_text)

print(f"Texto original HTML: {html_doc[:100]}...")
print(f"Texto limpo: {cleaned_text}")
print(f"Texto sem pontuação: {no_punctuation_text}")
print(f"Texto final (minúsculas): {final_text}")
```
A limpeza de dados é um processo iterativo e depende muito do contexto e da finalidade do dataset.

---
### 5. Tarefas de Modelagem de Linguagem

Modelos de Linguagem Grande (LLMs) são baseados na **arquitetura Transformer**, introduzida em 2017 por Vaswani et al. do Google Brain. O avanço principal dos Transformers é o uso do **mecanismo de atenção** para realizar tarefas de processamento de linguagem natural (PLN). Modelos como BERT (Bidirectional Encoder Representations from Transformers) e a família GPT (Generative Pre-trained Transformer) são exemplos proeminentes de Transformers. Esses LLMs são frequentemente chamados de **modelos de fundação** pela Universidade de Stanford, pois servem como base para modelos que são ajustados para tarefas específicas.

Dentro da modelagem de linguagem, existem várias tarefas de interesse:

* **Geração de Texto**: Como chatbots, tradução, sumarização, parafraseando e preenchimento de palavras faltantes.
* **Classificação de Texto**: Prever uma categoria ou categoria para o texto (ex: sentimento, spam, detecção de toxicidade).
* **Resposta a Perguntas**: Responder a perguntas diretas com trechos de um documento.
* **Modelagem de Linguagem Causal (CLM)**: Prever a próxima palavra em uma sequência, o que é fundamental para a geração de texto em tempo real.
* **Modelagem de Linguagem Mascarada (MLM)**: Preencher palavras ausentes ou mascaradas no texto, usada por modelos como BERT.
* **Clustering (Agrupamento)**: Agrupar textos semanticamente semelhantes, onde modelos BERT são preferíveis por mapear entradas de comprimento arbitrário para um embedding de comprimento fixo, permitindo o cálculo de similaridade.
* **Modelos Seq-to-Seq (Sequence-to-Sequence)**: Modelos como T5, que contêm tanto encoder quanto decoder, são ideais para tarefas de tradução.

---
### 6. Estruturação e Armazenamento de Dados Brutos

Ao trabalhar com dados textuais, há a liberdade e a responsabilidade de armazenar dados de texto brutos. Embora seja possível colocar esses dados diretamente em um objeto `Dataset` (como o do pacote `datasets`), há desvantagens:

* A escolha de um objeto de uma biblioteca específica pode dificultar a migração para outra biblioteca no futuro.
* Se houver pré-processamento ou **chunking** (divisão do texto em partes) no objeto `Dataset`, pode ser impossível reconstruir o contexto completo, o que é relevante se quiser treinar um modelo diferente com um comprimento de contexto diferente no futuro.
* A presença de toxicidade nos dados é mais difícil de gerenciar contexto por contexto em um objeto `Dataset` do que editar o arquivo fonte original e reconstruir o dataset.

Portanto, é recomendável armazenar os dados brutos e gerar o `Dataset` a partir deles.

#### Revisão: Salvando um Dataset

Para trabalhar com modelos pré-treinados do HuggingFace `transformers`, é desejável ter um objeto `Dataset` da biblioteca `datasets`. O método de salvamento depende se o objetivo é salvar no disco local ou no HuggingFace Hub.

Para criar um `Dataset` a partir de um dicionário Python, salvá-lo e carregá-lo do disco, pode-se usar o seguinte código:

```python
from datasets import Dataset, load_from_disk

# Criar um dicionário
data_dict = {"courses": ["Deep Learning", "Datasets for LLMs"], "type": ["Nanodegree", "Standalone"]}

# Criar um objeto Dataset a partir do dicionário
ds = Dataset.from_dict(data_dict)

# Salvar o objeto Dataset no disco local
ds.save_to_disk("my_dataset.hf")
print("Dataset saved!")

# Carregar o objeto Dataset do disco local
ds = load_from_disk("my_dataset.hf")
print("Dataset loaded!")
```

Para fazer upload para o HuggingFace Hub, siga as instruções específicas do HuggingFace. Ao usar um dataset do hub, utilize `load_dataset` em vez de `load_from_disk`.

---
### 7. Construindo Datasets para Modelagem de Linguagem Causal

A construção de um dataset para **modelagem de linguagem causal (CLM)** e o **ajuste fino (fine-tuning)** de um modelo GPT-2 nesse dataset é um processo comum.

Para começar, é necessário importar as bibliotecas relevantes, como `datasets` e `transformers`. Os dados de entrada são tipicamente arquivos de texto. Embora para demonstrações se usem poucos arquivos, na prática, datasets maiores são necessários.

As etapas para construir o dataset incluem:

* **Carregar Nomes de Arquivos**: Carregar os nomes dos arquivos de texto em uma lista.

    ```python
    # Exemplo de carregamento de nomes de arquivos
    # Supondo que os arquivos de texto estão em um diretório 'data/'
     from pathlib import Path
     filenames = list(Path('data/').glob('*.txt'))
    ```

* **Carregar Dados dos Arquivos**: Ler o conteúdo de cada arquivo e armazená-lo em uma lista ou estrutura de dados apropriada.

    ```python
    # Exemplo de carregamento de dados
     file_data = []
     for filename in filenames:
         with open(filename, 'r', encoding='utf-8') as f:
             file_data.append(f.read())
    ```

* **Criar Dataset**: Usar a lista de dados para criar um objeto `Dataset`.

    ```python
    from datasets import Dataset

    # Supondo que 'file_data' contém o texto de todos os arquivos
     dataset = Dataset.from_dict({'text': file_data})
     print(dataset)
    ```

* **Tokenização**: Tokenizar o texto do dataset usando um tokenizer apropriado para o modelo (ex: GPT-2 tokenizer). Este passo é crucial para converter o texto em um formato que o modelo pode processar. A tokenização pode incluir a divisão do texto em pedaços menores (chunks) de tamanho fixo.

    ```python
    from transformers import AutoTokenizer

     tokenizer = AutoTokenizer.from_pretrained("gpt2")
     def tokenize_function(examples):
         return tokenizer(examples["text"], truncation=True, max_length=512) # Ajuste max_length conforme necessário

     tokenized_dataset = dataset.map(tokenize_function, batched=True, num_proc=4, remove_columns=["text"])
    ```

* **Ajuste Fino (Fine-tuning)**: O dataset tokenizado pode então ser usado para ajustar um modelo como o GPT-2. A biblioteca `transformers` oferece a classe `Trainer` para facilitar esse processo.

    ```python
    from transformers import AutoModelForCausalLM, TrainingArguments, Trainer

     model = AutoModelForCausalLM.from_pretrained("gpt2")
     training_args = TrainingArguments(
         output_dir="./gpt2-finetuned",
         per_device_train_batch_size=8,
         num_train_epochs=3,
         save_steps=10_000,
         save_total_limit=2,
     )

     trainer = Trainer(
         model=model,
         args=training_args,
         train_dataset=tokenized_dataset,
         data_collator=None, # Pode ser necessário um DataCollatorForLanguageModeling
     )

     trainer.train()
    ```