from Models.DepartementClassification import DepClassifier
from Models.SentimentAnalysis import SentAnalyzer
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_models():
    try:
        # Ensure directories exist
        Path("./saved_models").mkdir(parents=True, exist_ok=True)
        
        logger.info("Initializing Department Classifier...")
        DepClassifier()
        logger.info("Department Classifier initialized and saved")

        logger.info("Initializing Sentiment Analyzer...")
        SentAnalyzer()
        logger.info("Sentiment Analyzer initialized and saved")

        logger.info("All models initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing models: {str(e)}")
        raise

if __name__ == "__main__":
    initialize_models()