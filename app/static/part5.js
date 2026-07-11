console.log("part5.js loaded");

let currentQuestions = [];
let currentQuestionIndex = 0;
let currentQuestion = null;
let mediaRecorder = null;
let audioChunks = [];
let timerInterval = null;
let timeLeft = 60;
let audioStream = null;

const questionTextEl = document.getElementById("question-text");
const questionNumberEl = document.getElementById("question-number");
const timerEl = document.getElementById("timer-display");
const recordingStatusEl = document.getElementById("recording-status");
const startBtn = document.getElementById("start-record-btn");
const startQuestionBtn = document.getElementById("start-question-btn");
const nextBtn = document.getElementById("next-question-btn");
const backBtn = document.getElementById("back-btn");
const loadingIndicatorEl = document.getElementById("loading-indicator");
const loadingEvaluationEl = document.getElementById("loading-evaluation-indicator");
const evaluationResultEl = document.getElementById("evaluation-result");

function resetTimer() {
    clearInterval(timerInterval);
    timeLeft = currentQuestion?.response_time || 60;
    if (timerEl) {
        timerEl.textContent = `${timeLeft}s`;
    }
}

function updateTimer() {
    if (!timerEl) {
        return;
    }

    timerEl.textContent = `${timeLeft}s`;
    if (timeLeft <= 0) {
        clearInterval(timerInterval);
        stopRecording();
        return;
    }
    timeLeft -= 1;
}

function setRecordingState(isRecording) {
    if (recordingStatusEl) {
        recordingStatusEl.textContent = isRecording ? "Recording..." : "Ready";
        recordingStatusEl.classList.toggle("is-recording", isRecording);
    }

    if (startBtn) {
        startBtn.disabled = isRecording;
        startBtn.textContent = isRecording ? "Recording..." : "Start Record";
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

    currentQuestion = question;
    if (questionNumberEl) {
        questionNumberEl.textContent = `Question ${question.question_number}`;
    }

    if (questionTextEl) {
        questionTextEl.innerHTML = `
            <h3>Question ${question.question_number}</h3>
            <p>${question.text}</p>
            <p><strong>Preparation:</strong> ${question.preparation_time || 45} seconds</p>
            <p><strong>Response:</strong> ${question.response_time || 60} seconds</p>
        `;
    }

    resetTimer();
    setRecordingState(false);
}

async function loadQuestions() {
    showLoading(loadingIndicatorEl, "Loading opinion prompt...");
    try {
        const response = await fetch("/api/part5/generate");
        if (!response.ok) {
            throw new Error(`Failed to load Part 5 questions (${response.status})`);
        }

        const data = await response.json();
        currentQuestions = data.questions || [];
        currentQuestionIndex = 0;
        if (currentQuestions.length > 0) {
            renderQuestion(currentQuestions[0]);
        }
    } catch (error) {
        console.error("Failed to load Part 5 questions:", error);
        if (questionTextEl) {
            questionTextEl.innerHTML = `
                <h3>Unable to load prompt</h3>
                <p>Please try again in a moment.</p>
            `;
        }
    } finally {
        hideLoading(loadingIndicatorEl);
    }
}

async function startRecording() {
    if (!currentQuestion) {
        await loadQuestions();
    }

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showError("Microphone access is not supported in this browser.");
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
    mediaRecorder.stop();
}

async function evaluateAudio(audioBlob) {
    if (!currentQuestion) {
        showError("Please load the prompt before recording.");
        return;
    }

    showLoading(loadingEvaluationEl, "Analyzing your opinion response...");

    const formData = new FormData();
    formData.append("original_text", currentQuestion.text || "Please answer the question naturally.");
    formData.append("audio", audioBlob, "recording.webm");

    try {
        const response = await fetch("/api/part5/evaluate", {
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
    if (!evaluationResultEl) {
        return;
    }

    const pronunciation = result.pronunciation || {};
    const organization = result.organization || {};
    const delivery = result.delivery || {};

    evaluationResultEl.innerHTML = `
        <div class="score-grid">
            <div class="score-card"><strong>Overall</strong>${result.total_score ?? "—"}</div>
            <div class="score-card"><strong>Pronunciation</strong>${pronunciation.score ?? "—"}</div>
            <div class="score-card"><strong>Structure</strong>${organization.score ?? "—"}</div>
            <div class="score-card"><strong>Delivery</strong>${delivery.score ?? "—"}</div>
        </div>
        <div class="result-card">
            <h3>Overall feedback</h3>
            <p>${result.overall_feedback || "Your response will be summarized here."}</p>
        </div>
        <div class="result-card">
            <h3>Study plan</h3>
            <ul>
                ${(result.study_plan || []).map((item) => `<li>${item}</li>`).join("")}
            </ul>
        </div>
    `;
}

function showError(message) {
    if (questionTextEl) {
        questionTextEl.innerHTML = `
            <h3>Notice</h3>
            <p>${message}</p>
        `;
    }
    if (evaluationResultEl) {
        evaluationResultEl.innerHTML = `
            <div class="empty-state">
                <strong>${message}</strong>
                <p>Please check your microphone and try again.</p>
            </div>
        `;
    }
}

if (startQuestionBtn) {
    startQuestionBtn.addEventListener("click", loadQuestions);
}

if (startBtn) {
    startBtn.addEventListener("click", async () => {
        if (!currentQuestion) {
            await loadQuestions();
        }
        startRecording();
    });
}

if (nextBtn) {
    nextBtn.addEventListener("click", loadQuestions);
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

resetTimer();
