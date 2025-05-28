# Construindo Datasets Personalizados para LLMs

Este documento serve como um material de estudo abrangente, expandindo o conteúdo das transcrições do curso sobre a criação de datasets personalizados para Modelos de Linguagem Grandes (LLMs). O objetivo é consolidar o aprendizado, aprofundar conceitos e fornecer uma referência completa para consulta futura.

---

## 1. Apresentação do Curso

* **Foco Principal**: O curso é dedicado à arte e ciência da construção de datasets personalizados, um componente vital para o desenvolvimento e otimização de Modelos de Linguagem Grandes (LLMs).
* **A Importância do Fine-Tuning**: Embora os LLMs pré-treinados disponíveis publicamente demonstrem capacidades impressionantes em uma vasta gama de tarefas, o processo de **fine-tuning** (ajuste fino) utilizando datasets customizados é frequentemente indispensável. Este ajuste permite que os modelos sejam especializados e alcancem um desempenho superior em tarefas específicas e contextos de nicho.
    * **Conceito Chave: Pré-treinamento vs. Fine-tuning**:
        * **Pré-treinamento**: É a fase inicial onde um LLM é treinado em uma quantidade massiva de dados textuais não rotulados (ex: toda a Wikipédia, grandes coleções de livros, código da web). O objetivo é que o modelo aprenda padrões gerais da linguagem, gramática, semântica e uma vasta gama de conhecimentos.
        * **Fine-tuning**: Após o pré-treinamento, o modelo (agora chamado de modelo de fundação) pode ser adaptado para tarefas específicas (ex: responder perguntas sobre um domínio médico, gerar código em uma linguagem particular, classificar o sentimento de avaliações de produtos). Isso é feito treinando-o adicionalmente em um dataset menor e específico para a tarefa, que geralmente contém exemplos rotulados.
* **Objetivos de Aprendizagem do Curso**: Capacitar os participantes com as habilidades práticas e o conhecimento teórico necessários para:
    * Implementar técnicas eficazes de coleta de dados.
    * Estruturar e consultar esses datasets de forma eficiente.
    * Refinar o desempenho dos LLMs, alinhando-os com os objetivos distintos de cada projeto ou aplicação.

---

## 2. Fundamentos sobre Datasets para LLMs

* **A Necessidade Inerente de Datasets**: Para treinar um LLM do zero ou, mais comumente, para realizar o fine-tuning de um modelo pré-treinado para uma nova tarefa (como gerar resumos de obras literárias ou responder a questões técnicas sobre vulnerabilidades de cibersegurança), a disponibilidade de um dataset relevante e de alta qualidade é um pré-requisito fundamental.
* **Capacidade de Aprendizado "Zero-Shot"**: Muitos LLMs contemporâneos exibem uma notável capacidade de "zero-shot question-answering". Isso significa que são capazes de responder a perguntas ou executar tarefas para as quais não foram explicitamente treinados com exemplos diretos. O modelo não teve "nenhuma tentativa" (zero shots) de ver um exemplo daquela pergunta específica durante seu treinamento formal.
    * **Exemplo**: LLMs podem realizar aritmética simples mesmo sem terem sido treinados especificamente com um corpus de problemas matemáticos.
    * **Conceitos Relacionados**:
        * **Few-Shot Learning**: O modelo recebe um pequeno número de exemplos da tarefa durante a inferência (no prompt) para "aprender" a tarefa em tempo real, sem atualização de pesos.
        * **One-Shot Learning**: Um caso específico de few-shot learning, onde apenas um exemplo é fornecido.
* **Propriedades Emergentes dos LLMs**: As capacidades de "zero-shot" e outras habilidades complexas que surgem em LLMs (especialmente os de grande escala) são frequentemente descritas como "propriedades emergentes". Elas não são explicitamente programadas, mas emergem como resultado da vasta quantidade de dados de treinamento, do grande número de parâmetros do modelo e da complexidade de sua arquitetura.
* **Desafios em Domínios Especializados**:
    * **Domínios Abertos (Gerais)**: Para perguntas de natureza geral, a capacidade "zero-shot" pode ser suficiente, pois os dados de treinamento massivos (como Wikipedia, Common Crawl, GitHub) provavelmente contêm informações contextualmente relevantes, mesmo que não diretamente ligadas à pergunta específica. Para muitos usuários e tarefas, isso é adequado.
    * **Domínios Especializados (de Nicho)**: Em campos como direito, cibersegurança, medicina ou engenharia específica, a performance "zero-shot" pode ser inadequada. Esses domínios utilizam jargões, nuances e um corpo de conhecimento específico que pode não estar bem representado nos datasets de pré-treinamento gerais. Portanto, para alcançar precisão e confiabilidade, é crucial treinar (ou fazer fine-tuning) o modelo com dados especializados daquele domínio.

---

## 3. Estrutura Geral do Aprendizado sobre Datasets

* O curso abordará de forma sequential e integrada os seguintes tópicos cruciais:
    1.  **Coleta Estratégica de Dados**: Métodos e melhores práticas para coletar dados relevantes para a tarefa alvo do LLM, com um foco particular na obtenção de dados da vastidão da internet.
    2.  **Avaliação Criteriosa e Limpeza de Dados**: Técnicas para avaliar a qualidade dos dados coletados e processos de limpeza para prepará-los para o treinamento. Este passo é vital, pois a qualidade do modelo final é diretamente influenciada pela qualidade dos dados de entrada, um princípio conhecido como "garbage in, garbage out" (lixo entra, lixo sai). Dados ruidosos, irrelevantes ou enviesados podem levar a um modelo com baixo desempenho, respostas incorretas ou comportamento indesejado.
    3.  **Impacto das Tarefas de Modelagem no Dataset**: Uma exploração das diversas tarefas que os LLMs podem executar e como a natureza de cada tarefa (ex: classificação, geração, tradução) influencia o design, a estrutura e o conteúdo do dataset necessário.
    4.  **Construção Prática de Datasets**: Orientações e demonstrações sobre como efetivamente construir um dataset que seja utilizável e otimizado para o treinamento ou fine-tuning de modelos de linguagem.

---

## 4. Coletando Dados da Internet: Fundamentos e Estratégias Iniciais

* **Realidade da Disponibilidade de Dados**: Embora o cenário ideal envolva fontes de dados internas, perfeitamente estruturadas e prontas para uso, a realidade da maioria dos projetos é que tais fontes são escassas. Frequentemente, os dados disponíveis internamente são mal formatados, carecem de contexto ou informações cruciais, ou simplesmente não existem em volume suficiente. Isso torna imperativo o uso de dados externos, seja para suplementar os internos ou como a fonte primária. O objetivo final, independentemente da origem, é produzir um dataset bem formatado e de alta qualidade.
* **Passos Essenciais no Início da Coleta de Dados**:
    1.  **Identificação de Fontes Potenciais**: O primeiro passo consiste em um levantamento exaustivo de onde os dados relevantes para a tarefa do LLM podem ser encontrados.
    2.  **Clareza sobre o Propósito do Modelo**: É crucial ter uma definição precisa do que se espera que o modelo realize e qual problema específico ele visa solucionar.
        * **Análise Crítica da Ferramenta**: Deve-se ponderar se a modelagem de linguagem é, de fato, a abordagem mais adequada. Em cenários que exigem altíssima precisão ou onde a interpretabilidade é paramount, um modelo de machine learning pode não ser a melhor escolha, e alternativas (como sistemas baseados em regras ou abordagens determinísticas) devem ser consideradas.
    3.  **Caracterização Detalhada de Entradas e Saídas**:
        * Qual a natureza da entrada (input) que o modelo processará? (ex: dados estruturados de bancos de dados, texto livre de páginas web, documentos PDF, código-fonte).
        * Qual a natureza da saída (output) esperada do modelo? (ex: resumos concisos, respostas diretas a perguntas, classificação de sentimentos, tradução para outro idioma, geração de código).
        * Esta caracterização detalhada é fundamental para orientar a coleta e o processamento dos dados.
    4.  **Mapeamento de Recursos de Dados Existentes**: Identificar quais fontes de informação (internas ou externas) são atualmente utilizadas por humanos para executar tarefas similares àquelas que o LLM deverá realizar.
        * Fontes internas: Se existem, qual a facilidade de acesso e coleta?
        * Fontes externas: Mais comumente, a busca se direciona a dados externos que as pessoas acessam em seu dia a dia (ex: websites, publicações, fóruns).
* **Escopo da Coleta**: Para os propósitos desta seção do curso, o foco recai sobre a coleta de dados de fontes externas, com ênfase particular na obtenção de informações da internet.

---

## 5. Coletando Dados da Internet: Métodos e Considerações Ético-Legais

* **Principais Métodos de Coleta de Dados da Web**:
    1.  **APIs (Application Programming Interfaces)**:
        * **Definição**: APIs são conjuntos de definições e protocolos que permitem que diferentes softwares se comuniquem entre si. No contexto da coleta de dados, elas são interfaces que os provedores de dados disponibilizam para acesso programático e controlado aos seus dados hospedados.
        * **Funcionamento Típico**: Geralmente, é necessário um registro prévio para obter uma **chave de API (API key)**, que autentica as requisições. As requisições feitas a uma API costumam retornar dados bem estruturados, mais comumente nos formatos JSON (JavaScript Object Notation) ou XML (eXtensible Markup Language).
            * **JSON**: Formato leve, baseado em texto, fácil para humanos lerem e escreverem, e fácil para máquinas parsearem e gerarem.
            * **XML**: Formato projetado para transportar e armazenar dados, com ênfase na legibilidade e na capacidade de representar estruturas de dados complexas.
        * **Vantagens**: APIs são o método preferencial quando disponíveis, pois representam um canal oficial e suportado para a coleta de dados, facilitando a integração e a manutenção de sistemas que dependem desses dados. Elas também costumam ter documentação clara sobre o uso, limites de taxa (rate limits) e formatos de dados.
    2.  **Web Scraping (Raspagem de Dados Web)**:
        * **Definição**: Scraping envolve o desenvolvimento de scripts ou programas (bots) que fazem requisições HTTP a páginas web, baixando o conteúdo HTML dessas páginas. Subsequentemente, esse HTML é parseado para extrair as informações desejadas.
        * **Impacto e Custo**: O acesso intensivo via scraping pode impor uma carga considerável aos servidores do site-alvo, tornando-se uma operação potencialmente custosa para o hospedeiro da informação em termos de tráfego e recursos computacionais.
        * **Ferramentas Comuns**: Bibliotecas como `Requests` (para requisições HTTP) e `BeautifulSoup` ou `Scrapy` (para parsing de HTML/XML) em Python são amplamente utilizadas.
* **Considerações Legais e Éticas Essenciais**:
    * **Licenciamento de Dados**: É fundamental verificar os termos de uso e as licenças associadas aos dados que se pretende coletar, especialmente se houver intenção de uso comercial. Alguns dados são proprietários, outros possuem licenças Creative Commons com diferentes restrições (ex: necessidade de atribuição, proibição de uso comercial). Código-fonte, em particular, pode ter licenças complexas (GPL, MIT, Apache) que regem seu uso e distribuição. Em caso de dúvida, a consulta a um profissional jurídico é recomendada.
    * **Legalidade e Respeito no Scraping**:
        * Embora o scraping de dados publicamente acessíveis seja geralmente considerado legal em muitas jurisdições (com exceções e nuances importantes, como violação de termos de serviço ou login), ele nem sempre é bem-visto ou permitido pelos proprietários dos sites.
        * **Boas Práticas**:
            * **`robots.txt`**: Sempre verifique o arquivo `robots.txt` do site (ex: `www.exemplo.com/robots.txt`). Este arquivo indica quais partes do site os web crawlers (incluindo scrapers) devem ou não acessar. Respeitar essas diretivas é uma prática ética fundamental.
            * **Moderação**: Faça scraping de forma responsável: colete apenas os dados estritamente necessários, evite fazer requisições em alta frequência (implemente delays entre requisições) e, se possível, faça scraping fora dos horários de pico de tráfego do site para minimizar o impacto.
            * **Identificação**: Considere identificar seu scraper no User-Agent da requisição HTTP, informando um contato caso o administrador do site precise falar com você.
        * Muitos sites implementam medidas anti-scraping (ex: CAPTCHAs, bloqueio de IPs). Tentar contorná-las agressivamente pode levar a problemas legais ou éticos.
    * **Toxicidade e Qualidade dos Dados Online**: A internet é um repositório vasto, mas também contém informações incorretas, desatualizadas, tendenciosas, discurso de ódio, spam e outro conteúdo "tóxico". É crucial estar ciente disso e implementar estratégias para filtrar ou evitar a inclusão desse tipo de material problemático no dataset do LLM, pois o modelo aprenderá com esses dados.
* **Balanço Final**: Quando conduzida de forma legal, ética e responsável, a coleta de dados da internet pode ser uma fonte inestimável de informações para treinar LLMs poderosos e relevantes para tarefas específicas.

---

## 6. Demonstração Prática de Web Scraping Básico

* **Ferramentas Utilizadas**: A demonstração foca no uso de duas bibliotecas Python populares:
    * **`requests`**: Uma biblioteca elegante e simples para fazer requisições HTTP (como GET, POST) para obter o conteúdo de URLs da web.
    * **`BeautifulSoup`**: Uma biblioteca para parsear documentos HTML e XML. Ela cria uma árvore de parse a partir do HTML bruto, permitindo navegar, buscar e modificar o conteúdo de forma intuitiva e programática.
* **Fluxo de Trabalho Demonstrado**:
    1.  **Obtenção do Conteúdo HTML**:
        * Utiliza-se `requests.get(URL)` para fazer uma requisição à URL desejada e obter a resposta do servidor, que inclui o HTML da página.
        * Na demonstração, o resultado é salvo em um arquivo local (`language_of_flowers.html`) para evitar múltiplas requisições ao mesmo servidor durante o desenvolvimento ou re-execução do código, o que é uma boa prática.
    2.  **Parsing com BeautifulSoup**:
        * O conteúdo HTML (do arquivo local ou diretamente da resposta da requisição) é passado para o construtor de `BeautifulSoup` para criar um objeto "soup". Este objeto representa o documento HTML como uma estrutura de dados aninhada que pode ser facilmente navegada.
        * O método `.prettify()` pode ser usado para exibir o HTML parseado com indentação, o que pode ajudar na visualização da estrutura, especialmente em páginas mais simples.
    3.  **Extração de Informações Específicas**:
        * **Busca por Tags**: `BeautifulSoup` permite encontrar tags HTML específicas.
            * Exemplo: `soup.title` retorna a tag `<title>` completa. Para obter apenas o texto dentro da tag, usa-se `.text` (ex: `soup.title.text`). O método `.strip()` é útil para remover espaços em branco extras no início e no fim do texto extraído.
            * Exemplo: `soup.find_all('p')` retorna uma lista de todas as tags `<p>` (parágrafos) no documento. Pode-se iterar sobre essa lista para extrair o texto de cada parágrafo.
        * **Busca por Atributos (Classes, IDs)**: É possível encontrar tags com base em seus atributos, como `class` ou `id`. Isso é particularmente útil porque classes CSS são frequentemente usadas para estilizar e semanticamente agrupar elementos com propósitos similares.
            * Exemplo: Para encontrar um uploader específico que está dentro de uma tag `<a>` com uma classe CSS particular como `item-upload-info_uploader-name`, pode-se usar `soup.find('a', class_='item-upload-info_uploader-name')`. Isso permite extrair dados de forma mais direcionada e robusta, mesmo que a estrutura da página mude ligeiramente, contanto que as classes permaneçam.
            * Outro exemplo: Extrair todos os itens de uma coleção, onde cada item é uma tag `<a>` com a classe `collection-item`.
* **Flexibilidade**: A chave para um scraping eficaz é entender a estrutura do HTML da página alvo. Com esse entendimento e as ferramentas certas, é possível extrair uma vasta gama de informações. O uso de seletores CSS (não explicitamente detalhado na demo, mas implícito pela busca de classes) é uma técnica poderosa dentro do `BeautifulSoup` para localizar elementos de forma precisa.

---

## 7. Critérios para Avaliação da Qualidade de Dados em LLMs

* **Distinção de Dados Tabulares**: No contexto de dados tabulares (planilhas, bancos de dados), a qualidade dos dados frequentemente se refere a questões como valores ausentes (missing values), inconsistências entre campos (inconsistent fields), outliers e a necessidade de codificar valores categóricos para formatos numéricos. Para Modelos de Linguagem Grandes (LLMs), que primariamente processam entradas e geram saídas em formato de texto não numérico, os critérios de qualidade são diferentes e adaptados à natureza da linguagem natural.
* **Propriedades Fundamentais da Qualidade de Texto para LLMs**:
    1.  **Normalidade Sintática e Semântica do Texto**:
        * **Definição**: O texto utilizado para treinar o LLM deve ser "normal" tanto em sua estrutura gramatical (sintaxe) quanto em seu significado (semântica), considerando o contexto da tarefa para a qual o modelo está sendo preparado.
        * **Sintaxe**: Refere-se às regras gramaticais e à estrutura que organizam as palavras em sentenças corretas e compreensíveis em uma determinada língua. Uma sentença pode ter o mesmo significado que outra, mas se sua sintaxe for muito peculiar ou incorreta, pode soar artificial ou ser difícil de processar pelo modelo (e por humanos).
            * Exemplo: "Erick Galinkin é um hacker e pesquisador de inteligência artificial cuja paixão é encontrar maneiras de aplicar IA à segurança e segurança à IA" (sintaxe natural) vs. "Erick Galinkin paixão é em encontrar maneiras de aplicar IA à segurança e aplicar segurança à IA e é um hacker e pesquisador de inteligência artificial" (mesmo significado, sintaxe incomum).
        * **Semântica**: Diz respeito ao significado das palavras, frases e sentenças. Pequenas alterações no texto, como a mudança de um tempo verbal (ex: trocar "é" por "era"), podem preservar uma sintaxe similar mas alterar drasticamente o significado transmitido.
            * Exemplo: Alterar "Erick Galinkin *é* um hacker..." para "Erick Galinkin *foi* um hacker..." implica que ele não é mais essas coisas, mudando a semântica.
        * **Variação por Domínio**: Em campos altamente especializados como direito, medicina ou finanças, a sintaxe e a semântica consideradas "normais" podem divergir significativamente do uso cotidiano da linguagem encontrado em livros gerais, fóruns da internet ou páginas web comuns. É crucial que o dataset reflita a linguagem específica do domínio da tarefa.
    2.  **Relevância do Texto para a Tarefa**:
        * **Definição**: O conteúdo do texto deve ser diretamente pertinente e útil para a tarefa que o LLM precisa aprender a executar.
        * **Desafio da Avaliação em Escala**: Avaliar a relevância de cada fragmento de texto individualmente é um processo intensivo em mão de obra, geralmente exigindo que especialistas no domínio revisem o material. Esta abordagem não é escalável para os volumes massivos de dados (milhões ou bilhões de palavras) tipicamente usados no treinamento de LLMs.
        * **Importância da Procedência e Confiança na Fonte**: Dada a dificuldade de avaliação individual em larga escala, torna-se vital confiar nas fontes de onde os dados são coletados.
            * Exemplo prático (assistente médico de IA): Para treinar um assistente virtual para médicos, seria necessário um volume substancial de dados sobre desfechos de saúde e práticas médicas. Embora existam inúmeros posts em fóruns da internet onde pessoas dão conselhos médicos, esses dados geralmente não são confiáveis e não deveriam ser incorporados ao dataset. Tais fontes podem conter informações incorretas, conselhos prejudiciais, spam, posts não relacionados e diversas formas de toxicidade online, que contaminariam o aprendizado do modelo.
            * **Alternativas Confiáveis**: Em vez de fontes não verificadas, deve-se buscar parcerias com redes de saúde para utilizar comunicações anônimas entre pacientes e médicos (respeitando regulações de privacidade como HIPAA nos EUA ou LGPD no Brasil) ou recorrer a fontes de dados públicos de alta credibilidade, como o PubMed, que agrega artigos de pesquisa médica científica.

---

## 8. Processos e Técnicas de Limpeza de Dados Textuais

* **O Desafio do HTML Bruto**: Após a etapa de scraping de páginas web, o resultado imediato é o código HTML, que, embora contenha a informação desejada, também é repleto de tags, scripts e metadados estruturais que são irrelevantes para o conteúdo textual que o LLM precisa aprender. A inspeção e extração manual desses dados é impraticável.
* **Exemplo Prático**: Desenvolver um modelo de IA capaz de redigir biografias para profissionais da área técnica, utilizando como fonte uma página web que lista perfis de funcionários, incluindo os do instrutor.
* **Etapas do Processo de Limpeza e Extração**:
    1.  **Carregamento e Inspeção Inicial**: Carregar o HTML (preferencialmente de um arquivo local para evitar sobrecarga ao servidor web). Identificar visualmente ou com ferramentas de desenvolvedor do navegador onde as informações de interesse (ex: as biografias) estão localizadas na estrutura do HTML (ex: dentro de tags `<p>`, `<div>` com classes ou IDs específicos como `bio-container` ou `bio-content`).
    2.  **Pré-processamento Básico**:
        * **Condensação de Espaços em Branco**: Remover espaços, tabulações e quebras de linha excessivas para tornar o texto mais compacto e fácil de processar.
        * **Remoção de Tags HTML (Stripping)**: Utilizar bibliotecas (como `BeautifulSoup`) para extrair apenas o conteúdo textual das tags, descartando as próprias tags, que são primariamente para a renderização no navegador e não para o conteúdo semântico do texto. O texto resultante é mais legível, mas ainda pode conter muito ruído e informações não pertinentes.
    3.  **Extração Direcionada**: Criar funções para parsear o HTML e extrair texto apenas de seções ou tags específicas que contêm os dados relevantes (ex: iterar sobre todas as `divs` com a classe `bio-content`). O resultado é uma lista de strings, cada uma representando um item de dado (ex: uma biografia).
    4.  **Filtragem e Refinamento da Extração**:
        * Pode ser necessário aplicar lógicas adicionais para isolar o dado exato. Por exemplo, se uma biografia estiver sempre na última linha de um bloco de texto dividido por quebras de linha, ou se biografias válidas sempre tiverem um comprimento mínimo de caracteres (ex: mais de 50 caracteres para distinguir de textos curtos não biográficos).
* **Correção Ortográfica e Gramatical Automatizada**:
    * **Problema**: Mesmo após a extração, o texto pode conter erros ortográficos, digitações, caracteres faltantes ou outros problemas que afetam a qualidade.
    * **Soluções**:
        * **Bibliotecas Open Source**: Ferramentas como `SymSpell` podem ser usadas para realizar correções ortográficas programaticamente. `SymSpell` utiliza algoritmos baseados em distância de edição (edit distance) e frequência de palavras para sugerir correções.
            * **Distância de Edição**: É o número mínimo de operações de edição (inserção, exclusão ou substituição de um único caractere) necessárias para transformar uma string em outra. `SymSpell` busca palavras no dicionário que estejam dentro de uma distância de edição máxima da palavra incorreta.
            * **Dicionários**: Requer um dicionário de frequência de palavras da língua alvo (ex: um dicionário para o inglês).
        * **Produtos Comerciais**: Existem também APIs e produtos comerciais robustos para verificação ortográfica e gramatical.
    * **Desafios na Correção**:
        * Nomes próprios e jargões técnicos podem ser erroneamente sinalizados como erros se não estiverem no dicionário. Uma estratégia é ignorar palavras capitalizadas, assumindo que são nomes próprios, mas isso pode levar à não correção de palavras comuns capitalizadas no início de frases ou erros de capitalização.
        * A correção pode nem sempre ser perfeita e, em alguns casos, pode até introduzir erros se as sugestões não forem adequadas.
        * Muitas ferramentas simples de correção podem remover ou alterar a pontuação.
    * **Resultado Desejado**: O objetivo é obter um texto o mais limpo e correto possível, pois isso impacta diretamente a capacidade do LLM de aprender padrões linguísticos válidos. Um dataset mais limpo geralmente leva a um modelo mais robusto e com melhor desempenho.

---

## 9. Panorama das Tarefas de Modelagem de Linguagem e Arquiteturas de LLMs

* **A Revolução da Arquitetura Transformer**:
    * Os Modelos de Linguagem Grandes (LLMs) contemporâneos são predominantemente baseados na arquitetura **Transformer**, introduzida em um paper seminal de 2017 por Vaswani et al. do Google Brain.
    * O avanço crucial do Transformer foi o uso do **mecanismo de atenção (attention mechanism)**, e mais especificamente o "self-attention", que permite ao modelo ponderar a importância de diferentes palavras (tokens) na sequência de entrada ao processar cada palavra, capturando dependências de longo alcance no texto de forma eficiente.
    * Exemplos proeminentes de modelos baseados em Transformer incluem:
        * **BERT (Bidirectional Encoder Representations from Transformers)**: Focado no uso de encoders do Transformer.
        * **GPT (Generative Pre-trained Transformer)**: Focado no uso de decoders do Transformer.
* **LLMs como Modelos de Fundação (Foundation Models)**:
    * LLMs pré-treinados em vastos corpora de dados são frequentemente chamados de "modelos de fundação". Eles adquirem um conhecimento linguístico e factual amplo, servindo como uma base robusta que pode ser subsequentemente especializada para uma miríade de tarefas downstream através do processo de fine-tuning.
* **Principais Tarefas de Modelagem de Linguagem**:
    1.  **Geração de Texto**: O modelo recebe uma entrada (prompt, instrução, pergunta) e gera uma sequência de texto como saída.
        * **Masked Language Modeling (MLM)**: Objetivo de treinamento típico de modelos como o BERT. Durante o treinamento, alguns tokens na sentença de entrada são substituídos por um token especial `[MASK]`, e o modelo é treinado para prever os tokens originais que foram mascarados, com base no contexto bidirecional (palavras antes e depois da máscara).
        * **Causal Language Modeling (CLM)**: Objetivo de treinamento típico de modelos como o GPT. O modelo é treinado para prever o próximo token em uma sequência, dado todos os tokens anteriores (contexto unidirecional, da esquerda para a direita). Esta é a base para a geração de texto livre.
    2.  **Sumarização Abstrativa**: Gerar um resumo conciso que capture as ideias principais de um texto mais longo, utilizando palavras e frases que podem não estar presentes no texto original (em contraste com a sumarização extrativa, que seleciona frases do original). CLM é naturalmente adequado para esta tarefa.
    3.  **Resposta a Perguntas (Question Answering - QA)**:
        * **QA Extrativa**: Dada uma pergunta e um texto de contexto, o modelo localiza e extrai o trecho (span) exato do contexto que contém a resposta. A resposta é uma cópia de parte do texto original.
        * **QA Abstrativa**: O modelo gera uma resposta em linguagem natural, que é semanticamente correta e responde à pergunta, mas não se limita a extrair texto verbatim do contexto.
    4.  **Classificação de Texto**: Atribuir um ou mais rótulos predefinidos a um trecho de texto. Os rótulos podem ser binários (ex: spam/não spam, positivo/negativo) ou multiclasse/multirrótulo (ex: categorizar notícias em tópicos como esportes, política, finanças).
    5.  **Tradução Automática**: Converter texto de um idioma para outro. Esta foi uma das primeiras e mais impulsionadoras aplicações da PLN e continua sendo uma área de pesquisa ativa e de grande impacto.
    6.  **Clusterização (Clustering) e Busca Semântica**:
        * **Clusterização**: Agrupar automaticamente documentos ou sentenças com base em sua similaridade semântica, sem rótulos predefinidos.
        * **Busca Semântica**: Encontrar textos relevantes para uma consulta não apenas com base em palavras-chave, mas no significado. LLMs, especialmente seus encoders, são usados para gerar **embeddings** (representações vetoriais densas) de textos. Esses embeddings capturam a semântica, e textos com embeddings próximos no espaço vetorial são considerados semanticamente similares. Bancos de dados vetoriais são usados para armazenar e consultar esses embeddings eficientemente.
* **Seleção da Arquitetura do Modelo Conforme a Tarefa**:
    * **Modelos Autoregressivos (Decoder-only, ex: família GPT)**: São inerentemente bons em tarefas que exigem geração de texto fluente e coerente, como geração de texto aberta baseada em instruções (estilo ChatGPT), sumarização abstrativa e QA abstrativa. Eles geram texto token por token, condicionando cada novo token nos tokens anteriores.
    * **Modelos Autoencoders (Encoder-only, ex: BERT, RoBERTa)**: Excelentes para tarefas que se beneficiam de uma compreensão profunda e contextualizada de toda a sequência de entrada.
        * **Classificação**: O encoder transforma a sequência de entrada em uma representação vetorial de tamanho fixo (ex: o embedding do token `[CLS]`) que pode ser alimentada a uma camada classificadora simples.
        * **QA Extrativa**: Podem prever os tokens de início e fim da resposta dentro do texto de contexto.
        * **Clusterização/Busca Semântica**: A representação de saída do encoder (embedding) é ideal para calcular similaridade entre textos.
    * **Modelos Sequence-to-Sequence (Encoder-Decoder, ex: T5, BART, MarianMT)**: Possuem tanto um encoder (para processar a entrada) quanto um decoder (para gerar a saída). São naturalmente adequados para tarefas que mapeiam uma sequência de entrada para uma sequência de saída, como tradução automática e sumarização.