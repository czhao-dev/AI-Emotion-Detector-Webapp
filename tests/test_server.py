"""Tests for the Flask app routes."""

from unittest.mock import patch

from server import app


def test_index_route_loads_app_shell():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"AI Emotion Detector" in response.data


def test_emotion_detector_route_returns_validation_error_for_blank_text():
    client = app.test_client()

    response = client.get("/emotionDetector?textToAnalyze=")
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["error"] == "Enter a sentence with enough context to analyze."
    assert payload["result"]["dominant_emotion"] == "None"


def test_emotion_detector_route_returns_service_error_for_failed_analysis():
    client = app.test_client()

    with patch("server.emotion_detector") as detector:
        detector.return_value = {
            "anger": 0.0,
            "disgust": 0.0,
            "fear": 0.0,
            "joy": 0.0,
            "sadness": 0.0,
            "dominant_emotion": "None",
        }

        response = client.get("/emotionDetector?textToAnalyze=Hello")

    payload = response.get_json()
    assert response.status_code == 503
    assert payload["error"] == "The emotion service is unavailable. Try again shortly."
