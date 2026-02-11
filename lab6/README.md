# TECHIN 515 – Lab 6: Speaker Identification on the Edge

You will build a speaker identification system that runs on a microcontroller using an I2S MEMS microphone. The system must distinguish between enrolled speakers and reject unknown ones. You will then evaluate your system's trade-offs — accuracy vs. latency vs. power vs. privacy — through systematic testing and ablation studies.

> **Important**: Voice is **identity data**. This lab includes mandatory ethics and data-handling requirements. Treat all recordings as sensitive.

---

## Learning Objectives

By completing this lab you will:

1. Build an **end-to-end embedded ML pipeline from scratch**: data collection → feature extraction → model training → on-device deployment → decision logic.
2. Design and justify a **repeatable test protocol** with quantitative evidence.
3. Perform **ablation studies** to support design decisions with data, not intuition.
4. Analyze key edge trade-offs: accuracy vs. latency, latency vs. battery life, thresholding vs. error rates, model size vs. memory constraints, privacy risk vs. utility.
5. Communicate engineering decisions concisely in a technical report.

---

## Hardware Requirements

- **ESP32 DevKit** — any variant with I2S support
- **INMP441 I2S MEMS Microphone** — [datasheet (PDF)](https://invensense.tdk.com/wp-content/uploads/2015/02/INMP441.pdf)
- **Push button**
- **LED** — built-in or external
- **Breadboard + jumper wires**
- **LiPo battery (3.7V, 500 mAh+)** — for battery estimation
- **Slide switch** — power switch (optional)

Use the INMP441 datasheet to determine the correct wiring to your ESP32. Note that the ESP32 I2S peripheral has **software-configurable pins** — you choose which GPIOs to use for WS, SCK, and SD in your code.

---

## Software Requirements

- **Arduino IDE** (2.x) or PlatformIO with ESP32 board package
- **Python 3.11+** — choose your own libraries for data collection, parsing, and analysis
- **Edge Impulse Studio** account ([studio.edgeimpulse.com](https://studio.edgeimpulse.com)) — free tier is sufficient

---

## Ethics + Data Governance (Mandatory)

### 1) Consent and classroom dynamics

Voice is biometric identity data. You must:

1. Ask each participant for explicit consent to record their voice for this lab.
2. Allow an easy opt-out with no penalty.
3. Respect withdrawal: if someone withdraws, delete their data and do not use it.

Prepare a consent form (you can search for templates online) and have your participants sign it before data collection.

### 2) Data minimization rules

1. Use **pseudonymous IDs** only: `S1`, `S2`, etc. No names, no student IDs.
2. Use a **neutral passphrase** (provided below) — do not record personal information.
3. Do not upload raw audio to any public repository or public dataset.
4. Depending on data management policy in your consent form, keep raw data local to your machine or in private course storage only, or remove all data after lab completion.

### 3) Passphrase

All recordings must use the same phrase:

> "AI runs on edge"

Speak the passphrase at natural pace. Configure your audio capture window to accommodate the full utterance.

**Question:** You are using a fixed passphrase for all speakers. Consider two scenarios: (a) a system trained on "AI runs on edge" but tested with a different phrase, (b) a system where each speaker says a unique sentence. How would you design an experiment to determine whether your model is recognizing *who* is speaking vs. *what* is being said? What would you measure?

### 4) Ethics questions

Answer these in your report:

1. What are two realistic misuse scenarios for speaker identification?
2. Which is more dangerous in your chosen use case: false accept or false reject? Why?
3. What data-handling policy would you recommend for a real product (retention, access control, deletion)?
4. If a user revokes consent after model training, is deleting their audio sufficient? What about the trained model weights?

---

## What You Must Build

Your final system must:

1. **Record** a short audio window from the microphone.
2. **Classify** the speaker as one of K enrolled speakers or "Unknown."
3. **Handle unknowns** — reject low-confidence predictions.
4. **Indicate** the result via LED, serial output, or another actuator of your choice.
5. **Log results** in a structured, machine-readable format that you design. Include at minimum: predicted label, confidence, and timing metrics (capture time, inference time, total time).
6. **Support two operating modes:**
   - **Push-to-talk**: system is idle until a button press triggers capture → inference → result.
   - **Battery-aware**: system continuously monitors audio energy and only runs inference when speech energy exceeds a threshold.

   These modes are mutually exclusive. You may switch between them via a serial command, a hardware switch, or another mechanism of your choosing.

---

## Part 0 — Define Your Design Target

Before you start building, specify your target scenario in writing:

- **Objective:** e.g., "Maximize accuracy for 5 enrolled speakers" or "Minimize latency for a smart doorbell"
- **Measurable success criteria:** e.g., ">=85% accuracy, P95 latency < 2 seconds"
- **Acceptable trade-offs:** e.g., "Willing to accept 10% false reject rate to keep false accept rate below 5%"

**Example:** *"I am building a study-room access system for 5 people. My target is >=80% accuracy with <2s latency. I prioritize low false-accept rate (security) and accept higher false-reject rate (users can try again)."*

> **Checkpoint 0:** Write your design target before proceeding. You will revisit it at the end to evaluate whether you met it.

---

## Part 1 — Data Collection

Collect a labeled audio dataset for training and evaluation. Before you start, think through:

- How many samples per speaker do you need for reliable training and evaluation? Justify your choice.
- What diversity do your samples need (different sessions, environments, microphone distances)?
- How will you split data for training vs. testing? Why does the split strategy matter? (Hint: consider what changes between recording sessions — background noise, microphone position, speaker fatigue, room acoustics — and what a random split would fail to test.)
- How will you handle the "Unknown" class — who speaks for it, and how many samples?

**Minimum requirements:** At least 5 enrolled speakers, recorded across 5 sessions, with a held-out session for testing.

You will need to build a data collection pipeline — for example, a Python script that reads audio from the ESP32 serial port and saves WAV files, or another approach of your choosing.

> **Checkpoint 1:** Report your thought process to the questions at the beginning of this part. Report your dataset design: counts per speaker, session split strategy, and justification for your choices. Reflection: if you had to double your dataset, where would you add samples — more speakers, more sessions per speaker, or more utterances per session? Why would that addition improve your model the most?

---

## Part 2 — Model Pipeline

Train a speaker identification model using Edge Impulse (or another framework if you prefer, as long as you can deploy to ESP32).

Consider:

- What audio features are relevant for distinguishing speakers?
- How do your feature extraction and classifier choices affect accuracy, model size, and inference time?
- What trade-offs exist between model complexity and ESP32 memory/compute constraints?

Perform **ablation studies** — systematically vary at least 2 design choices, one at a time, while holding everything else constant. For example, you might hold the classifier fixed and vary the feature extraction method, then hold features fixed and vary the classifier architecture. For each variation, record accuracy, model size (KB), and estimated inference time. Justify your final model selection with evidence.

> **Checkpoint 2:** Report your ablation results and explain why you chose your final model. Justify why your ablation studies are important to the project.

---

## Part 3 — On-Device Deployment

Write an Arduino sketch from scratch that:

1. Initializes the microphone
2. Captures audio windows on button press (push-to-talk mode)
3. Runs your exported model for inference
4. Applies your unknown-handling strategy (e.g., confidence thresholding, training an explicit Unknown class, or another approach — justify your choice)
5. Actuates an LED or other indicator based on the prediction
6. Logs results in your structured format with timing information
7. Implements battery-aware mode with an energy gate

> **Checkpoint 3:** Demonstrate push-to-talk mode working with serial output visible. Reflection: compare your measured on-device inference time to the Edge Impulse estimate. If they differ significantly, hypothesize why.

---

## Part 4 — Evaluation

"It worked once" is not a valid piece of evidence. Design a test protocol that would convince a skeptical reviewer your system meets (or fails to meet) your design target from Part 0.

Before running tests, answer:

- What does "working correctly" mean for your specific application?
- What failure modes matter most? (Refer back to your design target)
- How many test trials do you need to have confidence in your results? (Hint: if you run 10 trials and observe 80% accuracy, how confident are you that the true accuracy is near 80%? Consider how sample size affects uncertainty.)
- What metrics will you compute, and why those metrics? Think beyond accuracy — what other measures capture the failure modes you care about?
- How will you label ground truth during testing?

Run your tests, parse your logs, and analyze the results. Write your own analysis scripts or notebook.

**Guiding questions for your report:**

- Where does your system fail? Are failures random or systematic?
- What is the relationship between your confidence threshold and different types of errors?
- Is your system fast enough for interactive use?
- Did you meet your design target? If not, what would you change?

> **Checkpoint 4:** Report your evaluation methodology and key findings. What is your system's biggest strength and biggest weakness?

---

## Part 5 — Battery Awareness

Your battery-aware mode should gate inference using audio energy — do not run the ML classifier when the room is quiet.

Research or measure the ESP32's power consumption in different operating states. Using a 500 mAh LiPo battery, estimate battery life for:

1. **Push-to-talk only** (idle between button presses)
2. **Always-listening without energy gate** (continuous inference)
3. **Always-listening with your energy gate** (use your measured gate skip rate)

**Guiding question:** How does your energy threshold choice affect the trade-off between battery life and missed detections?

> **Checkpoint 5:** Report your energy gate skip rate and estimated battery life improvement. Reflection: test your energy gate in a noisy environment (e.g., with background conversation or music). Does your skip rate change? How would this affect your design target?

---

## Submission Requirements

### Directory structure

An example to your project directory is as follows.
```
lab6-submission/
├── README.md                    # Your report (or separate PDF)
├── speaker_id_esp32/
│   └── speaker_id_esp32.ino     # Your complete sketch
├── scripts/                     # Your data collection, parsing, and analysis scripts
├── data/                        # DO NOT upload raw audio to public repos
│   └── (keep local or in private storage)
├── results/                     # Parsed results, plots, analysis output
└── demo_video.mp4               # Demo video (max 3 minutes)
```

### Report contents

Your README or report PDF must include:

1. Answers to all questions
2. **Design target** (Part 0)
3. **Dataset design** — counts per speaker, session strategy, justification
4. **Model pipeline** — feature extraction and classifier choices, ablation results (>= 2 variables), model selection rationale
5. **Evaluation** — test protocol design, chosen metrics with justification, analysis of results, failure mode discussion
6. **Battery awareness** — energy gate behavior, battery life estimates with reasoning
7. **Final recommendation** — justify your model, threshold, and gate choices with >= 3 quantitative findings

### Demo video (max 3 minutes)

Show:

1. Push-to-talk identification for at least 2 enrolled speakers + an Unknown speaker
2. Battery-aware mode showing the energy gate behavior (when it skips vs. when it runs inference)
3. Serial output visible on screen
