# Modelos de Fundação

## 🏗️ O que é um Modelo de Fundação?

Um **modelo de fundação** é um tipo de modelo de inteligência artificial treinado em uma vasta quantidade de dados em escala, possuindo a capacidade de realizar uma ampla gama de tarefas com o mínimo de treinamento adicional. Eles são "fundacionais" porque servem como base para inúmeras aplicações, similar a como uma fundação suporta diversas estruturas arquitetônicas.

$$\text{Foundation Model} = \text{Vasto Pré-Treinamento} + \text{Transfer Learning} + \text{Fine-Tuning Mínimo}$$

---

## ⚖️ Modelos de Fundação vs. Modelos Tradicionais

| Aspecto | Modelos Tradicionais | Modelos de Fundação |
|---|---|---|
| **Dados de Treino** | Curados, específicos para a tarefa | Vastos e gerais (ex: Wikipedia, Common Crawl) |
| **Versatilidade** | Altamente eficaz para a tarefa alvo | Propósito geral, adapta-se a muitas tarefas |
| **Generalização** | Ineficaz fora do escopo original | Transfer Learning entre domínios |
| **Exemplos** | Regressão linear, árvores de decisão | GPT-3, BERT, Stable Diffusion |
| **Recursos** | Menor custo computacional | Alto custo de treinamento; reutilizável depois |

---

## ⚡ Arquitetura e Escala

A arquitetura dos modelos de fundação baseados em texto frequentemente se baseia na **arquitetura Transformer**. O conceito central é o **mecanismo de autoatenção**, que permite ao modelo ponderar a importância de diferentes partes da sequência de entrada.

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Onde $Q$ (Query), $K$ (Key) e $V$ (Value) são matrizes derivadas da entrada, e $d_k$ é a dimensão das chaves.

```mermaid
graph LR
  A[📝 Texto de Entrada] --> B[Embeddings]
  B --> C[Multi-Head Attention]
  C --> D[Feed-Forward]
  D --> E[Normalização]
  E --> F[🎯 Saída / Previsão]
```

Além da arquitetura, os modelos de fundação se distinguem pelo seu grande número de **parâmetros** — dos milhões iniciais aos bilhões e trilhões nos modelos atuais.

---

## 📧 Exemplo: Classificador de Spam com Foundation Model

Modelos de fundação, especialmente os LLMs comerciais, permitem a prototipagem rápida de novas aplicações. Para um classificador de spam:

```python
from transformers import pipeline

# Classifica e-mails como spam ou não usando um foundation model
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

def classify_email(email_text: str) -> str:
    """Classifica um e-mail usando um foundation model."""
    result = classifier(email_text[:512])[0]  # Limita ao tamanho máximo
    return f"{'SPAM' if result['label'] == 'NEGATIVE' else 'LEGIT'} ({result['score']:.1%})"

print(classify_email("Congratulations! You won $1,000,000. Click here now!"))
# SPAM (99.2%)
```

> 💡 **Insight:** Foundation models minimizam a necessidade de grandes conjuntos de dados de treinamento específicos para cada nova aplicação.

---

## 📊 Benchmarks e o GLUE

Conjuntos de dados de **benchmark** padronizam a avaliação de modelos, fomentam competição saudável e permitem reprodutibilidade científica.

#### O Benchmark GLUE

| Tarefa | Descrição | Tipo |
|---|---|---|
| **CoLA** | Aceitabilidade gramatical de uma frase | Classificação |
| **MNLI** | Relação entre dois textos (entailment/contradição) | Inferência |
| **MRPC** | Identifica se duas frases são paráfrases | Similaridade |
| **QNLI** | A frase contém a resposta para a pergunta? | Inferência |
| **RTE** | Hipótese é verdadeira/falsa dado uma premissa? | Entailment |
| **WNLI** | Resolução de correferente de pronomes | Compreensão |

---

## 💾 Dados de Treinamento e Escala dos LLMs

**Large Language Models (LLMs)** são treinados em um corpus de dados vasto e diversificado. A qualidade e diversidade dos dados são cruciais para que o modelo aprenda padrões, estruturas gramaticais, semântica e nuances contextuais da linguagem.

| Fonte de Dados | Exemplos |
|---|---|
| **Sites** | Artigos, blogs, fóruns (ex: Common Crawl — 25B+ páginas) |
| **Livros** | Ficção, não ficção, acadêmicos, técnicos |
| **Notícias** | Jornais e portais de notícias |
| **Publicações Científicas** | Linguagem especializada, conceitos complexos |
| **Mídias Sociais** | Linguagem informal, gírias, tendências |
| **Documentos Legais** | Contratos, processos judiciais, legislação |
| **Textos Multilíngues** | Múltiplos idiomas (embora predominantemente inglês) |

> 💡 **Escala:** Centenas de gigabytes a terabytes de texto (1 GB ≈ 1.000 livros). Fontes como **Common Crawl**, **Wikipedia** e artigos científicos formam a base. Quanto maior e mais diverso o corpus, maior a capacidade de generalização e coerência na geração de linguagem natural.

---

## ⚠️ Riscos: Viés, Desinformação e Impacto Ambiental

> 🔴 **Viés nos Dados:** Modelos treinados em dados com preconceitos históricos perpetuam e amplificam esses preconceitos. Diversifique fontes e monitore outputs continuamente.

> 🔴 **Alucinação:** Foundation models podem gerar informações falsas mas plausíveis. Não use LLMs como fonte primária de fatos verificados.

> 🔴 **Impacto Ambiental:** Treinar um único foundation model pode consumir energia equivalente a anos de consumo residencial. Use modelos pré-treinados e PEFT para reduzir pegada de carbono.

Medidas proativas:
* **Marca d'água** — Identificar conteúdo gerado por IA
* **Detecção de Deepfakes** — Tecnologias para identificar manipulações
* **Educação** — Letramento digital sobre capacidades e limitações da IA

---

## 🎯 Key Takeaways

| Conceito | Resumo |
|---|---|
| **Foundation Model** | Treinado em dados vastos; adapta-se a muitas tarefas com fine-tuning mínimo |
| **Transformer** | Arquitetura base; mecanismo de Attention: $\text{softmax}(QK^T/\sqrt{d_k})V$ |
| **Escala** | Bilhões de parâmetros = maior generalização, maior custo |
| **GLUE Benchmark** | 6 tarefas padronizadas para avaliar compreensão de linguagem |
| **Viés** | Dado ruim = modelo enviesado. Diversifique e monitore |
| **Alucinação** | LLMs inventam fatos — valide outputs críticos |

> 🏁 **Regra de Ouro:** Foundation models são generalistas poderosos, mas requerem adaptação e curadoria cuidadosas para aplicações críticas.

---

[← Fundamentos de Deep Learning](2_Deep_Learning_Fundamentals.md) · [Adaptando Modelos de Fundação →](4_Adapting_Foundation_Models.md)