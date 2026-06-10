# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

Students reviews of professors across multiple departments. This knowledge is valueable because it captures real, experience-based information, with important factors included. Some factors these reviews include are exam difficulty, amount of homework, usefulness of office hours. Students have always made these reviews either by word of mouth, online posts, and other platforms so it made it hard to search for systematically. 

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 |professor_Sam.txt |review |/document/professor_Sam |
| 2 |professor_Megan.txt |review |/documentprofessor_Megan.txt|
| 3 |professor_Amanda.txt |review |/document/professor_Amanda.txt |
| 4 |professor_Brandon.txt |review |/document/professor_Brandon.txt |
| 5 |professor_Bradley.txt |review |/document/professor_Bradley.txt |
| 6 |professor_Maggie.txt |review |/document/professor_Maggie.txt |
| 7 |professor_Shi.txt |review |https://www.ratemyprofessors.com/professor/2498365|
| 8 |professor_Ryan.txt |review |/document/professor_Ryan.txt|
| 9 |professor_Curry.txt |review |https://www.ratemyprofessors.com/professor/2425272|
| 10 |professor_Denis.txt |review |/document/professor_Denis.txt|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
 Each line/paragraph is kept as its own chunk (approximately 50–150 characters).
**Overlap:**
None — documents are short enough that each sentence stands alone.
Removed extra whitespace, normalized line endings, and stripped blank lines using clean_text() in ingestion.py.
**Why these choices fit your documents:**
Reasoning: The source documents are short student reviews, typically 3–5 sentences each. Each sentence covers a distinct topic (exams, homework, office hours, lectures). Keeping sentences as individual chunks.
**Final chunk count:**
44 chunks across 10 documents 

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
 all-MiniLM-L6-v2 via sentence-transformers
**Production tradeoff reflection:**

 For a real deployment I would consider several factors. For accuracy on different phrasing, text-embedding-3-large (OpenAI) scores higher on natural language test but adds cost and API latency.

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
You are an assistant that answers questions about university professors
using only the student reviews provided to you.

Rules you must follow:
1. Answer ONLY using information from the documents below. Do not use
   any outside knowledge.
2. For every claim you make, cite the source file in parentheses,
   like: (professor_Sam.txt)
3. If the documents do not contain enough information to answer the
   question, respond with exactly: "I don't have enough information
   in the provided reviews to answer that."

**How source attribution is surfaced in the response:**
After the LLM generates its answer, the source filenames are collected directly from the retrieved chunk metadata.

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |Which professors have difficult exams? |Professor Bradley |Returned Bradley  with correct reasoning and citations |Relevant |Accurate |
| 2 |Which professors are helpful or easy to contact during office hours? |Professors Denis, Maggie, Brandon,Sam, Amanda  |Returned Brandon, Denis, Maggie — missed Sam and Amanda |partially |partially accurate |
| 3 |Which professors are considered fair graders? |Profesors Sam and Brandon |Returned Sam and Brandon |Relevant |Accurate |
| 4 |Which courses have difficult homework? | Professor Sam |Returned Sam as rank 1 with the correct chunk about difficult homework |relevant |accurate |
| 5 |Which professor has light or fun or easy or summarized lectures? | Maggie, Ryan, Denis |Returned Ryan, Maggie, Denis, and Bradley |relevant | |accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which professors are helpful or easy to contact during office hours?
**What the system returned:**
Brandon, Denis, and Maggie — only 3 of the 5 expected professors. Sam and Amanda were not retrieved.
**Root cause (tied to a specific pipeline stage):**
 This failure happens at the retrieval stage and is caused by synonym variation combined with short chunk size. 
**What you would change to fix it:**
erge consecutive sentences into larger chunks (~300–400 characters) so each chunk carries more context. 

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The requirement to write  planning.md before my code helped me organize the questions I wanted to ask and the expected answers. 
**One way your implementation diverged from the spec, and why:**
The actual chunks ended up smaller (50–150 characters) with no overlap — which worked for most queries but caused the synonym-matching failure on the office hours question.

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- My planning.md Retrieval Approach section (embedding model: all-MiniLM-L6-v2, top-k: 4) and my pipeline diagram, and asked Claude to generate embed.py and retrieve.py.
- *What it produced:*
- Working ChromaDB integration code with a verify_load() function and a print_results() function with distance score flags.
- *What I changed or overrode:*
I identified that the chunk IDs would collide across documents because chunk_number resets to 0 for each file — so professor_Sam.txt chunk 0 and professor_Megan.txt chunk 0 would both get ID "0" and one would silently overwrite the other in ChromaDB. I directed Claude to fix this by combining the source filename with the chunk number to produce unique IDs like professor_Sam.txt_chunk_0.
**Instance 2**

- *What I gave the AI:*
- My grounding requirement (answers from retrieved context only, with source attribution), the output format I wanted (answer + source list), and asked Claude to generate query.py and app.py.
- *What it produced:*
- A query.py with a Groq API call and a system prompt, and an app.py using Gradio.
- *What I changed or overrode:*
The original system prompt said to "acknowledge" when information was insufficient but didn't specify exact wording. I directed Claude to add rule #3 with an exact refusal phrase so the out-of-scope behavior would be consistent and testable. I also directed Claude to switch from Gradio to Streamlit after Gradio failed to install on Python 3.14 — Claude produced a working Streamlit version that preserved all the same input and output fields.
