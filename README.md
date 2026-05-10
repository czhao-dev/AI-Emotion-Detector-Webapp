# AI Emotion Detector

A Flask web application that analyzes text and predicts emotional tone using an
IBM Watson NLP emotion classification endpoint. The app returns confidence
scores for anger, disgust, fear, joy, and sadness, then highlights the dominant
emotion in a clean browser interface.

## Features

- Text emotion analysis through a Flask JSON endpoint
- Emotion score visualization in the browser
- Graceful handling for blank input, API errors, malformed responses, and
  network failures
- Deterministic unit tests with mocked API responses
- Ruff linting and GitHub Actions CI

## Tech Stack

- Python
- Flask
- Requests
- Pytest
- Ruff
- HTML, CSS, and JavaScript

## Project Structure

```text
AI-Emotion-Detector-Webapp/
├── .github/workflows/ci.yml
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py
├── static/
│   ├── favicon.svg
│   ├── mywebscript.js
│   └── styles.css
├── templates/
│   └── index.html
├── tests/
│   ├── test_emotion_detection.py
│   └── test_server.py
├── server.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Getting Started

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python3 server.py
```

Open `http://localhost:5000` in your browser.

## Testing

Run the test suite:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

## API Response

The `/emotionDetector` route accepts a `textToAnalyze` query parameter and
returns JSON.

Successful response:

```json
{
  "result": {
    "anger": 0.02,
    "disgust": 0.01,
    "fear": 0.04,
    "joy": 0.9,
    "sadness": 0.03,
    "dominant_emotion": "joy"
  }
}
```

Validation or service failure response:

```json
{
  "error": "Enter a sentence with enough context to analyze.",
  "result": {
    "anger": 0.0,
    "disgust": 0.0,
    "fear": 0.0,
    "joy": 0.0,
    "sadness": 0.0,
    "dominant_emotion": "None"
  }
}
```

## Notes

This project uses a public IBM Skills Network Watson NLP demo endpoint. The app
handles service failures gracefully, but production deployments should use a
managed NLP service account, stronger observability, and rate limiting.

## License

This project is licensed under the Apache License 2.0.
