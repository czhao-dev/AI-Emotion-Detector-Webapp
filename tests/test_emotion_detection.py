"""Tests for the emotion detection client."""

from unittest.mock import Mock, patch

import requests

from EmotionDetection.emotion_detection import API_HEADERS, API_URL, emotion_detector


def make_response(status_code=200, payload=None):
    response = Mock()
    response.status_code = status_code
    response.json.return_value = payload or {}
    return response


def test_emotion_detector_returns_scores_and_dominant_emotion():
    payload = {
        "emotionPredictions": [
            {
                "emotion": {
                    "anger": 0.02,
                    "disgust": 0.01,
                    "fear": 0.04,
                    "joy": 0.9,
                    "sadness": 0.03,
                }
            }
        ]
    }

    with patch("EmotionDetection.emotion_detection.requests.post") as post:
        post.return_value = make_response(payload=payload)

        result = emotion_detector("I am glad this happened")

    post.assert_called_once_with(
        API_URL,
        json={"raw_document": {"text": "I am glad this happened"}},
        headers=API_HEADERS,
        timeout=10,
    )
    assert result == {
        "anger": 0.02,
        "disgust": 0.01,
        "fear": 0.04,
        "joy": 0.9,
        "sadness": 0.03,
        "dominant_emotion": "joy",
    }


def test_emotion_detector_rejects_blank_text_without_api_call():
    with patch("EmotionDetection.emotion_detection.requests.post") as post:
        result = emotion_detector("   ")

    post.assert_not_called()
    assert result["dominant_emotion"] == "None"
    assert result["joy"] == 0.0


def test_emotion_detector_handles_service_errors():
    with patch("EmotionDetection.emotion_detection.requests.post") as post:
        post.side_effect = requests.Timeout

        result = emotion_detector("This should not crash.")

    assert result["dominant_emotion"] == "None"


def test_emotion_detector_handles_unexpected_payloads():
    with patch("EmotionDetection.emotion_detection.requests.post") as post:
        post.return_value = make_response(payload={"unexpected": "shape"})

        result = emotion_detector("This should not crash either.")

    assert result["dominant_emotion"] == "None"


def test_emotion_detector_handles_invalid_score_values():
    payload = {
        "emotionPredictions": [
            {
                "emotion": {
                    "anger": None,
                    "disgust": "not-a-number",
                    "fear": float("nan"),
                    "joy": 0.72,
                    "sadness": 0.04,
                }
            }
        ]
    }

    with patch("EmotionDetection.emotion_detection.requests.post") as post:
        post.return_value = make_response(payload=payload)

        result = emotion_detector("I am glad this is resilient.")

    assert result["anger"] == 0.0
    assert result["disgust"] == 0.0
    assert result["fear"] == 0.0
    assert result["dominant_emotion"] == "joy"
