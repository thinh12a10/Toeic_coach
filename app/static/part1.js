console.log("part1.js loaded");

let currentQuestion = null;

let mediaRecorder = null;
let audioChunks = [];


// =========================
// Load Question
// =========================

async function loadQuestion() {

    const questionEl = document.getElementById("question-text");
    const loadingEl = document.getElementById("loading-indicator");
    const nextBtn = document.getElementById("next-btn");

    // Show loading indicator and disable button
    if (loadingEl) {
        loadingEl.style.display = "flex";
    }
    questionEl.innerText = "";
    nextBtn.disabled = true;
    nextBtn.innerText = "Loading...";

    try {
        const response = await fetch(
            "/api/part1/generate"
        );

        currentQuestion = await response.json();

        questionEl.innerText = currentQuestion.text;

        document.getElementById(
            "evaluation-result"
        ).innerHTML = "Waiting for evaluation...";
    } catch (error) {
        console.error("Failed to load question:", error);
        questionEl.innerText =
            "Failed to load question. Please try again.";
    } finally {
        // Hide loading indicator and re-enable button
        if (loadingEl) {
            loadingEl.style.display = "none";
        }
        nextBtn.disabled = false;
        nextBtn.innerText = "Next Question";
    }
}


// =========================
// Start Recording
// =========================

async function startRecording() {

    try {

        const stream =
            await navigator.mediaDevices.getUserMedia({
                audio: true
            });

        audioChunks = [];

        mediaRecorder =
            new MediaRecorder(stream);

        mediaRecorder.ondataavailable =
            event => {
                audioChunks.push(event.data);
            };

        mediaRecorder.start();

        alert("Recording started");

    } catch (error) {

        console.error(error);

        alert("Cannot access microphone");
    }
}


// =========================
// Stop Recording
// =========================

function stopRecording() {

    if (!mediaRecorder) {
        return;
    }

    mediaRecorder.onstop =
        async () => {

            const audioBlob =
                new Blob(
                    audioChunks,
                    {
                        type: "audio/webm"
                    }
                );

            await evaluateAudio(
                audioBlob
            );
        };

    mediaRecorder.stop();
}


// =========================
// Evaluate Audio
// =========================

async function evaluateAudio(
    audioBlob
) {

    if (!currentQuestion) {

        alert(
            "Generate a question first."
        );

        return;
    }

    const evaluateLoading = document.getElementById("loading-evaluation-indicator");
    if (evaluateLoading) {
        evaluateLoading.style.display = "flex";
    }

    const formData =
        new FormData();

    formData.append(
        "original_text",
        currentQuestion.text
    );

    formData.append(
        "audio",
        audioBlob,
        "recording.webm"
    );

    const response =
        await fetch(
            "/api/part1/evaluate",
            {
                method: "POST",
                body: formData
            }
        );

    const result =
        await response.json();

    if (evaluateLoading) {
        evaluateLoading.style.display = "none";
    }
    
    displayResult(
        result
    );
}


// =========================
// Display Result
// =========================

function displayResult(result) {

    document.getElementById(
        "evaluation-result"
    ).innerHTML = `
        <h3>Total Score: ${result.total_score}</h3>

        <hr>

        <h4>Pronunciation</h4>

        <p>Score: ${result.pronunciation.score}</p>

        <p>
            Mispronounced Words:
            ${result.pronunciation.mispronounced_words.join(", ")}
        </p>

        <p>
            Missing End Sounds:
            ${result.pronunciation.missing_end_sounds.join(", ")}
        </p>

        <p>
            Vowel Issues:
            ${result.pronunciation.vowel_issues.join(", ")}
        </p>

        <hr>

        <h4>Overall Feedback</h4>

        <p>
            ${result.overall_feedback}
        </p>

        <hr>

        <h4>Study Plan</h4>

        <ul>
            ${result.study_plan.map(item => `<li>${item}</li>`).join("")}
        </ul>
    `;
}


// =========================
// Reset
// =========================

function resetPage() {

    currentQuestion = null;

    document.getElementById(
        "question-text"
    ).innerHTML =
        "Click 'Next Question'";

    document.getElementById(
        "evaluation-result"
    ).innerHTML =
        "Waiting for evaluation...";
}


// =========================
// Event Binding
// =========================

document
    .getElementById(
        "next-btn"
    )
    .addEventListener(
        "click",
        loadQuestion
    );

document
    .getElementById(
        "start-btn"
    )
    .addEventListener(
        "click",
        startRecording
    );

document
    .getElementById(
        "stop-btn"
    )
    .addEventListener(
        "click",
        stopRecording
    );

document
    .getElementById(
        "reset-btn"
    )
    .addEventListener(
        "click",
        resetPage
    );