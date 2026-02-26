# 🗄️ Construindo Soluções com Bancos de Dados Vetoriais

## 🔍 Introdução aos Bancos de Dados Vetoriais

Os **Large Language Models (LLMs)** são uma tecnologia revolucionária, mas seu conhecimento é limitado ao conjunto de dados em que foram treinados. Os **bancos de dados vetoriais** são uma solução para estender arbitrariamente a base de conhecimento de um modelo, atuando como a "memória de longo prazo" para a IA generativa. Este material fornecerá uma compreensão sólida dos conceitos básicos de **busca vetorial**, seus casos de uso e como utilizar bancos de dados vetoriais para armazenar e recuperar informações.

---

## 📐 Fundamentos da Busca Vetorial

Dados como texto, imagens ou vídeos podem ser representados como um **vetor** — uma lista de números de ponto flutuante. A **busca vetorial** encontra os vetores no conjunto de dados mais próximos de um vetor de consulta usando métricas de distância.

### Métricas de Distância

**Distância Euclidiana** — mede a distância em linha reta entre dois pontos em um espaço multidimensional:

$$d(\vec{a}, \vec{b}) = \sqrt{\sum_{i=1}^{n} (a_i - b_i)^2}$$

**Similaridade de Cosseno** — mede o cosseno do ângulo entre dois vetores (1 = mesma direção, 0 = ortogonais, -1 = direções opostas):

$$\cos(\theta) = \frac{\vec{a} \cdot \vec{b}}{||\vec{a}|| \cdot ||\vec{b}||}$$

A **distância de Cosseno** é $1 - \cos(\theta)$. As duas métricas podem produzir resultados diferentes dependendo da aplicação. Com essas métricas, encontra-se os vetores mais relevantes usando a técnica **k-Nearest Neighbors (k-NN)**.

---

## 🧠 Embeddings

**Embeddings** são representações numéricas (vetores) de dados, extremamente úteis em diversas aplicações:

| Aplicação | Como Embeddings Ajudam |
|---|---|
| **Busca e Recomendação** | Retornam resultados intimamente relacionados à consulta do usuário |
| **Classificação** | Determinam o rótulo mais similar |
| **Visão Computacional** | Deduplicam dados, encontram imagens semelhantes para aprendizado ativo |
| **IA Generativa** | Encontram edge cases distantes dos dados de treinamento |

**Modelos de embedding populares:**

- **BERT** (texto): divide em tokens → embeddings por token → média = embedding de sentença
- **Fatoração de matrizes** (recomendação): gera embeddings de usuário e item
- **CLIP** (multimodal): aprende conceitos visuais via linguagem natural; gera embeddings para texto e imagens

---

## 🏛️ Bancos de Dados Vetoriais

Existem três tipos principais de ferramentas para busca vetorial:

| Tipo | Descrição | Escalabilidade | Caso de Uso |
|---|---|---|---|
| **Bibliotecas de índice vetorial** | Fornecem indexação e consulta de vetores (ex: FAISS) | Média | Protótipos e dados in-memory |
| **BDs tradicionais** | Relacionais/NoSQL com extensão vetorial (ex: pgvector) | Alta | Integração com stack existente |
| **BDs vetoriais** | Construídos especificamente para vetores de alta dimensão (ex: ChromaDB, Pinecone) | Muito alta | Produção com grandes volumes |

> 💡 **Bancos de dados vetoriais** são mais completos, escaláveis e performáticos — funcionam como um balcão único para armazenar vetores, metadados e texto bruto, sendo ideais para soluções RAG em produção.

---

## ⚡ Operações Vetoriais Avançadas

A busca vetorial em larga escala apresenta desafios quando há milhões de vetores e são necessárias respostas em milissegundos. Para isso, usam-se as técnicas de **Approximate Nearest Neighbor (ANN)** — um trade-off entre velocidade e precisão.

### Pipeline de Busca Vetorial

```
Consulta do usuário
        ↓
  [Modelo de Embedding]
        ↓
  Vetor de consulta q⃗
        ↓
  [Índice ANN no BD Vetorial]
        ↓
  Top-k vetores mais próximos
        ↓
  Documentos + metadados retornados
```

### Técnicas ANN

| Técnica | Abordagem | Exemplo Popular |
|---|---|---|
| **Baseada em Hash** | Mapeia vetores para espaço de dimensão inferior via hash | LSH (Locality-Sensitive Hashing) |
| **Baseada em Árvore** | Particiona o espaço vetorial em estrutura de árvore | KD-Tree, Ball-Tree |
| **Baseada em Partição (Clustering)** | Agrupa em clusters; busca apenas nos mais relevantes | **IVF** (Inverted File Index) |
| **Baseada em Grafo** | Grafo multicamadas onde nós = vetores e arestas = proximidade | **HNSW** (Hierarchical Navigable Small World) |

**Quantização** reduz o tamanho dos vetores armazenados (comprime em detrimento de precisão). A **quantização de produto** divide vetores em subvetores e quantiza cada um independentemente — ajustando o número de clusters ou subvetores, calibra-se o equilíbrio entre precisão e desempenho.

---

## 🎬 Aplicações de Busca Vetorial

A busca vetorial é crucial para a IA generativa, mas também possui muitas outras aplicações. Um exemplo clássico é um **recomendador de filmes** — filmes assistidos são usados como vetor de consulta para encontrar títulos semelhantes por similaridade semântica, não apenas por correspondências exatas de palavras-chave.

---

## 🖥️ Gradio para Interfaces de Usuário

**Gradio** é uma ferramenta que permite criar rapidamente interfaces de usuário interativas para modelos de aprendizado de máquina. No contexto de busca vetorial, Gradio pode construir um **chatbot de IA** que interaja com os resultados de busca vetorial — facilitando a visualização de resultados de busca multimodal em tempo real. Isso agiliza a experimentação e demonstração de aplicações de IA, tornando-as acessíveis mesmo sem conhecimento profundo de programação.

---

## 🎯 Key Takeaways

- **Bancos de dados vetoriais** são a "memória de longo prazo" dos LLMs — permitem estender o conhecimento do modelo com dados externos via RAG.
- Dados são representados como vetores (embeddings) e a busca usa métricas de distância: **Euclidiana** $d = \sqrt{\sum(a_i - b_i)^2}$ para distância absoluta e **Cosseno** $\cos(\theta) = \frac{\vec{a} \cdot \vec{b}}{||\vec{a}|| \cdot ||\vec{b}||}$ para similaridade semântica.
- **k-NN** encontra os vetores mais próximos; **ANN** (IVF, HNSW) troca precisão por velocidade em escala de milhões de vetores.
- Use **bancos de dados vetoriais** (ChromaDB, Pinecone) em produção — mais escaláveis e completos que bibliotecas de índice ou BDs tradicionais.
- **Gradio** acelera a prototipagem de interfaces para aplicações de busca vetorial e RAG.

---

[← Introdução ao Desenvolvimento de Aplicações Generativas](1_Introduction_to_Building_Generative_Apps.md) · [Desenvolvendo Soluções de IA Generativa com LangChain →](3_Developing%20Generative_AI_Solutions_with_LangChain.md)