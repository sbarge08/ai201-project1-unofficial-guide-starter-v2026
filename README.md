# The Unofficial Guide

A small retrieval-augmented generation (RAG) system that answers questions about campus life using a local document corpus.

## Project Overview

This project builds a question-answering system over a `campus_life` corpus. The pipeline loads campus-life documents, splits them into chunks, embeds the chunks, retrieves relevant chunks for a question, checks whether the retrieved information is relevant enough to answer, and then generates a short grounded answer with source attribution.

The main goal is not just to produce an answer, but to make sure the answer is supported by the retrieved documents and that questions outside the corpus are rejected instead of answered from general knowledge.

## Pipeline

The system uses these main stages:

1. Load the `campus_life` documents.
2. Split documents into paragraph-level chunks.
3. Embed the chunks using `all-MiniLM-L6-v2`.
4. Store and retrieve the chunks using the vector store.
5. Apply a relevance cutoff of `0.6`.
6. Generate a short answer using the retrieved documents.
7. Require the generated answer to name the supporting source document.

The corpus contains 88 documents and produced 170 chunks.

The final chunking strategy keeps short heading/title paragraphs attached to the paragraph that follows them. This helps prevent a heading from being separated from the information it describes.

## Acceptance Criteria

The five acceptance criteria were written before the Unit 1 evaluation.

### 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that contains the answer.

This target reflects the fact that the `campus_life` corpus contains short posts where the answer is usually contained in one sentence or paragraph. A 4/5 target checks that retrieval works for most test questions without requiring every possible question to succeed.

### 2. Every answer names a source

Every answer the system produces names at least one source document.

Source attribution is part of the intended behavior of the generation step. Since answers are supposed to come from retrieved documents, every generated answer should identify where its information came from.

### 3. The relevance gate stops out-of-corpus questions

At least 4 of 5 out-of-scope questions should be rejected with an "I don't have enough information about that" response.

The system should avoid answering questions that are outside the `campus_life` corpus instead of generating unsupported answers. A 4/5 target checks that the relevance gate is useful for unrelated questions without requiring every possible unrelated question to behave identically.

### 4. Something about the chunks

At least 4 of 5 sampled chunks should be self-contained enough to answer a question without needing the surrounding chunk.

The corpus consists of short posts where useful information is usually contained in a sentence or paragraph. Keeping short headings with the paragraph that follows them makes the resulting chunks more understandable on their own.

### 5. Source attribution is correct

For at least 4 of my 5 test questions, the answer names a source document that actually contains information supporting the answer.

Retrieval alone does not guarantee that every retrieved document supports the final answer. This criterion checks that the source named in the final answer actually supports the information being used.

# Unit 2

## Run Log — Before

The baseline evaluation was run with:

- Corpus: `campus_life`
- Documents: 88
- Chunks: 170
- Embedding model: `all-MiniLM-L6-v2`
- Retrieval top-k: 5
- Relevance cutoff: 0.6
- In-scope questions: 5
- Runs per in-scope question: 3
- Caching: off
- Out-of-scope questions: 5

The baseline evaluation was recorded in:

`results/run_2026-09-21_1903_before.md`

The five in-scope questions were:

1. What time should students go to North Kitchen to avoid the busiest period between classes?
2. How much does laundry cost at Old Brewhouse?
3. How far ahead can students book a group study room?
4. How often does the campus shuttle run on weekdays?
5. What happens to junior and senior housing lottery applicants?

### Before results

| Measure | Result |
|---|---:|
| In-scope questions passing | 5/5 |
| In-scope runs passing | 15/15 |
| Out-of-scope questions rejected | 5/5 |
| Runs per in-scope question | 3 |

The baseline already met the numerical targets used by the evaluation.

### Real baseline outputs

**North Kitchen**

> Students should go before 11:45 to avoid the busiest period between classes.
> Source: `dining_north_kitchen_followup.txt`

**Old Brewhouse laundry**

> Laundry costs $1.50 per wash and $1.50 per dry.
> Sources included `housing_old_brewhouse.txt` and `housing_old_brewhouse_laundry.txt`.

**Group study rooms**

> Students can book a group study room up to two weeks ahead.
> Source: `study_group_rooms.txt`

**Campus shuttle**

> The campus shuttle runs every 20 minutes on weekdays.
> Source: `transit_shuttle.txt`

**Housing lottery**

> Rising sophomores are randomly assigned a number, while juniors and seniors are ordered by accumulated credit hours, with random tie-breaking when needed.
> Source: `admin_housing_lottery.txt`

The out-of-scope questions were rejected by the relevance gate rather than answered from outside knowledge.

## Verdicts

### Criterion 1 — Retrieved chunks contain the answer: Pass

All five in-scope questions passed the answer check on all three runs.

### Criterion 2 — Every answer names a source: Pass

The generated answers identified source documents for the information used in the answers.

### Criterion 3 — The relevance gate stops out-of-corpus questions: Pass

The relevance gate rejected all five out-of-scope questions.

### Criterion 4 — Something about the chunks: Pass

The sampled chunks were understandable without needing the surrounding chunk. The paragraph-level chunking strategy also keeps short headings attached to the paragraph that follows them.

### Criterion 5 — Source attribution is correct: Pass

For the five test questions, the named source documents contained information supporting the answers.

## Diagnoses

The before evaluation did not expose a failing numerical criterion. Retrieval was finding supporting information for the five tested questions, and the relevance gate rejected the five out-of-scope questions.

Because the measured criteria were already passing, changing the retrieval cutoff, chunking strategy, or test questions would not have been justified by a measured failure.

The main area I examined was answer grounding. Even when retrieval finds relevant documents, the generation step still needs to stay within the retrieved evidence and avoid adding unsupported details.

The diagnosis therefore focused on the generation instructions rather than changing the retrieval pipeline.

## The Improvement

I made one change to `generate.py`.

I tightened the grounding instructions given to the language model.

The updated instructions tell the model to:

- use only information directly supported by the retrieved documents;
- avoid guessing or filling in missing information;
- base important parts of the answer on the document that supports it;
- name the exact source filename;
- avoid combining details from different documents unless the documents support the same answer;
- keep the answer brief.

The purpose of this change was to make the generation step more explicitly grounded in the retrieved evidence.

The code change was committed before running the after evaluation.

## After Evaluation

The same five in-scope questions were evaluated again using the same evaluation process.

The after evaluation was recorded in:

`results/run_2026-09-21_1906_after.md`

| Measure | Before | After |
|---|---:|---:|
| In-scope questions passing | 5/5 | 5/5 |
| In-scope runs passing | 15/15 | 15/15 |
| Out-of-scope questions rejected | 5/5 | 5/5 |
| Runs per in-scope question | 3 | 3 |

All five in-scope questions passed on all three after runs.

The relevance gate again rejected all five out-of-scope questions.

The measured pass rates therefore did not change. The improvement made the grounding requirement more explicit, but the existing test set was already passing before the change, so the evaluation did not demonstrate a higher numerical score.

### Real after outputs

**North Kitchen**

> Students should go before 11:45 to avoid the busiest period between classes.
> Source: `dining_north_kitchen_followup.txt`

**Old Brewhouse laundry**

> Laundry costs $1.50 per wash and $1.50 per dry.
> Sources included `housing_old_brewhouse.txt` and `housing_old_brewhouse_laundry.txt`.

**Group study rooms**

> Students can book a group study room up to two weeks ahead.
> Source: `study_group_rooms.txt`

**Campus shuttle**

> The campus shuttle runs every 20 minutes on weekdays.
> Source: `transit_shuttle.txt`

**Housing lottery**

> Rising sophomores are randomly assigned a number, while juniors and seniors are ordered by accumulated credit hours, with random tie-breaking when needed.
> Source: `admin_housing_lottery.txt`

## What’s Still Broken

The current evaluation does not demonstrate whether the grounding change improves performance when retrieved documents are incomplete, ambiguous, or conflicting.

The five in-scope questions already passed before the change, so the current test set has limited ability to show an improvement in pass rate.

The current test set is also small and does not establish how the system behaves across a much larger variety of questions.

The evaluation does not yet include enough adversarial cases where the model could be tempted to invent information when the retrieved evidence is incomplete.

## What I’d Do Differently

I would add more difficult evaluation questions before making another improvement.

In particular, I would test questions where:

- two retrieved documents contain different details;
- the retrieved documents contain only part of the answer;
- the question is related to the corpus but cannot actually be answered from the retrieved text;
- several documents are relevant but only one directly supports the final answer;
- the model has an opportunity to fill in a missing detail from general knowledge.

I would also add tests specifically designed to measure whether the model invents information when the retrieved evidence is incomplete.

That would make the grounding improvement easier to measure because the baseline would have more opportunities to reveal a generation problem.

## How I Used AI

I used AI as a development and debugging assistant.

I used it to help reason through the RAG pipeline, inspect and explain Python errors, improve the chunking strategy, develop evaluation questions, write and refine the scorer, interpret evaluation results, and improve the grounding instructions.

I made the final implementation decisions and ran the evaluation commands myself. The evaluation results in this repository come from the actual project runs rather than from AI-generated claims about what the system would do.
