"""
Sentiment Analysis on Rotten Tomatoes Reviews using PEFT with GPT-2

This script demonstrates efficient fine-tuning of GPT-2 for binary sentiment classification
using Parameter-Efficient Fine-Tuning (PEFT) techniques like LoRA.
"""

# Configuration Management
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

# Environment Setup
import os
import logging
from typing import Dict, Tuple, List
import numpy as np
import pandas as pd
import torch
from datasets import load_dataset, DatasetDict, concatenate_datasets
from sklearn.metrics import (
    accuracy_score, f1_score, 
    precision_score, recall_score, 
    classification_report
)
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    DataCollatorWithPadding, Trainer, TrainingArguments,
    set_seed
)
from peft import LoraConfig, get_peft_model, AutoPeftModelForSequenceClassification

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('experiment.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Set all seeds for reproducibility
set_seed(config.getint('TRAINING', 'SEED', fallback=42))

# Constants
MODEL_NAME = config.get('MODEL', 'NAME', fallback='gpt2')
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {DEVICE}")

class SentimentAnalysisPipeline:
    """End-to-end pipeline for sentiment analysis with PEFT"""
    
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.dataset = None
        self.data_collator = None

    def load_data(self) -> DatasetDict:
        """Load and validate dataset splits"""
        try:
            self.dataset = load_dataset("rotten_tomatoes")
            assert all(split in self.dataset for split in ['train', 'validation', 'test'])
            logger.info("Dataset loaded successfully")
            return self.dataset
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            raise

    def analyze_class_distribution(self) -> None:
        """Analyze and log class distributions for all splits"""
        for split in ['train', 'validation', 'test']:
            labels = self.dataset[split]['label']
            class_counts = np.bincount(labels)
            logger.info(
                f"{split.capitalize()} Set Distribution:\n"
                f"Negative: {class_counts[0]} ({class_counts[0]/len(labels):.2%})\n"
                f"Positive: {class_counts[1]} ({class_counts[1]/len(labels):.2%})"
            )

    def initialize_model(self) -> None:
        """Initialize model with proper configuration"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            self.tokenizer.pad_token = self.tokenizer.eos_token

            self.model = AutoModelForSequenceClassification.from_pretrained(
                MODEL_NAME,
                num_labels=2,
                id2label={0: "NEGATIVE", 1: "POSITIVE"},
                label2id={"NEGATIVE": 0, "POSITIVE": 1}
            ).to(DEVICE)
            
            logger.info(f"Model {MODEL_NAME} initialized successfully")
        except Exception as e:
            logger.error(f"Model initialization failed: {str(e)}")
            raise

    def tokenize_data(self) -> None:
        """Tokenize dataset with proper preprocessing"""
        def tokenize_fn(examples: Dict) -> Dict:
            return self.tokenizer(
                examples["text"],
                truncation=True,
                max_length=config.getint('PROCESSING', 'MAX_LENGTH', fallback=128),
                padding=False  # Dynamic padding later
            )
        
        self.dataset = self.dataset.map(
            tokenize_fn,
            batched=True,
            remove_columns=['text'],
            desc="Tokenizing dataset"
        )

        self.data_collator = DataCollatorWithPadding(
            tokenizer=self.tokenizer,
            padding='longest',
            pad_to_multiple_of=8
        )

    def configure_peft(self) -> None:
        """Apply PEFT configuration to model"""
        peft_config = LoraConfig(
            task_type="SEQ_CLS",
            r=config.getint('PEFT', 'R', fallback=8),
            lora_alpha=config.getint('PEFT', 'ALPHA', fallback=64),
            lora_dropout=config.getfloat('PEFT', 'DROPOUT', fallback=0.1),
            target_modules=['c_attn', 'c_proj'],
            bias="none"
        )
        
        self.model = get_peft_model(self.model, peft_config)
        self.model.print_trainable_parameters()
        
        # Freeze base model parameters
        for param in self.model.base_model.parameters():
            param.requires_grad = False

    def train(self) -> Trainer:
        """Execute training pipeline"""
        training_args = TrainingArguments(
            output_dir=config.get('PATHS', 'OUTPUT_DIR', fallback='./results'),
            learning_rate=config.getfloat('TRAINING', 'LR', fallback=3e-4),
            per_device_train_batch_size=config.getint('TRAINING', 'BATCH_SIZE', fallback=16),
            per_device_eval_batch_size=config.getint('TRAINING', 'BATCH_SIZE', fallback=16),
            evaluation_strategy="epoch",
            num_train_epochs=config.getint('TRAINING', 'EPOCHS', fallback=3),
            logging_steps=10,
            save_strategy="epoch",
            load_best_model_at_end=True,
            report_to="none",
            optim="adamw_torch",
            seed=config.getint('TRAINING', 'SEED', fallback=42)
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.dataset["train"],
            eval_dataset=concatenate_datasets([self.dataset["validation"], self.dataset["test"]]),
            data_collator=self.data_collator,
            compute_metrics=self._compute_metrics
        )

        logger.info("Starting training...")
        trainer.train()
        return trainer

    def _compute_metrics(self, eval_pred: Tuple) -> Dict:
        """Compute comprehensive evaluation metrics"""
        preds, labels = eval_pred
        preds = np.argmax(preds, axis=1)
        
        return {
            "accuracy": accuracy_score(labels, preds),
            "f1_macro": f1_score(labels, preds, average="macro"),
            "f1_binary": f1_score(labels, preds, average="binary"),
            "precision": precision_score(labels, preds, average="macro"),
            "recall": recall_score(labels, preds, average="macro"),
            "report": classification_report(labels, preds, output_dict=True)
        }

    def evaluate(self, trainer: Trainer) -> Dict:
        """Perform comprehensive model evaluation"""
        logger.info("Evaluating model...")
        metrics = trainer.evaluate()
        logger.info("\nEvaluation Results:")
        for k, v in metrics.items():
            if k != "report":
                logger.info(f"{k}: {v:.4f}")
        return metrics

    def save_model(self, path: str = "./model") -> None:
        """Save model and tokenizer with proper checks"""
        if not os.path.exists(path):
            os.makedirs(path)
            
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        logger.info(f"Model saved to {path}")

    @staticmethod
    def load_model(path: str = "./model") -> Tuple:
        """Load saved model and tokenizer"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model directory {path} not found")
            
        model = AutoPeftModelForSequenceClassification.from_pretrained(path).to(DEVICE)
        tokenizer = AutoTokenizer.from_pretrained(path)
        return model, tokenizer

if __name__ == "__main__":
    # Initialize pipeline
    pipeline = SentimentAnalysisPipeline()
    
    try:
        # Data loading and preparation
        pipeline.load_data()
        pipeline.analyze_class_distribution()
        pipeline.initialize_model()
        pipeline.tokenize_data()
        
        # Model training
        pipeline.configure_peft()
        trainer = pipeline.train()
        pipeline.evaluate(trainer)
        pipeline.save_model()
        
        # Example inference
        model, tokenizer = pipeline.load_model()
        sample_text = "A visually stunning but narratively weak production"
        inputs = tokenizer(sample_text, return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits).item()
        logger.info(f"Prediction for '{sample_text}': {model.config.id2label[prediction]}")
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        raise