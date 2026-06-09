# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
The domain I used was, professore reviews from students. The descriptions include a teacher's names with the course they teach then the exam difficulty, grading fairness, and course workload.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |professor1.txt |Student Review created for Professor Sam's BIO100.|docuements/professor1.txt|
| 2 |professo21.txt  |Student Review created for Professor Sam's BIO100. |docuements/professor1.txt |
| 3 |professor3.txt  |Student Review created for Professor Amanda's CHEM100. |docuements/professor1.txt |
| 4 |professor4.txt  |Student Review created for Professor Brandon's AI100. |docuements/professor1.txt |
| 5 |professor5.txt  |Student Review created for Professor Bradley's CSC100. |docuements/professor1.txt |
| 6 |professo61.txt  |Student Review created for Professor Maggie's FIN300. |docuements/professor1.txt |
| 7 |rate my professor |A real review from a student on rate my professor about Professor Shi's CSC211. |https://www.ratemyprofessors.com/professor/2498365 |
| 8 |professor8.txt  |Student Review created for Professor Ryan's CSC200.|docuements/professor1.txt |
| 9 |rate my professor |A real review from a student on rate my professor fro Professor Richard Curry's COM100.|https://www.ratemyprofessors.com/professor/2425272 |
| 10 |professor10.txt  |Student Review created for Professor Denis's A1400. |docuements/professor1.txt |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
125 characters
**Overlap:**
25 characters
**Reasoning:**
My documents are short reviews, not long text documents. A 300 charcater chunk should keep related information together, such as offic hours, etc. A 50 character overlap prevents information from being split between chunks.

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:**4

**Production tradeoff reflection:**
For this project all0MiniLM-L6-v2 is my choice becuase it's free and runs locally.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |Which professors have difficult exams? |Professor Amanda and Bradley have difficult exams.|
| 2 |Which professors are helpful or easy to contact during office hours? |Professor Denis, Maggie, Bradley, Amanda, and Sam are helpful or easy to contact.|
| 3 |Which professors are considered fair graders? |Professor Sam is reviewed to be a fair grader. |
| 4 |Which courses have diffcult homework? |Professor Sam has diffcult homework. |
| 5 |Which professor has light or fun or easy or summarized lectures?|Professor Bradley, Maggie, Ryan, and Denis. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The wording of each review varies, I used a lot of synonyms.

2.Missing attributes

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---
Documents->Document ingestion, file reading->Chunking/Cleaning-> Embedding using sentence-transformers->vector store->retrieval of top 4 chunks for user question->generation-> grounded answer with source citation

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->


**Milestone 3 — Ingestion and chunking:**
I will use Claude to help me understand how to plan my python code, that cleans extra white space, splits text into 300 character chunks with 50 character overlap. 

**Milestone 4 — Embedding and retrieval:**
I will use AI to help connect a sentence transformers with ChromeDB. I will provide the retrieval approach, embedding model, and top k-value to Claude and recieve an implementation for retrieval of top 4 chunks for question.

**Milestone 5 — Generation and interface:**
I will use Claude to help me verify and implement a grounded prompt for Groq that answers only from retrived chunks. 
