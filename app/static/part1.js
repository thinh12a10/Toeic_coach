console.log("part1.js loaded");

let currentQuestion = null;

let mediaRecorder = null;
let audioChunks = [];
let timerInterval = null;
let timerLeft = 45;

const TOTAL_TIME = 45;

// =========================
// UI Helper Functions
// =========================

function getElements() {
    return {
        questionEl: document.getElementById("question-text"),
        loadingEl: document.getElementById("loading-indicator"),
        evaluationResultEl: document.getElementById("evaluation-result"),
        loadingEvaluationEl: document.getElementById("loading-evaluation-indicator"),
        timerDisplayEl: document.getElementById("timer-display"),
        timerLegacyEl: document.getElementById("timer"),
        timerProgressEl: document.getElementById("timer-progress"),
        timerWidgetEl: document.getElementById("timer-widget"),
        recordingStatusEl: document.getElementById("recording-status"),
        nextBtn: document.getElementById("next-btn"),
        startBtn: document.getElementById("start-btn"),
        stopBtn: document.getElementById("stop-btn"),
        resetBtn: document.getElementById("reset-btn")
    };
}

function setRecordingState(isRecording) {
    const { startBtn, stopBtn, recordingStatusEl, timerWidgetEl } = getElements();

    if (startBtn) startBtn.disabled = isRecording;
    if (stopBtn) stopBtn.disabled = !isRecording;

    if (recordingStatusEl) {
        if (isRecording) {
            recordingStatusEl.innerText = "🔴 Recording...";
            recordingStatusEl.classList.add("is-recording");
        } else {
            recordingStatusEl.innerText = "Ready";
            recordingStatusEl.classList.remove("is-recording");
        }
    }

    if (timerWidgetEl) {
        if (isRecording) {
            timerWidgetEl.classList.add("is-recording");
        } else {
            timerWidgetEl.classList.remove("is-recording", "warning");
        }
    }
}

function updateTimerUI() {
    const { timerDisplayEl, timerLegacyEl, timerProgressEl, timerWidgetEl } = getElements();

    const formattedTime = `${timerLeft}s`;

    if (timerDisplayEl) {
        timerDisplayEl.innerText = formattedTime;
    }
    if (timerLegacyEl) {
        timerLegacyEl.innerText = `Time Left: ${formattedTime}`;
    }

    if (timerProgressEl) {
        const percentage = Math.max(0, Math.min(100, (timerLeft / TOTAL_TIME) * 100));
        timerProgressEl.style.width = `${percentage}%`;
    }

    if (timerWidgetEl) {
        if (timerLeft <= 10 && timerLeft > 0) {
            timerWidgetEl.classList.add("warning");
        } else {
            timerWidgetEl.classList.remove("warning");
        }
    }
}

function resetTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
    timerLeft = TOTAL_TIME;
    updateTimerUI();
}

function updateTimer() {
    if (timerLeft > 0) {
        timerLeft--;
        updateTimerUI();
    } else {
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
        stopRecording();
    }
}


// =========================
// Load Question
// =========================

async function loadQuestion() {
    const { questionEl, loadingEl, nextBtn, evaluationResultEl } = getElements();

    if (loadingEl) {
        loadingEl.style.display = "flex";
    }
    if (questionEl) {
        questionEl.innerText = "";
    }
    if (nextBtn) {
        nextBtn.disabled = true;
        nextBtn.innerText = "Loading...";
    }

    try {
        const response = await fetch("/api/part1/generate");
        currentQuestion = await response.json();

        if (questionEl) {
            questionEl.innerText = currentQuestion.text;
        }
        if (evaluationResultEl) {
            evaluationResultEl.innerHTML = `<div class="empty-state">
                <strong>Question ready!</strong>
                <p>Press "Start Recording" when you are ready to read aloud.</p>
            </div>`;
        }
    } catch (error) {
        console.error("Failed to load question:", error);
        if (questionEl) {
            questionEl.innerText = "Failed to load question. Please try again.";
        }
    } finally {
        if (loadingEl) {
            loadingEl.style.display = "none";
        }
        if (nextBtn) {
            nextBtn.disabled = false;
            nextBtn.innerText = "Next Question";
        }
    }
}


// =========================
// Start Recording
// =========================

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        audioChunks = [];
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        resetTimer();
        mediaRecorder.start();
        setRecordingState(true);
        timerInterval = setInterval(updateTimer, 1000);

    } catch (error) {
        console.error("Error accessing microphone:", error);
        alert("Cannot access microphone. Please ensure microphone permissions are granted.");
    }
}


// =========================
// Stop Recording
// =========================

function stopRecording() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }

    setRecordingState(false);

    if (!mediaRecorder || mediaRecorder.state === "inactive") {
        return;
    }

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        await evaluateAudio(audioBlob);
    };

    mediaRecorder.stop();
}


// =========================
// Evaluate Audio
// =========================

async function evaluateAudio(audioBlob) {
    const { evaluationResultEl, loadingEvaluationEl } = getElements();

    if (!currentQuestion) {
        alert("Generate a question first.");
        return;
    }

    if (loadingEvaluationEl) {
        loadingEvaluationEl.style.display = "flex";
    }

    const formData = new FormData();
    formData.append("original_text", currentQuestion.text);
    formData.append("audio", audioBlob, "recording.webm");

    try {
        const response = await fetch("/api/part1/evaluate", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        displayResult(result);
    } catch (error) {
        console.error("Failed to evaluate audio:", error);
        if (evaluationResultEl) {
            evaluationResultEl.innerHTML = `<div class="empty-state" style="color: #b71c1c;">
                <strong>Evaluation failed.</strong>
                <p>Please try recording again.</p>
            </div>`;
        }
    } finally {
        if (loadingEvaluationEl) {
            loadingEvaluationEl.style.display = "none";
        }
    }
}


// =========================
// Display Result
// =========================

function displayResult(result) {
    const { evaluationResultEl } = getElements();
    if (!evaluationResultEl) return;

    evaluationResultEl.innerHTML = `
        <div class="result-card">
            <h3>Total Score: ${result.total_score || 0} / 10</h3>
        </div>

        <div class="score-card">
            <strong>Pronunciation Score</strong>
            <p>${result.pronunciation?.score ?? 'N/A'}</p>
            ${result.pronunciation?.mispronounced_words?.length ? `<p><strong>Mispronounced Words:</strong> ${result.pronunciation.mispronounced_words.join(", ")}</p>` : ''}
            ${result.pronunciation?.missing_end_sounds?.length ? `<p><strong>Missing End Sounds:</strong> ${result.pronunciation.missing_end_sounds.join(", ")}</p>` : ''}
            ${result.pronunciation?.vowel_issues?.length ? `<p><strong>Vowel Issues:</strong> ${result.pronunciation.vowel_issues.join(", ")}</p>` : ''}
        </div>

        <div class="result-card" style="margin-top: 12px;">
            <h3>Overall Feedback</h3>
            <p>${result.overall_feedback || "No feedback provided."}</p>
        </div>

        ${result.study_plan?.length ? `
        <div class="result-card">
            <h3>Study Plan</h3>
            <ul>
                ${result.study_plan.map(item => `<li>${item}</li>`).join("")}
            </ul>
        </div>` : ''}
    `;
}


// =========================
// Reset
// =========================

function resetPage() {
    currentQuestion = null;
    resetTimer();
    setRecordingState(false);

    const { questionEl, evaluationResultEl } = getElements();

    if (questionEl) {
        questionEl.innerHTML = "Click 'Next Question'";
    }

    if (evaluationResultEl) {
        evaluationResultEl.innerHTML = `
            <div class="empty-state">
                <strong>Click "Next Question" to load a passage.</strong>
                <p>Press "Start Recording" when you are ready to read aloud.</p>
            </div>
        `;
    }
}


// =========================
// Event Binding
// =========================

document.addEventListener("DOMContentLoaded", () => {
    const { nextBtn, startBtn, stopBtn, resetBtn } = getElements();

    if (nextBtn) nextBtn.addEventListener("click", loadQuestion);
    if (startBtn) startBtn.addEventListener("click", startRecording);
    if (stopBtn) stopBtn.addEventListener("click", stopRecording);
    if (resetBtn) resetBtn.addEventListener("click", resetPage);

    resetTimer();
    setRecordingState(false);
});