# Turkish News Classification System

## Overview

This project is a web application that uses machine learning to automatically classify Turkish news articles into different categories. The system uses a trained neural network model to analyze and categorize news text into categories such as politics, economy, sports, technology, health, world news, and culture.

## Features

- **Text Classification**: Analyze Turkish news articles and classify them into predefined categories
- **User-Friendly Interface**: Simple web interface for easy text input and classification
- **Demo Section**: Sample texts for each category to demonstrate the system's capabilities
- **REST API**: Backend API for integration with other applications

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Machine Learning**: TensorFlow/Keras
- **Natural Language Processing**: Turkish text preprocessing with TurkishStemmer
- **Deployment**: Docker containerization, Gunicorn WSGI server

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/devdogukan/turkish-news-classification.git
cd turkish-news-classification
```

2. Build and run the Docker container:
```bash
docker build -t turkish-news-classification .
docker run -p 5000:5000 turkish-news-classification
```

3. Access the application at http://localhost:5000

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/devdogukan/turkish-news-classification.git
cd turkish-news-classification
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Access the application at http://localhost:5000

## Usage

1. Open your web browser and navigate to http://localhost:5000
2. Enter or paste a Turkish news article text into the text area
3. Click "Sınıflandır" (Classify) to analyze the text
4. View the classification results showing the predicted category
5. Try different examples using the "Örnek Metinleri Görüntüle" (View Sample Texts) button

## API Usage

The application provides a REST API endpoint that can be used for programmatic access:

```
POST /predict
Content-Type: application/json

{
  "text": "Your Turkish news text here"
}

Response:
{
  "category": "predicted_category",
  "confidence": 0.95
}
```

Project Structure
----------------
```
turkish-news-classification/
├── app.py                # Main Flask application
├── models/               # ML model files
│   ├── turkish_news_catagory.json      # Model architecture
│   ├── turkish_news_catagory.weights.h5 # Model weights
│   ├── tokenizer.pickle  # Text tokenizer
│   └── label_encoder.pickle # Category labels
├── static/               # Static files (CSS, JS)
│   └── css/
│       └── style.css
├── templates/            # HTML templates
│   ├── index.html        # Main page
│   └── demo.html         # Sample texts page
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
└── README.txt            # This file
```

Model Information
----------------
The classification model is a neural network trained on a dataset of Turkish news articles. It uses word embeddings and sequence processing to understand the context and content of news texts.

The model currently supports the following categories:
- Siyaset (Politics)
- Ekonomi (Economy)
- Spor (Sports)
- Teknoloji (Technology)
- Sağlık (Health)
- Dünya (World News)
- Kültür (Culture)

License
-------
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgements
---------------
- TurkishStemmer for Turkish text lemmatization
- TensorFlow and Keras for machine learning framework
- Flask for the web application framework