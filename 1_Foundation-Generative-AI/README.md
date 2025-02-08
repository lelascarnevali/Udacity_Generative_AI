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

## Apply Lightweight Fine-Tuning to a Foundation Model

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


**Solution**

Project 1 - [Notebook](LightweightFineTuning.ipynb)