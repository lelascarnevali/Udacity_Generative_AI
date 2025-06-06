### 1. Histórico dos Modelos de Linguagem
Historicamente, as **Redes Neurais Recorrentes (RNNs)**, como as **LSTMs (Long Short-Term Memory)**, foram as arquiteturas predominantes para tarefas de Processamento de Linguagem Natural (PNL). No entanto, as RNNs processam os tokens de entrada sequencialmente, um por um, consolidando-os em um único **vetor de contexto** ou **estado oculto**. Esse método as tornava suscetíveis ao **problema do gradiente evanescente**, onde o estado oculto podia perder informações importantes em sequências muito longas.

Para mitigar esse problema, as LSTMs introduziram **portões de esquecimento** e **portões de entrada**, permitindo que a rede neural controlasse quais informações reter e quais descartar. Apesar dessas melhorias, as RNNs ainda apresentavam limitações no manuseio de dependências de longo alcance e na capacidade de paralelização, o que as tornava lentas para o treinamento em grandes conjuntos de dados.

O conceito de **atenção** surgiu como uma solução para essas deficiências, permitindo que o modelo "olhe" para diferentes partes da sequência de entrada ao gerar a saída. Inicialmente, a atenção foi integrada às RNNs como um mecanismo para combinar os estados ocultos do codificador a cada passo de tempo, formando um vetor de contexto que o decodificador poderia usar para "escolher" a quantidade de atenção a ser dada a cada token de entrada. Essa abordagem é comparável a um "telefone sem fio" modificado, onde a tradução é feita com base na mensagem completa, e não apenas no último pedaço recebido.

---
### 2. Definição de Atenção
A atenção é um conceito fundamental em modelos de linguagem que permite à rede neural focar em partes específicas de uma sequência de entrada ao processar ou gerar uma saída. A terminologia **"query", "key"** e **"value"** (consulta, chave e valor) tem suas raízes no campo de bancos de dados. De forma análoga a um banco de dados, onde uma consulta é usada para encontrar uma chave correspondente e, por sua vez, recuperar um valor, a atenção constrói um **embedding contextualizado** a partir de vetores de "correspondência suave". Isso significa que, em vez de uma correspondência exata, o modelo calcula uma pontuação de similaridade entre a consulta e todas as chaves, e então usa essas pontuações para ponderar a soma dos valores.

Existem diferentes tipos de mecanismos de atenção:

* **Atenção Multiplicativa (Dot-Product Attention)**: Este é o tipo mais eficiente de atenção, onde a pontuação de atenção é calculada pelo produto escalar entre a consulta e a chave. É computacionalmente eficiente e eficaz quando as dimensões da consulta e da chave são as mesmas. Frequentemente, é implementada usando o **produto escalar**, que é altamente otimizado para GPUs. Antes de aplicar a função softmax, o produto escalar é dividido pela raiz quadrada da dimensão da chave ($d_k$). Essa escala é aplicada para evitar gradientes muito grandes ou muito pequenos, o que poderia levar a problemas de estabilidade durante o treinamento. A fórmula completa para atenção multiplicativa escalada é:
    $Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt{d_k}})V$
    Sem a escala, a fórmula é:
    $Attention(Q,K,V)=softmax(QK^T)V$

* **Atenção Aditiva (Additive Attention ou Bahdanau Attention)**: Embora mais complexa, a atenção aditiva é útil quando as dimensões da consulta e da chave são diferentes. Ela usa uma camada oculta e uma função de ativação, geralmente `tanh`, para calcular as pontuações de atenção. Apesar de ser mais flexível, é menos eficiente que a atenção multiplicativa devido à sua complexidade. A fórmula para atenção aditiva é:
    $Attention(Q,K,V)=softmax(W_2tanh(QW_1+(KW_3)^T))V$
    Nesta fórmula, $W_1$ é uma matriz de projeção da consulta que transforma $Q$ em um espaço oculto, $W_2$ é uma matriz de projeção de pontuação que transforma $Q+K$ em logits de atenção escalar, e $W_3$ é uma matriz de projeção da chave que transforma $K$ em um espaço oculto. Todas as três matrizes $W$ são parâmetros aprendíveis treinados durante a retropropagação.

* **Atenção Geral (General Attention)**: A atenção geral é uma otimização da atenção aditiva. Ela também permite dimensões flexíveis para consulta e chave, mas é mais eficiente ao remover algumas das matrizes de peso presentes na atenção aditiva. Isso resulta em computação mais rápida e melhor eficiência de espaço, o que é crucial para dados de alta dimensão. No entanto, ainda é menos eficiente que a atenção multiplicativa e deve ser utilizada apenas quando a flexibilidade nas dimensões da consulta e da chave for estritamente necessária. A fórmula é:
    $GeneralAttention(Q,K,V)=softmax(QW_gK^T)V$
    Nesta fórmula, $W_g$ é outra matriz de projeção que é aprendida durante o treinamento do modelo, dando mais flexibilidade do que a similaridade bruta de consulta-chave produzida pelo produto escalar.

O cálculo das pontuações de atenção envolve os seguintes passos:
1.  **Cálculo da similaridade**: A pontuação de similaridade entre a consulta e cada chave é calculada.
2.  **Normalização (Softmax)**: As pontuações são normalizadas usando a função softmax, garantindo que a soma das ponderações seja 1. Isso transforma as pontuações em uma distribuição de probabilidade.
3.  **Soma ponderada**: Os valores são combinados usando as pontuações de atenção normalizadas como pesos.
Na prática, as matrizes de consulta, chave e valor são transformadas usando uma transformação aprendida (camadas totalmente conectadas) antes de serem passadas pela fórmula de atenção. Se representarmos essas camadas totalmente conectadas usando $W_Q$, $W_K$ e $W_V$ para as transformações de consulta, chave e valor, respectivamente, a fórmula de atenção para atenção multiplicativa (produto escalar) escalada se torna:
$Attention(QW_Q,KW_K,VW_V) = Softmax(\frac{(QW_Q)(KW_K)^T}{\sqrt{d_k}})(VW_V)$
É importante notar que, em implementações de código de Transformers, $q$, $k$, e $v$ geralmente se referem aos valores *após* a transformação linear. Por exemplo:
```python
def attention(query, key, value):
    "Compute 'Scaled Dot Product Attention'"
    d_k = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
    p_attn = scores.softmax(dim=-1)
    return torch.matmul(p_attn, value)
```
Este código implementa a fórmula:
$Attention(Q,K,V)=Softmax(\frac{QK^T}{\sqrt{d_k}})V$

---
### 3. Mecanismos de Atenção
Os mecanismos de atenção, como a **autoatenção** e a **atenção cruzada**, descrevem como a atenção é aplicada dentro de uma rede neural, especificamente em relação à origem e ao destino da atenção.

* **Autoatenção (Self-Attention)**: Neste mecanismo, o conjunto de consultas, chaves e valores são todos idênticos, geralmente provenientes da saída das camadas anteriores. A autoatenção é utilizada para calcular a atenção dentro de uma única sequência, permitindo que cada posição na sequência atenda a todas as outras posições na mesma sequência. Isso é crucial para entender as relações contextuais entre os elementos de uma sequência, independentemente da distância entre eles. A autoatenção possui uma distância de interação de $O(1)$, o que é uma melhoria significativa em relação à distância de interação $O(n)$ de uma RNN, embora tenha uma complexidade computacional de $O(n^2)$. A multiplicação de matrizes para calcular a autoatenção pode ser paralelizada, o que é uma grande vantagem em termos de eficiência computacional.

* **Atenção Multi-Cabeça (Multi-Head Attention)**: Este mecanismo utiliza múltiplas "cabeças" de Q, K e V. Cada cabeça possui seu próprio conjunto de pesos, e a atenção é distribuída, com cada cabeça focando em uma característica especializada diferente da entrada. Os resultados dos diferentes cálculos de atenção são concatenados para formar um resultado maior.

* **Atenção Multi-Consulta (Multi-Query Attention)**: Diferente da atenção multi-cabeça, na atenção multi-consulta, cada consulta é distinta e compartilha a mesma chave e valor. Em comparação com a atenção multi-cabeça, é mais eficiente e pode aumentar significativamente o tamanho do lote de treinamento através do compartilhamento de parâmetros. Grandes LLMs com bilhões de parâmetros, como Falcon e LLaMA 2, utilizam atenção multi-consulta.

* **Atenção Cruzada (Cross-Attention)**: Na atenção cruzada, as consultas vêm de uma fonte e as chaves e valores vêm de outra fonte diferente ($Q \neq K, V$). Um exemplo clássico é em modelos de tradução, onde as consultas vêm do decodificador (a língua de destino) e as chaves e valores vêm do codificador (a língua de origem). Isso permite que o decodificador preste atenção às partes relevantes da sequência de entrada (no codificador) ao gerar a saída. Este mecanismo é especialmente útil para tarefas onde diferentes tipos de dados interagem, como legendagem de imagens.

A arquitetura do **Transformer**, por exemplo, utiliza ambos os tipos de atenção. O codificador emprega autoatenção para processar a sequência de entrada, enquanto o decodificador utiliza tanto autoatenção (para processar a sequência de saída já gerada) quanto atenção cruzada (para focar na entrada do codificador).

A autoatenção, embora poderosa, não compreende a ordem de entrada por padrão, sendo necessário adicionar **embeddings posicionais** como parte dos embeddings de entrada para fornecer informações sobre a posição. Além disso, como as camadas de autoatenção não possuem não-linearidade por padrão, uma **rede feed-forward** é adicionada após cada token processado para permitir que o modelo capture mais complexidade. Para evitar que o modelo "trapaceie" ao prever uma sequência (olhando para o "futuro"), a atenção em palavras futuras é **mascarada** durante a decodificação.

---
### 4. Arquiteturas de Transformers
As arquiteturas de **Transformers** são construídas a partir de blocos de camadas de autoatenção e podem ser classificadas em três tipos principais:

* **Apenas Codificador (Encoder-only)**: Exemplos incluem o **BERT (Bidirectional Encoder Representations from Transformers)**. Essas arquiteturas são excelentes para tarefas que exigem uma compreensão profunda da entrada, como classificação de texto, análise de sentimento e extração de características. Elas processam toda a sequência de entrada de uma vez e não são projetadas para gerar novas sequências. O BERT, por exemplo, é treinado usando **Masked Language Modeling (MLM)** e **Next Sentence Prediction (NSP)** para aprender representações contextuais da linguagem.

* **Codificador-Decodificador (Encoder-Decoder)**: Um exemplo notável é o **T5 (Text-to-Text Transfer Transformer)**. Essa arquitetura é ideal para tarefas que envolvem mapeamento de uma sequência de entrada para uma sequência de saída, como tradução de idiomas, sumarização e resposta a perguntas. O codificador processa a entrada e o decodificador gera a saída, utilizando atenção cruzada para focar nas informações relevantes do codificador.

* **Apenas Decodificador (Decoder-only)**: Os modelos **GPT (Generative Pre-trained Transformer)** são exemplos proeminentes desta categoria. Eles são particularmente bons para **geração de linguagem**, como chatbots, criação de conteúdo e escrita criativa. Esses modelos preveem o próximo token na sequência com base nos tokens anteriores, operando de forma autoregressiva. Cada token gerado se torna parte da entrada para a previsão do próximo token.

A arquitetura original do Transformer superou as RNNs ao endereçar o problema do gradiente evanescente e ao permitir a **paralelização** do cálculo da atenção, o que acelera significativamente o treinamento. Elementos adicionais nos Transformers incluem:

* **Embeddings Posicionais (Positional Embeddings)**: Como a autoatenção não possui intrinsecamente a capacidade de capturar a ordem sequencial dos tokens, os embeddings posicionais são adicionados aos embeddings de entrada para fornecer informações sobre a posição relativa ou absoluta de cada token na sequência. Isso é crucial para tarefas onde a ordem dos elementos é importante para o significado, como na linguagem natural. Existem diferentes métodos para calcular esses embeddings, sendo os baseados em seno e cosseno (sinusoidais) os mais comuns, o que permite que o modelo generalize para sequências de diferentes comprimentos. Outros tipos incluem embeddings posicionais aprendidos (usados em BERT e GPT), embeddings posicionais relativos (TransformerXL) e embeddings posicionais rotativos.
* **Conexões Residuais (Residual Connections ou Skip Layers)**: Elas permitem que as entradas de uma camada sejam adicionadas diretamente à sua saída, após a camada de atenção. Isso ajuda a mitigar o problema do gradiente evanescente, facilitando o treinamento de redes muito profundas, pois o gradiente pode fluir mais facilmente através da rede. As conexões residuais, que se originaram no artigo ResNets de 2015 de He et al. para tarefas de visão computacional, são um tipo de camada ignorada.
* **Normalização de Camada (Layer Normalization)**: Aplicada após as conexões residuais, a normalização de camada ajuda a estabilizar e acelerar o treinamento ao normalizar as ativações da camada. O processo envolve subtrair a média e dividir pelo desvio padrão das entradas para cada amostra. Isso impacta os gradientes usados para a retropropagação, de forma similar à escala da pontuação de atenção.
* **Rede Feed-Forward**: Uma rede neural feed-forward é adicionada após cada camada de autoatenção e normalização. Ela introduz a não-linearidade necessária no modelo. Sem essa não-linearidade, múltiplas camadas de atenção combinadas equivaleriam a uma única camada, limitando a capacidade expressiva do modelo.

---
### 5. Treinamento de Transformers
O treinamento de modelos Transformer modernos geralmente envolve duas fases principais:

* **Pré-treinamento (Self-supervised learning)**: Esta fase visa produzir um **checkpoint de propósito geral**. Os modelos são treinados em grandes quantidades de dados não rotulados usando objetivos de auto-supervisão. Isso significa que a verdade fundamental pode ser construída dentro da estrutura dos dados, sem a necessidade de anotação manual. Alguns dos objetivos de pré-treinamento mais comuns incluem:
    * **Autoregressivo**: Modelos preveem o próximo token usando sua própria saída anterior. O **GPT (Generative Pre-trained Transformer)** é um exemplo proeminente com um objetivo autoregressivo, sendo treinado para prever a próxima palavra em uma sequência, o que o torna excelente para geração de texto. As pontuações de atenção para tokens futuros são definidas como infinito negativo para evitar "trapaças", e o modelo então escolhe o candidato com a maior probabilidade para o próximo token. Uma técnica chamada "teacher forcing", usada desde os anos 80, pode ser empregada para evitar que o modelo acumule erros e continue em um ciclo de feedback vicioso durante o treinamento.
    * **Autoencoder de Denoising**: Modelos corrompem uma entrada e, em seguida, tentam recuperá-la usando seu entorno. O **BERT (Bidirectional Encoder Representations from Transformers)** utiliza **Masked Language Modeling (MLM)**, onde uma porcentagem dos tokens de entrada é mascarada e o modelo deve prever os tokens originais com base no contexto bidirecional. Isso torna o BERT bem preparado para tarefas de classificação e compreensão de texto. O BERT também otimiza para o objetivo de **Next Sentence Prediction (NSP)**, onde o modelo aprende a prever se duas sentenças estão relacionadas (uma classificação binária).
    * **Objetivo Contrastivo**: Esta abordagem se concentra em aprender representações que maximizam a similaridade entre exemplos relacionados e minimizam a similaridade entre exemplos não relacionados.

* **Fine-tuning (Ajuste fino)**: Após o pré-treinamento, o modelo é **ajustado** para casos de uso específicos de domínio. Isso envolve treinamento adicional do modelo em dados rotulados menores e mais específicos. O ajuste fino é particularmente útil porque permite que o modelo pré-treinado, que já capturou um vasto conhecimento da linguagem, seja adaptado para tarefas específicas com menos dados e tempo de treinamento, resultando em desempenho aprimorado. Além do ajuste fino, outras técnicas como prompting e geração aumentada por recuperação (retrieval-augmented generation) também são usadas para adaptar modelos pré-treinados.

---
### 6. Prós e Contras dos Transformers
Os Transformers se destacam por suas capacidades que revolucionaram o campo da IA, mas também apresentam desafios.

**Vantagens dos Transformers:**

* **Hardware Acceleration (Aceleração de Hardware)**: Uma das principais razões para o sucesso dos Transformers é a capacidade de aproveitar a aceleração de hardware fornecida pelas **GPUs (Graphics Processing Units)**. GPUs possuem muitas unidades de processamento pequenas e paralelas, o que as torna até 10 vezes mais rápidas que as CPUs monolíticas para treinar Transformers. Frameworks de Deep Learning como **PyTorch** e **JAX** utilizam **CUDA**, uma biblioteca de programação numérica otimizada para realizar eficientemente as **multiplicações de matrizes** em larga escala, que são o bloco de construção fundamental das redes neurais.

* **Parallelization (Paralelização)**: A arquitetura do Transformer permite a computação paralela, ao contrário das RNNs que processam dados sequencialmente. Isso significa que todas as operações dentro de uma camada de autoatenção podem ser realizadas simultaneamente, reduzindo significativamente o tempo de treinamento.

* **Long-Range Dependencies (Dependências de Longo Alcance)**: Ao contrário das RNNs que sofrem do problema do gradiente evanescente e podem "esquecer" informações em sequências longas, a autoatenção nos Transformers permite que o modelo capture dependências de longo alcance de forma eficaz. Cada token pode "atender" a qualquer outro token na sequência, independentemente da distância.

* **Transfer Learning (Aprendizado por Transferência)**: O pré-treinamento em grandes conjuntos de dados não rotulados, seguido de ajuste fino em tarefas específicas, é extremamente eficaz. Isso permite que os modelos aprendam representações gerais da linguagem e as transfiram para uma ampla gama de tarefas de PNL com desempenho superior, mesmo com conjuntos de dados menores para ajuste fino.

* **Interpretability (Interpretabilidade)**: O mecanismo de atenção é inerentemente mais interpretável do que outras arquiteturas. As pontuações de atenção entre os tokens podem ser visualizadas, revelando como o modelo está "pesando" diferentes partes da entrada ao gerar uma saída. Isso contrasta com as RNNs, que "acumulam" todas as informações em um estado oculto que é difícil de decompor e entender.

* **Data Types (Tipos de Dados)**: Os Transformers são eficazes para escalar com diferentes tipos de dados que podem ser tratados como um conjunto, como imagens, áudio e até **nuvens de pontos**. Isso é possível graças a "vieses indutivos" adicionais, como os **embeddings posicionais**, que permitem ao modelo inferir a estrutura da sequência.

**Desvantagens dos Transformers:**

* **Computational Cost (Custo Computacional)**: Apesar da paralelização, os Transformers, especialmente os modelos maiores com muitos bilhões de parâmetros, são extremamente caros para treinar e implantar. O custo computacional cresce quadraticamente com o comprimento da sequência de entrada devido às operações de atenção. Isso exige grandes recursos de hardware e energia.

* **Memory Usage (Uso de Memória)**: A necessidade de armazenar as matrizes de consulta, chave e valor, bem como as matrizes de atenção, pode levar a um alto uso de memória, especialmente para sequências de entrada longas.

* **Lack of Inductive Biases (Falta de Vieses Indutivos)**: Ao contrário das RNNs que possuem um viés indutivo de processamento sequencial, os Transformers, por padrão, não têm um conhecimento intrínseco da ordem ou estrutura sequencial. Isso é mitigado pela adição de embeddings posicionais, mas pode exigir atenção cuidadosa na engenharia de características para tarefas específicas.

* **Data Requirements (Requisitos de Dados)**: Para atingir seu potencial máximo, os Transformers exigem enormes quantidades de dados para pré-treinamento, o que pode ser um desafio para domínios com dados limitados.

* **Quadratic Complexity (Complexidade Quadrática)**: A complexidade do mecanismo de atenção é quadrática em relação ao comprimento da sequência. Isso significa que, à medida que a sequência de entrada se torna mais longa, o tempo de computação e o uso de memória aumentam exponencialmente, tornando-se um gargalo para sequências muito grandes. Novas pesquisas estão explorando otimizações como a "atenção esparsa" para mitigar esse problema.