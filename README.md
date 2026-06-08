# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

What topic or category of knowledge does your system cover?
- The chosen domain is the Unofficial GWU Freshman Computer Science Student Survival Guide. It provides a student-to-student playbook covering introductory CS class rigor, local tech internship navigation, freshman housing choices,dining realities, course registration, and urban campus adaptation at George Washington University.

Why is this knowledge valuable and hard to find through official channels? 
- This knowledge is valuable because it helps incoming students set realistic expectations, make informed decisions about their academic and social lives, and navigate the unique challenges of being a freshman in a large urban university setting. It can reduce anxiety, improve student satisfaction, and enhance the overall college experience by providing practical advice that is not available through official channels. It can also foster a sense of community and support among new students by sharing insights from those who have recently gone through similar experiences.

- The information is hard to find through official channels because it is often anecdotal, subjective, and rapidly changing based on student experiences, which are not typically documented in formal university resources. By compiling this knowledge into a single guide, it provides a more comprehensive and accessible resource for new students. 

---

## Document Sources

The Unofficial GWU Freshman Computer Science Student Survival Guide.

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit | Pacing and rigor of early computer science classes. | https://www.reddit.com/r/gwu/comments/1dxy9a3/how_is_the_computer_science_at_gwu_incoming/ |
| 2 | Reddit | Local tech market jobs and student internships. | https://www.reddit.com/r/gwu/comments/1b2u2ih/cs_jobs/ |
| 3 | Reddit | Student life inside the engineering department. | https://www.reddit.com/r/gwu/comments/62m1d2/computer_science_at_gw/ |
| 4 | Reddit | How the freshman housing lottery works. | https://www.reddit.com/r/gwu/comments/1pyc0s6/how_to_get_the_dorm_you_want_as_a_first_year/ |
| 5 | Reddit | Living on the Mount Vernon campus. | https://www.reddit.com/r/gwu/comments/1k6aax4/chances_of_residence_hall_i_want/ |
| 6 | Reddit | Finding centrally located freshman dorms. | https://www.reddit.com/r/gwu/comments/gwsp0i/gwu_housing/ |
| 7 | Reddit | Swapping rooms if the lottery fails. | https://www.reddit.com/r/gwu/comments/8ouwev/i_didnt_get_any_of_my_15_housing_choices/ |
| 8 | Reddit | Social environments of different residence halls. | https://www.reddit.com/r/gwu/comments/1jvbdjc/incoming_student_housing_questions/ |
| 9 | Reddit | Strategy hacks for high-stress class registration. | https://www.reddit.com/r/gwu/comments/i34t90/registration_tipschances/ |
| 10 | Reddit | Brutally honest reviews of campus dining halls. | https://www.reddit.com/r/gwu/comments/1bw4x7a/my_honest_review_on_gw_dining/ |
| 11 | Reddit | Secret quiet spots to study on and off campus. | https://www.reddit.com/r/gwu/comments/1kh4lqw/favorite_study_spots/ |
| 12 | Reddit | Moving in, making friends, and freshman dorm advice. | https://www.reddit.com/r/gwu/comments/14kcb90/general_advice_for_freshmen/ |
| 13 | Reddit | Honest breakdown of Greek life vs. DC nightlife options. | https://www.reddit.com/r/gwu/comments/1b8b92n/social_scene_in_gw/ |
| 14 | Reddit | Navigating the D.C. Metro system and going carless. | https://www.reddit.com/r/gwu/comments/1may8rf/commuting_by_metro/ |
| 15 | Reddit | Campus safety, city life tips, and night walking alerts. | https://www.reddit.com/r/gwu/comments/137uaqr/campus_safety/ |

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


## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

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

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

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
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
