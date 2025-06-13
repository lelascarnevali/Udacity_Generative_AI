### 1. Modelos de Difusão: A Base da IA Generativa Moderna

Modelos de difusão são uma tecnologia essencial na **Inteligência Artificial Generativa** (IA Generativa), utilizada para a criação de diversas mídias, como imagens, vídeos e áudios. A sua funcionalidade é centrada em um processo de duas fases: a fase direta (forward) e a fase reversa (backward).

1.  **Fase Direta (Forward):** Começa com uma imagem original e adiciona-se ruído progressivamente até que a imagem se torne puro ruído aleatório. É uma transformação gradual de dados estruturados para aleatoriedade, simulando o processo físico de difusão onde moléculas se espalham e se misturam.

2.  **Fase Reversa (Backward):** Inversamente, parte-se do ruído e realiza-se um processo de denoising (remoção de ruído) gradativo até que uma imagem realista seja reconstruída. Essa fase reverte o caos introduzido na fase direta, restaurando uma estrutura coerente a partir do ruído. A necessidade de muitos pequenos passos na fase reversa é crucial, pois é mais fácil aprimorar uma imagem com ruído leve do que reconstruir uma imagem clara a partir de um ruído puro. Isso permite que o modelo seja treinado para fazer transições progressivas de estados ruidosos para menos ruidosos.

A geração de novas imagens ocorre a partir de um ruído aleatório, com o modelo sendo usado iterativamente para remover esse ruído. Inicialmente, o modelo "inventa" bastante, pois lida com ruído puro. Contudo, à medida que o processo avança (do tempo T ao tempo 0), uma imagem começa a surgir, e o modelo adiciona detalhes mais finos até que a imagem final e realista seja alcançada.

---
### 2. Condicionamento e Condicionamento por Texto

Inicialmente, os modelos de difusão operavam de forma **incondicional**, gerando imagens sem orientação específica. Eles podiam produzir qualquer imagem com base em seu conjunto de dados de treinamento, mas não conseguiam gerar imagens baseadas em instruções específicas (por exemplo, um tipo específico de carro).

Atualmente, existem diversas formas de **condicionar** um modelo de difusão:

1.  **Condicionamento de Esboço para Imagem:** O modelo é condicionado por um esboço fornecido pelo usuário, que serve de base para gerar uma imagem detalhada e realista.

2.  **Condicionamento de Imagem para Imagem:** Inicia-se com uma imagem existente e o modelo gera variações dela, como uma versão futurista do mesmo objeto.

3.  **Condicionamento de Estilo:** O modelo gera uma imagem de algo com base em um estilo específico, que é exemplificado por uma imagem de entrada (por exemplo, uma imagem de carro no estilo de Van Gogh).

A forma de condicionamento mais comum e transformadora é o **condicionamento por texto**. Este permite guiar a geração de imagens através de descrições textuais.

1.  **Como o Condicionamento por Texto Funciona:**
    a.  **Embeddings de Modelos de Linguagem:** O texto é convertido em um vetor numérico (embedding) usando um modelo de linguagem pré-treinado, o que ajuda a IA a compreender e representar o significado do texto.
    b.  **Integração em Modelos de Difusão:** Durante o treinamento, esses embeddings são injetados no modelo de difusão em diversos pontos, utilizando **cross-attention**. Isso garante que a imagem gerada esteja alinhada com a intenção do texto.
    c.  **Classificador-Free Guidance:** Uma abordagem inovadora usada na fase de inferência que amplifica a importância do prompt de texto, garantindo que a imagem final se adeque mais fielmente à descrição textual. Isso é feito comparando a geração condicional (com texto) e incondicional (sem texto) usando a mesma entrada de ruído e amplificando a direção influenciada pelo texto.

O condicionamento, especialmente por texto, é um avanço significativo no campo da IA generativa de imagens, permitindo uma criação de conteúdo mais controlada, precisa e relevante para as solicitações dos usuários.

---
### 3. Modelos de Difusão Latente (LDMs)

Modelos de Difusão Latente (LDMs) representam uma evolução dos modelos de difusão tradicionais, superando as limitações computacionais dos modelos que operam no nível do pixel. O **Stable Diffusion** é um exemplo proeminente de LDM.

1.  **Limitações dos Modelos Nível-Pixel:** Modelos de difusão que operam diretamente no nível do pixel são computacionalmente intensivos, exigindo recursos substanciais, especialmente para imagens de alta resolução (por exemplo, uma imagem de 512x512 pixels envolve mais de 260.000 números).

2.  **Como os Modelos de Difusão Latente Funcionam:**
    a.  **Autoencoders e Espaço Latente:** LDMs utilizam **autoencoders**, que consistem em um **encoder** (compressor) e um **decoder** (descompressor). O encoder comprime uma imagem em um **vetor latente** (ou embedding), uma representação muito menor do conteúdo da imagem. O decoder inverte o processo, expandindo o vetor latente de volta para uma imagem.
    b.  **Processo de Difusão no Espaço Latente:** O processo de difusão nesses modelos adiciona ruído ao vetor latente em várias etapas até que ele esteja totalmente aleatório. O modelo é então treinado para **denoisar** esses vetores de volta à sua forma original. Como o espaço latente é consideravelmente menor do que o tamanho total da imagem, o modelo exige significativamente menos poder computacional.
    c.  **Implicações Práticas:** A operação no espaço latente permite que os LDMs funcionem mais rapidamente e até mesmo em hardware de consumo, tornando-os mais acessíveis. Por exemplo, a representação latente no Stable Diffusion pode ser de apenas cerca de 16.000 números, em comparação com os mais de 260.000 pixels de uma imagem 512x512, reduzindo drasticamente a carga computacional.

LDMs são revolucionários por sua capacidade de gerar conteúdo de alta qualidade com menor consumo de recursos, ampliando as possibilidades de aplicação em diversas áreas, desde a criação artística até soluções de design.

---
### 4. Vantagens e Desvantagens dos Modelos de Difusão

Os modelos de difusão se destacam no campo da IA generativa, mas também apresentam desafios:

1.  **Vantagens:**
    * **Grande Diversidade de Amostras:** Geram uma ampla gama de imagens criativas e originais, cobrindo diversos aspectos do dataset de treinamento.
    * **Amostras de Alta Qualidade:** Produzem imagens fotorrealistas e convincentes, e podem ser executados em hardware de consumo.
    * **Facilidade de Condicionamento:** Oferecem uma forma natural de condicionar a saída de várias maneiras (texto-para-imagem, imagem-para-imagem, áudio-para-imagem, e até mesmo design de moléculas), demonstrando sua versatilidade.

2.  **Desvantagens:**
    * **Velocidade:** Requerem múltiplas passagens diretas (dezenas ou centenas) para cada etapa do processo de denoising, tornando-os mais lentos em comparação com outros modelos generativos como as GANs (Redes Adversariais Generativas), que exigem apenas uma chamada à sua rede neural.

3.  **Análise Comparativa com Outros Modelos:**
    * **GANs (Generative Adversarial Networks):** Enquanto as GANs são muito mais rápidas, os modelos de difusão oferecem a mesma qualidade de amostras e maior diversidade.
    * **VAEs (Variational Autoencoders) e Normalizing Flows:** Modelos de difusão superam esses em termos de qualidade de amostra, mas são mais lentos na velocidade de amostragem.

A pesquisa contínua visa melhorar a velocidade dos modelos de difusão, que, apesar de sua desvantagem em velocidade, são ferramentas poderosas na IA generativa devido à sua versatilidade e à alta qualidade de suas saídas.

---
### 5. Implementação de DDPMs (Denoising Diffusion Probabilistic Models)

A implementação de DDPMs envolve detalhes específicos sobre o processo de adição de ruído (fase direta) e denoising (fase reversa).

1.  **Compreendendo o Agendamento de Ruído (Noise Schedule):**
    a.  **Adição de Ruído:** O agendamento de ruído é fundamental na fase direta, ditando a adição gradual de ruído aos dados. O ruído é adicionado seguindo uma **Distribuição Normal**, parametrizada por `β` (beta). `β` é um número positivo entre 0 e 1 que aumenta ao longo dos passos de tempo (por exemplo, linearmente). O ruído é amostrado de uma distribuição Gaussiana cuja média e variância dependem de `β`.
    b.  **Fórmula Matemática:** Para um intervalo de tempo `t`, adiciona-se a cada pixel `i` da imagem um número amostrado de uma distribuição Gaussiana com média `(1 - β_t) * x^(t-1)_i` e variância `β * I`. À medida que `t` avança, a média da Gaussiana diminui e a variância aumenta.

2.  **Processamento Sequencial vs. Paralelo:**
    a.  **Superando a Dependência Sequencial:** Uma implementação ingênua do processo direto seria sequencial, onde o pixel no tempo `t` depende de seu valor no tempo `t-1`. Isso exigiria `t` passos sequenciais para gerar a imagem ruidosa no tempo `t`.
    b.  **Solução de Processamento Paralelo:** Isso é resolvido através de uma **reparametrização** usando `α_bar_t = Produto(1 - β_t)` e observando que um produto de Gaussianas ainda é uma Gaussiana. Essa abordagem faz com que a imagem no passo `t` dependa do ponto de dados original no tempo `t=0` (em vez do passo anterior `t-1`), o que é crucial para o processamento paralelo e para o funcionamento da função de perda. O ruído adicionado a um pixel no tempo `t` é então retirado de uma distribuição Gaussiana com média `sqrt(α_bar_t) * x_0` e variância `(1 - α_bar_t) * I`.

3.  **Função de Perda e Expectativa:**
    a.  **Função de Perda:** Ao treinar DDPMs, compara-se o ruído `ϵ` adicionado durante a fase direta no passo `t` com o ruído `ϵ_θ` previsto pelo modelo na fase reversa no mesmo `t`. O objetivo é minimizar a **expectativa** do erro quadrático médio: `E[||ϵ - ϵ_θ||^2]`. Isso significa que, em média, a diferença entre o ruído verdadeiro e o ruído previsto deve diminuir à medida que o modelo melhora. Na prática, a expectativa é aproximada pela média do erro quadrático médio (MSE) `||ϵ - ϵ_θ||^2` sobre um mini-batch de várias imagens `x_0`, onde um passo de tempo `t` aleatório é escolhido para cada imagem.

    b.  **Código do Processo Direto e Treinamento:**
    ```python
    n_steps = 512 # Isso é chamado de T nas fórmulas
    # Linear noise schedule
    beta = linspace(start, end, n_steps)

    # Precomputa algumas quantidades para a reparametrização
    alpha = 1. - beta
    alpha_bar = cumprod(alpha, axis=0)

    sqrt_alpha_bar = sqrt(alpha_bar)
    sqrt_one_minus_alpha_bar = sqrt(1. - alpha_bar)

    model = UNet()
    optimizer = Adam(model.parameters(), lr=0.001)

    for batch, _ in dataloader:
        # move batch para GPU, reset otimizadores, então:
        bs = batch.shape[0]
        # Passos de tempo aleatórios, um para cada imagem no
        # mini-batch
        t = torch.randint(0, T, (bs,)).long()

        # Gera ruído e adiciona às imagens
        # (passagem direta)
        noise = torch.randn_like(batch, device=device)
        x_noisy = (
            sqrt_alpha_bar[t].view(bs, 1, 1, 1) * batch +
            sqrt_one_minus_alpha_bar[t].view(bs, 1, 1, 1) * noise
        )

        # Preve o ruído usando o modelo
        # NOTA como o modelo recebe como entrada a imagem ruidosa
        # E o passo de tempo t
        noise_pred = model(x_noisy, t)

        # Aproxima a expectativa pela média
        # da perda MSE sobre o minibatch e os passos de tempo
        # aleatórios
        loss = F.mse_loss(noise, noise_pred)

        # Calcula gradientes e otimiza os pesos do modelo
        loss.backward()
        optimizer.step()
    ```

---
### 6. Denoising com Arquitetura UNet e Inferência

A arquitetura **UNet** é adaptada para DDPMs para prever o ruído a ser subtraído em cada passo de tempo, gradualmente denoisando a imagem.

1.  **Função da UNet:** A UNet recebe como entrada a imagem no tempo `t` e o valor de `t`, e produz o ruído previsto.
2.  **Embeddings Temporais:** **Embeddings temporais** informam a UNet sobre o intervalo de tempo atual. Codificações posicionais para cada passo de tempo são processadas através de uma camada linear e uma função de ativação, garantindo que o modelo esteja ciente do tempo.
3.  **Pesos Compartilhados ao Longo do Tempo:** A UNet usa o mesmo conjunto de pesos em todos os intervalos de tempo, um aspecto crucial de sua arquitetura.

No processo de **inferência** (geração de imagens):

1.  **Amostragem e Geração:** O modelo começa com ruído puro e aplica o processo de denoising aprendido em ordem inversa (do tempo `T` ao `t=0`). Em cada passo, o ruído previsto pelo modelo é subtraído da melhor estimativa atual da imagem, renormalizado adequadamente. Um termo de ruído adicional (`σ_t * z`) é adicionado, o que, embora contraintuitivo, promove a diversidade nas amostras e reduz a correlação entre cada passo de tempo, evitando o acúmulo de erros. Este novo termo de ruído `σ_t` é grande no início da amostragem (tempo `T`) e diminui à medida que se aproxima de `t=0`. Isso encoraja o modelo a focar na estrutura geral da imagem no início do denoising e nos detalhes mais finos no final.

2.  **Código da Inferência:**
    ```python
    # Computa algumas quantidades necessárias, contidas
    # nas fórmulas reportadas acima
    sqrt_one_minus_alpha_bar = sqrt(1. - alpha_bar)
    alpha_bar_t_minus_1 = F.pad(
        alpha_bar[:-1],
        (1, 0),
        value=1.0
    )
    # Isso é chamado \sigma_{t} nas fórmulas
    # posterior_variance = (
    # beta * (1.0 - alpha_bar_t_minus_1) /
    # (1.0 - alpha_bar)
    # )
    # Tamanho do batch. Por exemplo, gerar 8
    # imagens falsas
    bs = 8
    # Gera a inicialização aleatória
    # (lembre-se, uma imagem preenchida com valores aleatórios
    # é o início do processo reverso)
    x = randn((bs, 3, IMG_SIZE, IMG_SIZE))
    # Percorremos "para trás no tempo"
    for ts in range(0, T)[::-1]:

        # Este é o ruído z que adicionaremos de volta
        # à imagem denoisada (exceto se estivermos
        # na última iteração)
        noise = randn_like(x) if ts > 0 else 0

        # Para cada imagem no batch, consideramos
        # o passo de tempo ts
        t = full((bs,), ts).long()

        # Esta é a fórmula para o denoising
        x = (
            sqrt_one_over_alpha[t].view(bs, 1, 1, 1) *
            (
            # Lembre-se: alpha[t] = 1 - beta[t]
            x - beta[t].view(bs, 1, 1, 1)
            /
            sqrt_one_minus_alpha_bar[t].view(bs, 1, 1, 1) *
            model(x, t)
            ) + sqrt(posterior_variance[t].view(bs, 1, 1, 1)) *
            noise
    # Corta qualquer valor abaixo de -1 ou acima de 1
    # (isso é necessário para que a conversão de volta para
    # imagem RGB funcione bem)
    generated_image = torch.clamp(x, -1, 1)
    ```

A biblioteca Hugging Face Diffusers é uma ferramenta poderosa para testar e experimentar a geração de IA generativa, incluindo vídeos e outras capacidades de visão computacional.