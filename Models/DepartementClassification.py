from transformers import pipeline
import pickle
import os
import logging
from pathlib import Path

class DepClassifier:
    def __init__(self):
        self.model_path = Path("./saved_models/department_classifier.pkl")
        self.classifier = self._load_or_create_model()
        self.result = ""
        self.best_department = ""
    
    def _load_or_create_model(self):
        try:
            if self.model_path.exists():
                logging.info("Loading saved department classifier...")
                with open(self.model_path, 'rb') as f:
                    return pickle.load(f)
            
            logging.info("Creating new department classifier...")
            model = pipeline("zero-shot-classification")
            
            self.model_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(model, f)
            
            return model
            
        except Exception as e:
            logging.error(f"Error in loading/creating department classifier: {str(e)}")
            raise

    def classify_ticket(self, ticket, departments):
        try:
            self.result = self.classifier(ticket, candidate_labels=departments)
            self.best_department = self.result["labels"][0]
            return self.best_department
        except Exception as e:
            logging.error(f"Error in ticket classification: {str(e)}")
            raise