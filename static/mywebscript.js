const emotions = ["anger", "disgust", "fear", "joy", "sadness"];

const form = document.getElementById("analysisForm");
const textarea = document.getElementById("textToAnalyze");
const characterCount = document.getElementById("characterCount");
const analyzeButton = document.getElementById("analyzeButton");
const statusPill = document.getElementById("statusPill");
const dominantEmotion = document.getElementById("dominantEmotion");
const scoreList = document.getElementById("scoreList");
const systemResponse = document.getElementById("systemResponse");

const formatEmotion = (emotion) =>
    emotion.charAt(0).toUpperCase() + emotion.slice(1);

const formatScore = (score) => `${Math.round(Number(score) * 100)}%`;

const renderScores = (result = {}) => {
    scoreList.innerHTML = emotions
        .map((emotion) => {
            const score = Number(result[emotion] || 0);
            const width = Math.max(0, Math.min(score * 100, 100));

            return `
                <div class="score-row">
                    <div class="score-label">
                        <span>${formatEmotion(emotion)}</span>
                        <strong>${formatScore(score)}</strong>
                    </div>
                    <div class="score-track" aria-hidden="true">
                        <span style="width: ${width}%"></span>
                    </div>
                </div>
            `;
        })
        .join("");
};

const setState = (state, message) => {
    statusPill.textContent = state;
    systemResponse.textContent = message;
};

const renderResult = (result) => {
    dominantEmotion.textContent = formatEmotion(result.dominant_emotion);
    renderScores(result);
    setState("Complete", "Analysis complete.");
};

const renderError = (message, result) => {
    dominantEmotion.textContent = "No result";
    renderScores(result);
    setState("Needs text", message);
};

textarea.addEventListener("input", () => {
    characterCount.textContent = `${textarea.value.length} / ${textarea.maxLength}`;
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const textToAnalyze = textarea.value.trim();
    analyzeButton.disabled = true;
    setState("Analyzing", "Reading emotional tone...");

    try {
        const params = new URLSearchParams({ textToAnalyze });
        const response = await fetch(`/emotionDetector?${params.toString()}`);
        const payload = await response.json();

        if (!response.ok) {
            renderError(payload.error || "Unable to analyze that text.", payload.result);
            return;
        }

        renderResult(payload.result);
    } catch (error) {
        renderError("The emotion service is unavailable. Try again shortly.");
    } finally {
        analyzeButton.disabled = false;
    }
});

renderScores();
