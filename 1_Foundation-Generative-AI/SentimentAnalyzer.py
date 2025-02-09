"""
Script de Inferência para Análise de Sentimento com Modelo PEFT
"""

import torch
from peft import AutoPeftModelForSequenceClassification
from transformers import AutoTokenizer
import logging
from typing import List, Dict

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class SentimentClassifier:
    def __init__(self, model_path: str = "./model/gpt2-rotten-tomatoes-lora"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.tokenizer = self._load_model(model_path)
        self.label_map = {0: "NEGATIVE", 1: "POSITIVE"}
        
    def _load_model(self, model_path: str):
        """Carrega o modelo e tokenizer salvos"""
        try:
            logger.info(f"Carregando modelo de {model_path}")
            
            model = AutoPeftModelForSequenceClassification.from_pretrained(
                model_path
            ).to(self.device).eval()

            tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            logger.info("Modelo carregado com sucesso")
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {str(e)}")
            raise

    def preprocess_text(self, text: str) -> Dict[str, torch.Tensor]:
        """Preprocessa o texto para entrada do modelo"""
        return self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=128,
            return_tensors="pt"
        )

    def predict(self, text: str) -> Dict:
        """Faz a predição para um único texto"""
        try:
            inputs = self.preprocess_text(text)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self.model(**inputs)

            probabilities = torch.softmax(outputs.logits, dim=-1)
            prediction = torch.argmax(probabilities).item()
            
            return {
                "text": text,
                "prediction": self.label_map[prediction],
                "confidence": probabilities[0][prediction].item(),
                "probabilities": {
                    "NEGATIVE": probabilities[0][0].item(),
                    "POSITIVE": probabilities[0][1].item()
                }
            }
            
        except Exception as e:
            logger.error(f"Erro na predição: {str(e)}")
            return {"error": str(e)}

    def batch_predict(self, texts: List[str]) -> List[Dict]:
        """Faz predições para múltiplos textos de uma vez"""
        return [self.predict(text) for text in texts]

if __name__ == "__main__":
    import argparse
    
    # Configuração do parser de argumentos
    parser = argparse.ArgumentParser(description="Classificador de Sentimento")
    parser.add_argument("--text", type=str, help="Texto para classificação")
    parser.add_argument("--file", type=str, help="Arquivo com textos (um por linha)")
    args = parser.parse_args()

    # Inicializar classificador
    classifier = SentimentClassifier()
    
    # Processar entradas
    if args.text:
        result = classifier.predict(args.text)
        print("\nResultado da Predição:")
        print(f"Texto: {result['text']}")
        print(f"Predição: {result['prediction']}")
        print(f"Confiança: {result['confidence']:.2%}")
        print(f"Probabilidades:")
        print(f"- NEGATIVE: {result['probabilities']['NEGATIVE']:.2%}")
        print(f"- POSITIVE: {result['probabilities']['POSITIVE']:.2%}")
        
    elif args.file:
        with open(args.file, 'r') as f:
            texts = [line.strip() for line in f.readlines() if line.strip()]
            
        results = classifier.batch_predict(texts)
        print("\nResultados em Lote:")
        for i, result in enumerate(results, 1):
            print(f"\nExemplo {i}:")
            print(f"Texto: {result['text']}")
            print(f"Predição: {result['prediction']}")
            print(f"Confiança: {result['confidence']:.2%}")
            
    else:
        print("Modo de uso:")
        print("Para texto único: python script.py --text 'seu texto aqui'")
        print("Para arquivo: python script.py --file caminho/do/arquivo.txt")