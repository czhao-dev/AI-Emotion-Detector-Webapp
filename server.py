"""Flask server for the emotion detector web application."""

import os

from flask import Flask, jsonify, render_template, request

from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.get("/emotionDetector")
def detect_emotion():
    """Analyze submitted text and return emotion scores as JSON."""
    text_to_analyze = request.args.get("textToAnalyze", "")

    if not text_to_analyze.strip():
        return (
            jsonify(
                {
                    "error": "Enter a sentence with enough context to analyze.",
                    "result": emotion_detector(text_to_analyze),
                }
            ),
            400,
        )

    result = emotion_detector(text_to_analyze)

    if result["dominant_emotion"] == "None":
        return (
            jsonify(
                {
                    "error": "The emotion service is unavailable. Try again shortly.",
                    "result": result,
                }
            ),
            503,
        )

    return jsonify({"result": result})


@app.get("/")
def render_index_page():
    """Render the browser interface."""
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
