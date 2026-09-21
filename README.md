# The Unofficial Guide

## Unit 1

## What This Does

I picked the `campus_life` corpus, which contains short posts about campus life, housing, dining, courses, transportation, and other student information.

The system loads these documents, splits them into meaningful chunks, creates embeddings, and searches for the chunks most relevant to a student's question. It then uses the retrieved information to generate a grounded answer and name the source document.

If the question is outside the corpus, a relevance gate stops the system from calling the language model.

## Chunking Strategy

**Chunk size:** Variable, based on paragraph boundaries.

**Overlap:** None.

I changed the starter's fixed-size character-window approach because the `campus_life` documents are mostly short posts where the useful information is usually contained in one sentence or paragraph.

I split documents at paragraph boundaries instead of cutting them at an arbitrary character count. I also kept short heading/title paragraphs together with the paragraph that follows them. This prevents a short heading from being separated from the information that explains it.

For the `campus_life` corpus, this produced 170 chunks from 88 documents, with an average of 163 characters per chunk. The shortest chunk was 65 characters and the longest was 397 characters.

The function that produces these chunks is `chunker.py::split_documents`.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

> On the add/drop deadline
>
> You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

**Chunk 2** — source: `advising_registration.txt#1` — produced by: `chunker.py::split_documents`

> Registration times are staggered by credit hours, same as the housing lottery. Popular courses fill in the first two days.

**Chunk 3** — source: `course_cs_340_workload.txt#0` — produced by: `chunker.py::split_documents`

> Workload for CS 340 Databases
>
> People keep asking so: 6 hours a week early, 15 in the last three weeks when the project lands. That's real time, not optimistic time.

**Chunk 4** — source: `course_hist_118_exams.txt#1` — produced by: `chunker.py::split_documents`

> The essay rubric is posted in week 2 and it's followed exactly — read it early.

**Chunk 5** — source: `course_stat_150_exams.txt#0` — produced by: `chunker.py::split_documents`

> STAT 150 Applied Statistics — assessment
>
> Three equally weighted midterms, no final. No curve, but the lowest midterm is dropped.

## Sample Answer

**Question:** How much does laundry cost at Old Brewhouse?

**Answer:** Laundry costs $1.50 for a wash and $1.50 for a dry at Old Brewhouse (housing_old_brewhouse.txt and housing_old_brewhouse_laundry.txt).

**Source:** `housing_old_brewhouse.txt` and `housing_old_brewhouse_laundry.txt`

**Relevance cutoff:** 0.6

## Unit 2

### Before Evaluation

I ran the five test questions three times before making my Unit 2 change.

All five in-scope questions passed on all three runs.

The five out-of-scope questions were all rejected by the relevance gate. The gate refused 5 out of 5 out-of-scope questions.

The best retrieval distances for the five in-scope questions were:

| Question | Best distance |
|---|---:|
| North Kitchen busiest period | 0.298 |
| Old Brewhouse laundry cost | 0.221 |
| Group study room booking | 0.236 |
| Campus shuttle frequency | 0.182 |
| Junior and senior housing lottery | 0.262 |

### What I Changed

I changed the grounding instructions in `generate.py`.

The original instructions already told the model to use only the provided documents and name the source filename. I made the instructions more specific by telling it to use information directly supported by the retrieved documents, avoid filling in missing details, and avoid combining details from different documents unless the documents support the same answer.

I made this change because the system is supposed to give answers grounded in the retrieved corpus rather than relying on information from outside the corpus.

### After Evaluation

I ran the same five questions three times after the change.

All five in-scope questions passed on all three runs.

The relevance gate also rejected all five out-of-scope questions.

| Measure | Before | After |
|---|---:|---:|
| In-scope questions passing | 5/5 | 5/5 |
| Out-of-scope questions rejected | 5/5 | 5/5 |
| Runs per in-scope question | 3 | 3 |

The main change was to make the grounding instructions more explicit. The existing tests were already passing before the change, so the after evaluation did not show a change in the pass rate. The change was intended to make the answer-generation behavior more clearly grounded in the retrieved evidence.

## How I Used AI

**1.**

I used AI when I got stuck understanding how the starter `chunker.py` worked. I used it to explain what the existing code was doing and to help me think through a better way to split the campus-life posts. I then changed `chunker.py` and tested the chunks myself with the provided commands.

**2.**

I used AI when I was testing the question-answering system. It helped me decide which questions to test and helped me interpret the retrieval distances and source documents. I ran the commands myself and used the results to decide that the 0.6 relevance cutoff was working for my test questions.

**3.**

For Unit 2, I used AI to help me understand the evaluation output and troubleshoot the scorer format. I checked the starter `run_eval.py` to make sure my `scorer.py` used the required `judge(question, expects, answer, results)` function. I then ran the before and after evaluations myself.