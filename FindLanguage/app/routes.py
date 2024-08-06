from flask import request, jsonify
from app import app
from app.predict import predict_language

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Check if the data is a list
    if isinstance(data, list):
        results = []
        for item in data:
            if 'id' not in item or 'text' not in item:
                return jsonify({"error": "Each object must contain 'id' and 'text' fields"}), 400
            
            text = item['text']
            language_code = predict_language(text)
            results.append({
                "id": item['id'],
                "text": text,
                "language": language_code
            })
        return jsonify(results)
    
    # Check if the data is a single object
    elif isinstance(data, dict):
        if 'id' not in data or 'text' not in data:
            return jsonify({"error": "Object must contain 'id' and 'text' fields"}), 400
        
        text = data['text']
        language_code = predict_language(text)
        result = {
            "id": data['id'],
            "text": text,
            "language": language_code
        }
        return jsonify(result)
    
    # If the data is neither a list nor a dict, return an error
    else:
        return jsonify({"error": "Invalid input format"}), 400
