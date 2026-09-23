# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1 **before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something a person could plainly observe. *"Retrieval works"* is an opinion. *"For at least 4 of my 5 test questions, the top results include a chunk containing the answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a stricter or looser one. A reason that says something about your corpus or your pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that contains the answer.

**Why this target:**

The `campus_life` corpus contains short posts where the answer to a question is usually contained in one sentence or paragraph. I chose 4 of 5 because the retrieval system should find the supporting information for most test questions while still allowing one harder question to miss without making the criterion too strict.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**

The system is designed to answer from retrieved documents, so every generated answer should identify where its information came from. I chose every answer rather than 4 of 5 because source attribution is part of the expected behavior of the answer-generation step and should not depend on which question is asked.

---

## 3. The relevance gate stops out-of-corpus questions

At least 4 of 5 out-of-scope questions should be rejected with an "I don't have enough information about that" response.

**Why this target:**

The system should avoid answering questions that are outside the `campus_life` corpus instead of generating unsupported answers.

When I ask a question my documents clearly don't cover, the relevance gate stops it and the system returns "I don't have enough information about that" — in at least 4 of 5 tries.

**Why this target:**

I chose 4 of 5 because the relevance gate uses a fixed distance cutoff and the out-of-scope questions are intentionally unrelated to the corpus. A majority target checks that the gate is consistently useful without requiring every possible unrelated question to behave identically.

---

## 4. Something about your chunks

At least 4 of 5 sampled chunks should be self-contained enough to answer a question without needing the surrounding chunk.

**Why this target:**

The `campus_life` corpus is made up of short posts where useful information is usually contained in a sentence or paragraph. After keeping short headings with the paragraph that follows them, the sampled chunks are generally complete enough to understand on their own.

---

## 5. Source attribution is correct

For at least 4 of my 5 test questions, the answer names a source document that actually contains information supporting the answer.

**Why this target:**

My corpus has several documents that can be retrieved for a question, but retrieval alone does not guarantee that every retrieved document supports the final answer. I want the source named in the answer to be one that actually contains the information being used. I chose 4 of 5 because the source attribution should be correct for most test questions while allowing for one difficult retrieval case.

---

## Unit 2

### Criterion Verdicts

**Criterion 1 — Retrieved chunks contain the answer: Pass**

All five in-scope questions passed the answer check on all three runs.

**Criterion 2 — Every answer names a source: Pass**

The generated answers identified source documents for the information used in the answers.

**Criterion 3 — The relevance gate stops out-of-corpus questions: Pass**

The relevance gate rejected all five out-of-scope questions.

**Criterion 4 — Something about your chunks: Pass**

The sampled chunks were generally understandable without needing the surrounding chunk because the chunking strategy keeps paragraph-level information together and attaches short headings to the paragraph that follows them.

**Criterion 5 — Source attribution is correct: Pass**

For the five test questions, the named source documents contained information supporting the answers.

### Diagnosis

The before evaluation did not expose a failing criterion. The retrieval and relevance-gate behavior were already working for the tested questions.

The main area I examined was answer grounding. Even when the retrieval system finds relevant documents, the generation step still needs to stay within the retrieved evidence and avoid adding unsupported details.

Because the measured criteria were already passing, I did not change the retrieval cutoff, chunking strategy, or test questions.

### Unit 2 Improvement

I made one change to `generate.py`.

I tightened the grounding instructions given to the language model. The updated instructions tell the model to:

- use only information directly supported by the retrieved documents;
- avoid guessing or filling in missing information;
- base important parts of the answer on the document that supports them;
- name the exact source filename;
- avoid combining details from different documents unless the documents support the same answer;
- keep the answer brief.

The purpose of this change was to make the generation step more explicitly grounded in the retrieved evidence.

The same five in-scope questions were then evaluated again using the same evaluation process.

### After Evaluation

All five in-scope questions passed on all three after runs.

The relevance gate rejected all five out-of-scope questions.

The measured pass rates were unchanged:

| Measure | Before | After |
|---|---:|---:|
| In-scope questions passing | 5/5 | 5/5 |
| Out-of-scope questions rejected | 5/5 | 5/5 |
| Runs per in-scope question | 3 | 3 |

The change therefore did not increase the measured pass rate because the original system was already passing these tests. The purpose of the change was to make the grounding requirement more explicit in the generation instructions.

### What Is Still Broken

The current evaluation does not demonstrate that the grounding change improves performance on cases where the retrieved documents are incomplete, ambiguous, or conflicting.

The five in-scope questions already passed before the change, so the evaluation has limited ability to show an improvement in pass rate.

The current test set also does not establish how the system behaves across a much larger variety of questions.

### What I Would Do Differently

I would add more difficult evaluation questions before making another change.

In particular, I would test questions where:

- two retrieved documents contain different details;
- the retrieved documents contain only part of the answer;
- the question is related to the corpus but cannot actually be answered from the retrieved text;
- several documents are relevant but only one directly supports the final answer.

I would also add tests specifically designed to measure whether the model invents information when the retrieved evidence is incomplete.
