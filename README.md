
# FindLanguage

FindLanguage is a Flask application that uses FastText to predict the language of given text inputs. The application is designed to run inside a Docker container and provides a RESTful API for language prediction.

## Features

- Predicts the language of given text inputs.
- Supports both single text and multiple texts in a single request.
- Dockerized for easy deployment.

## Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/findlanguage.git
cd findlanguage
```

2. Create the required directories and files:

```sh
mkdir -p app
touch app/__init__.py app/routes.py app/predict.py run.py requirements.txt Dockerfile docker-compose.yml
```

3. Populate the files with the following content:

### `app/__init__.py`

```python
from flask import Flask

app = Flask(__name__)

from app import routes
```

### `app/routes.py`

```python
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
```

### `app/predict.py`

```python
import fasttext

# Load the model once at the start
model = fasttext.load_model('./models/lid.176.ftz')

def predict_language(content):
    predictions = model.predict(content, k=1)
    language_code = predictions[0][0].replace("__label__", "")
    return language_code
```

### `run.py`

```python
from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

### `requirements.txt`

```txt
Flask==1.1.2
Werkzeug==1.0.1
Jinja2==2.11.3
MarkupSafe==1.1.1
itsdangerous==1.1.0
fasttext==0.9.2
```

### `Dockerfile`

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install build-essential and g++ for fasttext compilation
RUN apt-get update && apt-get install -y     build-essential     g++

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME FindLanguage

# Run app.py when the container launches
CMD ["python", "run.py"]
```

### `docker-compose.yml`

```yaml
version: '3'
services:
  findlanguage:
    build: .
    ports:
      - "5001:5000"  # Change the host port to 5001
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
```

4. Place the FastText model file `lid.176.ftz` in the `models` directory:

```sh
mkdir models
# Place lid.176.ftz inside the models directory
```

## Usage

1. Build the Docker image:

```sh
docker-compose build
```

2. Run the Docker container:

```sh
docker-compose up
```

The Flask application will be accessible at `http://127.0.0.1:5001`.

## API Endpoints

### POST /predict

- **Description**: Predicts the language of given text inputs.
- **Content-Type**: `application/json`
- **Request Body**: 
  - Single text object:
    ```json
    {
      "id": 3423434,
      "text": "Hello, how are you?"
    }
    ```
  - Multiple text objects:
    ```json
    [
      {
        "id": 3423434,
        "text": "Hello, how are you?"
      },
      {
        "id": 567890,
        "text": "Bonjour, comment ça va?"
      }
    ]
    ```

- **Response**:
  - For a single text object:
    ```json
    {
      "id": 3423434,
      "text": "Hello, how are you?",
      "language": "en"
    }
    ```
  - For multiple text objects:
    ```json
    [
      {
        "id": 3423434,
        "text": "Hello, how are you?",
        "language": "en"
      },
      {
        "id": 567890,
        "text": "Bonjour, comment ça va?",
        "language": "fr"
      }
    ]
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
