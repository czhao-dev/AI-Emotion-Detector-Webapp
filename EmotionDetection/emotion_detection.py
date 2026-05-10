"""Emotion detection client for the IBM Watson NLP demo endpoint."""

from __future__ import annotations

import math
from typing import Any

import requests

API_URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
API_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result() -> dict[str, float | str]:
    """Return the public result shape used for invalid input or API failures."""
    return {
        "anger": 0.0,
        "disgust": 0.0,
        "fear": 0.0,
        "joy": 0.0,
        "sadness": 0.0,
        "dominant_emotion": "None",
    }


def _extract_emotion_scores(payload: dict[str, Any]) -> dict[str, float] | None:
    """Read emotion scores from the API payload without assuming every key exists."""
    try:
        raw_scores = payload["emotionPredictions"][0]["emotion"]
    except (KeyError, IndexError, TypeError):
        return None

    if not isinstance(raw_scores, dict):
        return None

    scores = {}
    for emotion in EMOTIONS:
        try:
            score = float(raw_scores.get(emotion, 0.0))
        except (TypeError, ValueError):
            score = 0.0

        scores[emotion] = score if math.isfinite(score) else 0.0

    return scores


def emotion_detector(text_to_analyze: str | None) -> dict[str, float | str]:
    """Analyze text and return emotion scores with the dominant emotion.

    The function always returns the same dictionary shape so Flask routes and tests
    can handle invalid input, network issues, and unexpected API payloads cleanly.
    """
    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_result()

    payload = {"raw_document": {"text": text_to_analyze.strip()}}

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=API_HEADERS,
            timeout=10,
        )
    except requests.RequestException:
        return _empty_result()

    if response.status_code != 200:
        return _empty_result()

    try:
        response_payload = response.json()
    except ValueError:
        return _empty_result()

    emotion_scores = _extract_emotion_scores(response_payload)
    if emotion_scores is None:
        return _empty_result()

    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    return {
        **emotion_scores,
        "dominant_emotion": dominant_emotion,
    }
