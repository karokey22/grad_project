from transformers import pipeline
import pickle
import os
import logging
from pathlib import Path

class SentAnalyzer:
    def __init__(self):
        self.model_path = Path("./saved_models/sentiment_analyzer.pkl")
        self.sentiment_analyzer = self._load_or_create_model()
        self.label = ""
        self.score = 0
        self.output = ""
    
    def _load_or_create_model(self):
        try:
            if self.model_path.exists():
                logging.info("Loading saved sentiment analyzer...")
                with open(self.model_path, 'rb') as f:
                    return pickle.load(f)
            
            logging.info("Creating new sentiment analyzer...")
            model = pipeline("sentiment-analysis")
            
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(model, f)
            
            return model
            
        except Exception as e:
            logging.error(f"Error in loading/creating sentiment analyzer: {str(e)}")
            raise

    def classify_priority(self, ticket_text):
        try:
            sentiment = self.sentiment_analyzer(ticket_text)[0]
            self.label = sentiment['label']
            self.score = sentiment['score']

            if self.label == "NEGATIVE":
                if self.score > 0.75:
                    self.output = "High"
                else:
                    self.output = "Medium"
            elif self.label == "NEUTRAL":
                self.output = "Medium"
            else:  # POSITIVE
                if self.score > 0.75:
                    self.output = "Low"
                else:
                    self.output = "Medium"
            return self.output
        except Exception as e:
            logging.error(f"Error in priority classification: {str(e)}")
            raise