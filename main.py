from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from pathlib import Path
from Models.DepartementClassification import DepClassifier
from Models.SentimentAnalysis import SentAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ensure saved_models directory exists
Path("./saved_models").mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
CORS(app)

# Initialize models
try:
    logger.info("Loading models...")
    department_model = DepClassifier()
    priority_model = SentAnalyzer()
    logger.info("Models loaded successfully")
except Exception as e:
    logger.error(f"Failed to load models: {str(e)}")
    raise

@app.route('/predict_department', methods=['POST'])
def predict_department():
    try:
        input_text = request.json.get('text', '')
        if not input_text:
            return jsonify({'error': 'No input text provided'}), 400

        departments = ["IT", "Finance", "HR", "Sales"]
        result = department_model.classify_ticket(input_text, departments)
        return jsonify({'prediction': result})
    except Exception as e:
        logger.error(f"Error in predict_department: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict_priority', methods=['POST'])
def predict_priority():
    try:
        input_text = request.json.get('text', '')
        if not input_text:
            return jsonify({'error': 'No input text provided'}), 400

        priority = priority_model.classify_priority(input_text)
        return jsonify({
            'prediction': priority,
            'score': priority_model.score,
            'label': priority_model.label
        })
    except Exception as e:
        logger.error(f"Error in predict_priority: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=9000)