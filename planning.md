# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

What domain did you choose? 
- The chosen domain is the Unofficial GWU Freshman Computer Science Student Survival Guide. It provides a student-to-student playbook covering introductory CS class rigor, local tech internship navigation, freshman housing choices,dining realities, course registration, and urban campus adaptation at George Washington University.

Why is this knowledge valuable and hard to find through official channels? 
- This knowledge is valuable because it helps incoming students set realistic expectations, make informed decisions about their academic and social lives, and navigate the unique challenges of being a freshman in a large urban university setting. It can reduce anxiety, improve student satisfaction, and enhance the overall college experience by providing practical advice that is not available through official channels. It can also foster a sense of community and support among new students by sharing insights from those who have recently gone through similar experiences.

- The information is hard to find through official channels because it is often anecdotal, subjective, and rapidly changing based on student experiences, which are not typically documented in formal university resources. By compiling this knowledge into a single guide, it provides a more comprehensive and accessible resource for new students. 
---

## Documents

The Unofficial GWU Freshman Computer Science Student Survival Guide.

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit | Pacing and rigor of early computer science classes. | https://www.reddit.com/r/gwu/comments/1dxy9a3/how_is_the_computer_science_at_gwu_incoming/ |
| 2 | Reddit | Managing coding anxiety as a new student. | https://www.reddit.com/r/gwu/comments/1dxy9a3/how_is_the_computer_science_at_gwu_incoming/ |
| 3 | Reddit | Local tech market jobs and student internships. | https://www.reddit.com/r/gwu/comments/1b2u2ih/cs_jobs/ |
| 4 | Reddit | Student life inside the engineering department. | https://www.reddit.com/r/gwu/comments/62m1d2/computer_science_at_gw/ |
| 5 | Reddit | How the freshman housing lottery works. | https://www.reddit.com/r/gwu/comments/1pyc0s6/how_to_get_the_dorm_you_want_as_a_first_year/ |
| 6 | Reddit | Living on the Mount Vernon campus. | https://www.reddit.com/r/gwu/comments/1k6aax4/chances_of_residence_hall_i_want/ |
| 7 | Reddit | Finding centrally located freshman dorms. | https://www.reddit.com/r/gwu/comments/gwsp0i/gwu_housing/ |
| 8 | Reddit | Swapping rooms if the lottery fails. | https://www.reddit.com/r/gwu/comments/8ouwev/i_didnt_get_any_of_my_15_housing_choices/ |
| 9 | Reddit | Social environments of different residence halls. | https://www.reddit.com/r/gwu/comments/1jvbdjc/incoming_student_housing_questions/ |
| 10 | Reddit | Strategy hacks for high-stress class registration. | https://www.reddit.com/r/gwu/comments/i34t90/registration_tipschances/ |
| 11 | Reddit | Brutally honest reviews of campus dining halls. | https://www.reddit.com/r/gwu/comments/1bw4x7a/my_honest_review_on_gw_dining/ |
| 12 | Reddit | Secret quiet spots to study on and off campus. | https://www.reddit.com/r/gwu/comments/1kh4lqw/favorite_study_spots/ |
| 13 | Reddit | Moving in, making friends, and freshman dorm advice. | https://www.reddit.com/r/gwu/comments/14kcb90/general_advice_for_freshmen/ |
| 14 | Reddit | Honest breakdown of Greek life vs. DC nightlife options. | https://www.reddit.com/r/gwu/comments/1b8b92n/social_scene_in_gw/ |
| 15 | Reddit | Navigating the D.C. Metro system and going carless. | https://www.reddit.com/r/gwu/comments/1may8rf/commuting_by_metro/ |
| 16 | Reddit | Campus safety, city life tips, and night walking alerts. | https://www.reddit.com/r/gwu/comments/137uaqr/campus_safety/ |

---

* Specific questions the system should handle:

1. What do students say about the pacing and rigor of early computer science classes at GWU?
2. Is the freshman housing lottery actually random, or does the placement matrix favor certain preferences?
3. What are the best strategies for navigating the high-stress course registration process at GWU?
4. What are the realistic pros and cons of living on the Mount Vernon campus versus Foggy Bottom dorms like Thurston Hall?
5. What do students say about the quality and variety of food at GWU dining halls?
6. How can an incoming freshman maximize their chances of securing early local tech internships or staff positions in the D.C. area?
7. What are the best quiet study spots on and off campus according to students?
8. How do students describe the social scene at GWU, particularly the tradeoffs between Greek life and D.C. nightlife?
9. What safety tips do students share for navigating campus and the city, especially at night?
10. What advice do students give for making friends and adjusting to freshman dorm life at GWU?
11. What do students say about the D.C. Metro system and commuting without a car?
12. What are the most common sources of stress for GWU freshmen, and how do students recommend managing them?
13. What are the best resources for finding student reviews of professors and courses at GWU?
14. How do students describe the workload and time management challenges of being a freshman at GWU?

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

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

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
