console.log("part2.js loaded");

let currentQuestion = null;
let mediaRecorder = null;
let audioChunks = [];
let timerInterval = null;
let timeLeft = 30;
let audioStream = null;
let recognition = null;
let currentTranscript = "";
let currentQuestionIndex = 0;

const recordingStatusEl = document.getElementById("recording-status");
const timerEl = document.getElementById("timer-display");
const imageEl = document.getElementById("question-image");
const imagePlaceholderEl = document.getElementById("image-placeholder");
const transcriptEl = document.getElementById("transcript-result");
const resultEl = document.getElementById("evaluation-result");
const startBtn = document.getElementById("start-record-btn");
const startQuestionBtn = document.getElementById("start-question-btn");
const nextBtn = document.getElementById("next-question-btn");
const backBtn = document.getElementById("back-btn");
const loadingImageEl = document.getElementById("loading-image-indicator");
const loadingEvaluationEl = document.getElementById("loading-evaluation-indicator");

const TOTAL_TIME = 30;

function updateTimerUI() {
    if (timerEl) {
        timerEl.textContent = `${timeLeft}s`;
    }
    const timerProgressEl = document.getElementById("timer-progress");
    if (timerProgressEl) {
        const pct = Math.max(0, Math.min(100, (timeLeft / TOTAL_TIME) * 100));
        timerProgressEl.style.width = `${pct}%`;
    }
    const timerWidgetEl = document.getElementById("timer-widget");
    if (timerWidgetEl) {
        if (timeLeft <= 10 && timeLeft > 0) {
            timerWidgetEl.classList.add("warning");
        } else {
            timerWidgetEl.classList.remove("warning");
        }
    }
}

// Reset the speaking timer to the default 30-second limit.
function resetTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
    timeLeft = TOTAL_TIME;
    updateTimerUI();
}

function updateTimer() {
    updateTimerUI();
    if (timeLeft <= 0) {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
        stopRecording();
        return;
    }

    timeLeft -= 1;
}

function setRecordingState(isRecording) {
    if (recordingStatusEl) {
        recordingStatusEl.textContent = isRecording ? "🔴 Recording..." : "Ready";
        recordingStatusEl.classList.toggle("is-recording", isRecording);
    }

    const timerWidgetEl = document.getElementById("timer-widget");
    if (timerWidgetEl) {
        if (isRecording) {
            timerWidgetEl.classList.add("is-recording");
        } else {
            timerWidgetEl.classList.remove("is-recording", "warning");
        }
    }

    if (startBtn) {
        startBtn.disabled = isRecording;
        startBtn.textContent = isRecording ? "Recording..." : "🎤 Start Record";
    }

    const stopRecordBtn = document.getElementById("stop-record-btn");
    if (stopRecordBtn) {
        stopRecordBtn.disabled = !isRecording;
    }
}

function showLoading(targetEl, label) {
    if (targetEl) {
        targetEl.style.display = "flex";
        targetEl.querySelector(".loading-text").textContent = label;
    }
}

function hideLoading(targetEl) {
    if (targetEl) {
        targetEl.style.display = "none";
    }
}

function renderQuestion(question) {
    if (!question) {
        return;
    }

    const questionNumberEl = document.getElementById("question-number");
    if (questionNumberEl) {
        questionNumberEl.textContent = `Question ${currentQuestionIndex + 1}`;
    }

    if (imageEl) {
        imageEl.src = question.image_url || "";
        imageEl.alt = question.instruction || "Picture prompt";
    }

    if (imagePlaceholderEl) {
        imagePlaceholderEl.style.display = "none";
    }

    currentTranscript = "";
    if (transcriptEl) {
        transcriptEl.textContent = "Click Start to load a picture prompt.";
    }

    if (resultEl) {
        resultEl.innerHTML = `
            <div class="empty-state">
                <strong>Click Start to load a picture prompt.</strong>
                <p>Your speech transcript and AI feedback will appear here once recording is complete.</p>
            </div>
        `;
    }
}

async function loadQuestion() {
    if (loadingImageEl) {
        showLoading(loadingImageEl, "Loading image...");
    }

    if (imageEl) {
        imageEl.src = "";
        imageEl.style.display = "none";
    }

    if (imagePlaceholderEl) {
        imagePlaceholderEl.style.display = "flex";
    }

    resetTimer();
    setRecordingState(false);

    try {
        const response = await fetch("/api/part2/generate");
        if (!response.ok) {
            throw new Error(`Failed to load question (${response.status})`);
        }

        currentQuestion = await response.json();
        currentQuestionIndex += 1;
        const imageUrl = currentQuestion.image_url || "/static/images/part2-placeholder.svg";
        if (imageEl) {
            imageEl.src = imageUrl;
            imageEl.style.display = "block";
        }

        renderQuestion(currentQuestion);
    } catch (error) {
        console.error("Failed to load question:", error);
        if (imagePlaceholderEl) {
            imagePlaceholderEl.style.display = "flex";
            imagePlaceholderEl.querySelector("h3").textContent = "Unable to load image";
            imagePlaceholderEl.querySelector("p").textContent = "Please check your connection and try again.";
        }
        if (transcriptEl) {
            transcriptEl.textContent = "Unable to load the question image.";
        }
    } finally {
        hideLoading(loadingImageEl);
    }
}

// Start microphone capture, begin the countdown, and optionally enable browser speech transcription.
async function startRecording() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showError("Your browser does not support microphone access.");
        return;
    }

    try {
        if (audioStream) {
            audioStream.getTracks().forEach((track) => track.stop());
        }

        audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        audioChunks = [];
        mediaRecorder = new MediaRecorder(audioStream);

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
            await evaluateAudio(audioBlob);
            if (audioStream) {
                audioStream.getTracks().forEach((track) => track.stop());
            }
            audioStream = null;
        };

        mediaRecorder.start();
        if (recognition && typeof recognition.start === "function") {
            recognition.start();
        }
        resetTimer();
        timerInterval = setInterval(updateTimer, 1000);
        setRecordingState(true);
    } catch (error) {
        console.error("Recording failed:", error);
        showError("Microphone permission was denied or recording failed.");
    }
}

function stopRecording() {
    if (!mediaRecorder || mediaRecorder.state === "inactive") {
        return;
    }

    setRecordingState(false);
    resetTimer();
    if (recognition && typeof recognition.stop === "function") {
        recognition.stop();
    }
    mediaRecorder.stop();
}

// Send the captured audio to the evaluation endpoint and render the AI feedback once it returns.
async function evaluateAudio(audioBlob) {
    if (!currentQuestion) {
        showError("Please load a question before recording.");
        return;
    }

    showLoading(loadingEvaluationEl, "Analyzing your response...");

    const formData = new FormData();
    formData.append("original_text", currentQuestion.text || currentQuestion.instruction || "Describe the picture.");
    formData.append("audio", audioBlob, "recording.webm");

    try {
        const response = await fetch("/api/part2/evaluate", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Evaluation failed (${response.status})`);
        }

        const result = await response.json();
        displayResult(result);
    } catch (error) {
        console.error("Evaluation error:", error);
        showError("The evaluation service is unavailable. Please try again later.");
    } finally {
        hideLoading(loadingEvaluationEl);
    }
}

function displayResult(result) {
    if (!resultEl) {
        return;
    }

    const pronunciation = result.pronunciation || {};
    const intonation = result.intonation || {};
    const pacing = result.pacing || {};
    const transcriptText = result.transcript || currentTranscript || "Your transcript will appear here after the recording is processed.";
    if (transcriptEl) {
        transcriptEl.textContent = transcriptText;
    }

    resultEl.innerHTML = `
        <div class="score-grid">
            <div class="score-card"><strong>Overall</strong>${result.total_score ?? "—"}</div>
            <div class="score-card"><strong>Pronunciation</strong>${pronunciation.score ?? "—"}</div>
            <div class="score-card"><strong>Fluency</strong>${pacing.score ?? "—"}</div>
            <div class="score-card"><strong>Grammar</strong>${intonation.score ?? "—"}</div>
        </div>
        <div class="result-card">
            <h3>Key improvement tips</h3>
            <ul>
                ${(pronunciation.improvement_tips || []).concat(intonation.improvement_tips || [], pacing.improvement_tips || []).slice(0, 5).map((tip) => `<li>${tip}</li>`).join("")}
            </ul>
        </div>
        <div class="result-card">
            <h3>Overall feedback</h3>
            <p>${result.overall_feedback || "Your speaking performance will be summarized here."}</p>
        </div>
    `;
}

function showError(message) {
    if (transcriptEl) {
        transcriptEl.textContent = message;
    }
    if (resultEl) {
        resultEl.innerHTML = `
            <div class="empty-state">
                <strong>${message}</strong>
                <p>Please try again after checking your microphone, network connection, or API configuration.</p>
            </div>
        `;
    }
}

function resetPage() {
    currentQuestion = null;
    resetTimer();
    setRecordingState(false);
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
    }
    if (audioStream) {
        audioStream.getTracks().forEach((track) => track.stop());
    }
    if (recognition && typeof recognition.stop === "function") {
        recognition.stop();
    }
    audioStream = null;
    mediaRecorder = null;
    audioChunks = [];
    currentTranscript = "";

    if (imageEl) {
        imageEl.src = "";
        imageEl.style.display = "none";
    }
    if (imagePlaceholderEl) {
        imagePlaceholderEl.style.display = "flex";
        imagePlaceholderEl.querySelector("h3").textContent = "Picture will appear here";
        imagePlaceholderEl.querySelector("p").textContent = "Use the controls below to load the next prompt.";
    }
    if (transcriptEl) {
        transcriptEl.textContent = "Click Start to load a picture prompt.";
    }
    if (resultEl) {
        resultEl.innerHTML = `
            <div class="empty-state">
                <strong>Click Start to load a picture prompt.</strong>
                <p>Your speech transcript and AI feedback will appear here once recording is complete.</p>
            </div>
        `;
    }
}

function initializeSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        return null;
    }

    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = true;

    recognition.onresult = (event) => {
        const transcript = Array.from(event.results)
            .map((result) => result[0].transcript)
            .join(" ");
        currentTranscript = transcript;
        if (transcriptEl) {
            transcriptEl.textContent = transcript;
        }
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
    };

    recognition.onend = () => {
        if (transcriptEl && !currentTranscript) {
            transcriptEl.textContent = "No speech detected. Please try again.";
        }
    };

    return recognition;
}

if (startQuestionBtn) {
    startQuestionBtn.addEventListener("click", () => {
        loadQuestion();
    });
}

if (startBtn) {
    startBtn.addEventListener("click", async () => {
        if (!currentQuestion) {
            await loadQuestion();
        }
        startRecording();
    });
}

const stopRecordBtn = document.getElementById("stop-record-btn");
if (stopRecordBtn) {
    stopRecordBtn.addEventListener("click", () => {
        stopRecording();
    });
}

if (nextBtn) {
    nextBtn.addEventListener("click", loadQuestion);
}

if (backBtn) {
    backBtn.addEventListener("click", () => {
        window.location.href = "/";
    });
}

window.addEventListener("beforeunload", () => {
    if (audioStream) {
        audioStream.getTracks().forEach((track) => track.stop());
    }
});

initializeSpeechRecognition();
resetPage();
