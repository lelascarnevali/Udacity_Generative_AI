# Udacity Project - Foundation Generative AI

## Apply Lightweight Fine-Tuning to a Foundation Model

### Project Introduction
Lightweight fine-tuning is one of the most important techniques for adapting foundation models, because it allows you to modify foundation models for your needs without needing substantial computational resources.

In this project, I will apply **parameter-efficient fine-tuning** using the Hugging Face `peft` library.
<br> 
### Project Summary
In this project, I will bring together all of the essential components of a PyTorch + Hugging Face training and inference process. Specifically, I will:

1. Load a pre-trained model and evaluate its performance
2. Perform parameter-efficient fine tuning using the pre-trained model
3. Perform inference using the fine-tuned model and compare its performance to the original model
</br>

## Project evaluation key points

### Prepare the Foundation Model

1. Load a pretrained HF model: Includes the relevant imports and loads a pretrained Hugging Face model that can be used for sequence classification.
2. Load and preprocess a dataset: Includes the relevant imports and loads a Hugging Face dataset that can be used for sequence classification. Then includes relevant imports and loads a Hugging Face tokenizer that can be used to prepare the dataset. A subset of the full dataset may be used to reduce computational resources needed.
3. Evaluate the pretrained model: At least one classification metric is calculated using the dataset and pretrained model.

### Perform Lightweight Fine-Tuning

1. Create a PEFT model: Includes the relevant imports, initializes a Hugging Face PEFT config, and creates a PEFT model using that config.
2. Train the PEFT model: The model is trained for at least one epoch using the PEFT model and dataset.
3. Save the PEFT model: Fine-tuned parameters are saved to a separate directory. The saved weights directory should be in the same home directory as the notebook file.

### Perform Inference Using the Fine-Tuned Model

1. Load the saved PEFT model: Includes the relevant imports then loads the saved PEFT model
2. Evaluate the fine-tuned model: Repeats the earlier evaluation process (same metric(s) and dataset) to compare the fine-tuned version to the original version of the model.


## Solution

Project 1 - [Notebook](LightweightFineTuning.ipynb)

### Prerequisites

Before using the script, make sure you have the required dependencies installed:

```bash
pip install torch transformers peft
```

Additionally, ensure that you have a trained model stored in `./model/gpt2-rotten-tomatoes-lora` or update the `model_path` in the script accordingly.

### Running the Script
You can run the script from the command line with a single text input or a file containing multiple texts.

#### 1. Predict Sentiment of a Single Text
```bash
python SentimentAnalyzer.py --text "This movie was fantastic!"
```

Example Output:
```
Resultado da Predição:
Texto: This movie was fantastic!
Predição: POSITIVE
Confiança: 98.34%
Probabilidades:
- NEGATIVE: 1.66%
- POSITIVE: 98.34%
```

#### 2. Predict Sentiment from a File
```bash
python SentimentAnalyzer.py --file reviews.txt
```
Each line in `reviews.txt` should contain one review. The script will output predictions for each line.

### Fine-Tuning Process

This script is part of the **Udacity Generative AI Foundation** project. The fine-tuning process involved:

1. **Loading a Pretrained Model**: GPT-2 model for sequence classification.
2. **Preparing Dataset**: Rotten Tomatoes dataset for sentiment analysis.
3. **Fine-Tuning with PEFT**: Used LoRA (Low-Rank Adaptation) for efficient training.
4. **Evaluating Performance**: Compared fine-tuned model vs. original model.