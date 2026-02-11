# TECHIN 515 Individual Project: AI on Edge Devices

This is a capstone-like individual project: you define the problem, design the solution, evaluate the results, and justify every decision with evidence.

This project is not about building something that works once under ideal conditions. It's about understanding *why* it works, knowing when it fails, and justifying every design choice with data.

**Timeline:** 10 weeks (Week 10 = final demo)
**Estimated effort:** 6–8 hours per week
**Deliverables:** Proposal, weekly progress logs, evaluation, final report, live demo + presentation

---

## Theme: AI in Your Everyday Life

Your project must involve **machine learning deployed on an embedded system**. Beyond that, the application domain is yours to choose.

---

## Weekly Progress (Weeks 1–9)

Project management is part of this course. Each week, submit a brief progress log that demonstrates incremental work. The instructor will review these weekly as part of your assessment.

Each log should include:

- What you accomplished this week (with evidence: screenshots, serial output, code commits, plots)
- What you plan to do next week
- Any blockers or changes to your plan

**Reflection (include at least one per week):**

- What surprised you?
- What assumption turned out to be wrong?
- What would you do differently if starting over?

Weekly progress is assessed on evidence of consistent, incremental work, but NOT perfection. Falling behind without communicating is worse than falling behind with a revised plan.

---

## Proposal

Before writing any code, articulate **what you're building, why it matters, and how you'll know if it works.**

Your proposal (2–3 pages) must include:

1. **Project vision** — What are you building, who is it for, and why does it matter?
2. **Design target** — Define 3–5 measurable success criteria. Be specific enough that you can evaluate whether you met them at the end. (e.g., "≥85% accuracy across 5 classes, P95 latency < 200ms, battery life ≥ 6 hours on 1000mAh LiPo")
3. **Technical approach** — Hardware, software, data plan, ML pipeline. Include a system diagram.
4. **Dataset plan** — How many classes? How many samples per class? How will you ensure your test set represents real-world usage? How will you split training and test data? Note: these questions are not exhaustive and you should answer them whenever applicable.
5. **Timeline** — Weekly milestones for the full 10 weeks.
6. **Risks** — What could go wrong? What's your backup plan? Identify 2–3 risks and mitigation strategies.

**Guiding questions:**

- What accuracy / latency / power budget would make your system usable in the real world?
- What failure modes are unacceptable for your application?
- How will you know if your approach isn't working early enough to adjust?

**Minimum data bars:** We value scalable and systematic tests and validation.

**Ethics:** If your project involves biometric data (voice, gesture patterns, facial features), sensor data from people, or data collected in shared spaces, address privacy, consent, and potential misuse in your proposal and report. Refer to Lab 6's ethics framework for guidance.

The instructor will provide feedback after Week 1. Revise and resubmit by end of Week 2.

---

## Evaluation

Design and execute an evaluation that answers: *Does my system meet my design target, and why or why not?*

Before running tests, answer:

- What evidence would convince a skeptical reviewer that your system works (or doesn't)?
- Which performance dimensions matter most for YOUR application? Why those metrics?
- How many test trials do you need to have confidence in your results?
- What controlled experiments would reveal which design choices have the biggest impact on performance?
- When and why does your system fail?

You choose the metrics, test protocol, and analysis approach. Justify your methodology.

**Minimum bar:** At least 2 ablation studies isolating individual design choices, with quantitative results and interpretation.

**Guiding questions for your report:**

- Are failures random or systematic? What patterns do you see?
- Which design choice had the biggest impact on performance? On model size or latency?
- What resource constraints (latency, memory, power) matter for your scenario?
- If you had more time, what single change would most improve your system? Why?

> A system that achieves modest performance with deep analysis and evidence-based improvement proposals demonstrates stronger engineering than a system that achieves high performance with no understanding of why.

---

## Final Report

Your report (6–10 pages) should communicate:

1. What you built and why it matters
2. How you built it — architecture, data pipeline, model, deployment
3. Evidence of whether your system meets your design target — evaluation results, ablation findings, failure analysis
4. What you learned — limitations, surprises, trade-offs, ethical considerations
5. Whether your system is ready for real-world deployment (justify your answer)

Write for an audience of engineers unfamiliar with your project. Focus on design rationale and evaluation insights, not tutorial-style instructions.

Your project will be assessed on:

- **Engineering rigor** — Are design choices justified with evidence? Is evaluation systematic?
- **Critical thinking** — Do you understand why your system works (or fails)? Can you defend trade-offs?
- **Communication** — Can another engineer understand and replicate your work from your documentation?

---

## Final Demo & Presentation

- **Demo:** Show your system working in real-time with serial output visible. Have a backup video in case of hardware failure.
- **Poster:** Cover your approach, key evaluation findings, and lessons learned. 
- **Q&A:** Be prepared to defend your design choices and discuss trade-offs.

---

## FAQs

### Can I work with a partner?

No. This is an individual project. You may discuss high-level ideas with classmates, but all code, data collection, evaluation, and writing must be your own.

### Can I use pre-trained models or public datasets?

Yes, but you must justify why. If you use a pre-trained model, fine-tune it with your own data. If you use a public dataset, collect additional test data in your own environment. Using pre-trained models does NOT reduce expectations for evaluation rigor.

### What if my system doesn't meet my design target?

That's expected more often than not. The goal is rigorous engineering, not perfection. If you don't meet your target, your evaluation and discussion should explain *why* and propose evidence-based solutions. A thoughtful failure analysis is more valuable than hiding poor results.

### Can I pivot if my original idea doesn't work?

Yes, but document the pivot in your weekly progress logs. Explain what went wrong, what you learned, and how your new direction addresses those challenges. Consult the instructor before major pivots after Week 4.

### Can I use AI coding assistants?

Yes, but you are responsible for understanding and justifying every line of code. AI tools cannot design test protocols, analyze failure modes, or justify trade-offs for you.

