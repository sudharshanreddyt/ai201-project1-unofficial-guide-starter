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
| 1 | Reddit(r/gwu) | Pacing and rigor of early computer science classes. | https://www.reddit.com/r/gwu/comments/1dxy9a3/how_is_the_computer_science_at_gwu_incoming/ |
| 2 | Reddit(r/gwu) | Local tech market jobs and student internships. | https://www.reddit.com/r/gwu/comments/1b2u2ih/cs_jobs/ |
| 3 | Reddit(r/gwu) | Student life inside the engineering department. | https://www.reddit.com/r/gwu/comments/62m1d2/computer_science_at_gw/ |
| 4 | Reddit(r/gwu) | How the freshman housing lottery works. | https://www.reddit.com/r/gwu/comments/1pyc0s6/how_to_get_the_dorm_you_want_as_a_first_year/ |
| 5 | Reddit(r/gwu) | Living on the Mount Vernon campus. | https://www.reddit.com/r/gwu/comments/1k6aax4/chances_of_residence_hall_i_want/ |
| 6 | Reddit(r/gwu) | Finding centrally located freshman dorms. | https://www.reddit.com/r/gwu/comments/gwsp0i/gwu_housing/ |
| 7 | Reddit(r/gwu) | Swapping rooms if the lottery fails. | https://www.reddit.com/r/gwu/comments/8ouwev/i_didnt_get_any_of_my_15_housing_choices/ |
| 8 | Reddit(r/gwu) | Social environments of different residence halls. | https://www.reddit.com/r/gwu/comments/1jvbdjc/incoming_student_housing_questions/ |
| 9 | Reddit(r/gwu) | Strategy hacks for high-stress class registration. | https://www.reddit.com/r/gwu/comments/i34t90/registration_tipschances/ |
| 10 | Reddit(r/gwu) | Brutally honest reviews of campus dining halls. | https://www.reddit.com/r/gwu/comments/1bw4x7a/my_honest_review_on_gw_dining/ |
| 11 | Reddit(r/gwu) | Secret quiet spots to study on and off campus. | https://www.reddit.com/r/gwu/comments/1kh4lqw/favorite_study_spots/ |
| 12 | Reddit(r/gwu) | Moving in, making friends, and freshman dorm advice. | https://www.reddit.com/r/gwu/comments/14kcb90/general_advice_for_freshmen/ |
| 13 | Reddit(r/gwu) | Honest breakdown of Greek life vs. DC nightlife options. | https://www.reddit.com/r/gwu/comments/1b8b92n/social_scene_in_gw/ |
| 14 | Reddit(r/gwu) | Navigating the D.C. Metro system and going carless. | https://www.reddit.com/r/gwu/comments/1may8rf/commuting_by_metro/ |
| 15 | Reddit(r/gwu) | Campus safety, city life tips, and night walking alerts. | https://www.reddit.com/r/gwu/comments/137uaqr/campus_safety/ |

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
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers) -->

**Chunk size: 500**
The 500-character chunk size allows for capturing complete thoughts and advice without splitting sentences or key information across chunks. This is particularly important for Reddit posts, which often contain multiple paragraphs of advice and discussion. A smaller chunk size might split important context, while a larger chunk size could make retrieval less precise.

**Overlap: 100**
The 100-character overlap handles edge cases where key proper nouns (such as specific residence halls like Thurston or District, or specific course codes like CSCI 1111) occur near split boundaries, guaranteeing that either adjacent chunk retains enough surrounding semantic context to be matching and retrievable.

**Preprocessing**

The scraper (`scraper.py`) and ingestion pipeline (`ingest.py`) apply the following preprocessing steps before any text reaches the chunker:

1. **HTML removal and entity decoding** - Removed residual HTML tags and decoded HTML entities. This ensures only clean prose reaches the chunker.

2. **Boilerplate tag removal** - For non-Reddit pages, a regex pattern matches element class/id/role attributes and those HTML elements are decomposed from the parse tree before text extraction. This prevents navigation menus and ads from polluting the corpus.

3. **Whitespace normalisation** - Multiple consecutive spaces/tabs on the same line are collapsed to a single space and runs of three or more newlines are collapsed to exactly two, preserving paragraph structure without excessive blank lines.

4. **Structural label extraction — post title and post body separation** - Each cleaned file contains scraping artefact markers: `POST TITLE <title>` and `POST BODY`. A three-state parser separates these sections:  
   - `POST TITLE` is extracted as the `doc_title` metadata field.  
   - `POST BODY` (the original Reddit question) is extracted as the `post_body` metadata field — it is stored in ChromaDB metadata for LLM context but is **not** included in chunk text, since the original question is not an answer.  
   - Everything after the first blank line following the post body (the community comments and replies) becomes the `text` field that is actually chunked and embedded.

5. **Deleted/removed comment filtering** - Comments where the `deleted` CSS class is present, or whose body text equals `"[deleted]"` or `"[removed]"`, are skipped entirely and never written to disk.

**Why these choices fit your documents:**
The 500-character chunk size with 100-character overlap is effective for Reddit posts because it preserves the conversational context of discussions, ensures that nuanced advice and anecdotes are not cut off mid-sentence, and handles the variability in post length while maintaining sufficient context for retrieval accuracy.

**Final chunk count:** 109

**5 labeled sample chunks with their source document name**

**Chunk 1** — Source: `campus_safety` (chunk 0)
```
Police alerts are common but don't let them get you paranoid. There is police activity
everywhere all the time in cities, especially DC, they just don't send out alerts every
time they are nearby. 99% of time the GW ones are followed up with an all clear within
20 minutes, and most of them are technically "off campus" or on the outskirts. GW campus
is quiet and doesn't have many issues, just follow regular city rules like not walking
alone at 2am and not flaunting any expensive items. The "worst
```

**Chunk 2** — Source: `cs_jobs` (chunk 0)
```
You can get jobs, just not student employment jobs. You can apply to be staff. Most on
campus internships are restricted to current students.

I heard that Washington DC, Virginia and Arlington still have many tech internships and
job offers.

I have a friend in computer engineering (in the work force), says that CS is tough right
now. A little over saturated, can be harder to get a job than other tech fields.
```

**Chunk 3** — Source: `how_is_the_computer_science_at_gwu_incoming` (chunk 0)
```
GWU has a cybersecurity program and scholarship that you might be interested in.

Hello, I was wondering where I could get more information on that as I'm currently
enrolled in '28 CS and would be interested in the cyber security program as I have two
certificates (Sec+ & Net+).

IF you take CS at GWU, try to avoid Professor Aviv if you can.
```

**Chunk 4** — Source: `how_to_get_the_dorm_you_want_as_a_first_year` (chunk 0)
```
You don't get to choose. You rank the dorms in order from most to least preferred and
CLRE will place you from there.

It's completely random. I have no clue if the rankings mean anything, because everyone
puts the Foggy Bottom ones first.
```

**Chunk 5** — Source: `social_scene_in_gw` (chunk 0)
```
Greek life only makes up a small portion of campus social life so I wouldn't worry about
that. If you're looking for a school with big game days and massive tailgates/pregames,
GW isn't for you. If you're down with house-parties, student org events, and partying
across the city (imo GW's #1 social advantage), then GW's great.
```

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2

**Production tradeoff reflection:**
I chose all-MiniLM-L6-v2 because it offers a strong balance of performance and efficiency for English-language text retrieval, and its local deployment eliminates API costs and latency. In a production environment without cost constraints, I would consider using a larger, more powerful model like OpenAI's text-embedding-3-large or Cohere's multilingual-embed-v3-large. These models offer significantly higher accuracy and better handling of complex, domain-specific language, which would be crucial for a system that needs to provide precise answers to nuanced student questions. Additionally, larger models typically have longer context windows, allowing them to process more information at once and potentially improve the quality of retrieved results. The trade-off would be increased latency and cost, but for a production system where accuracy and user experience are paramount, this would likely be a worthwhile investment.

---

## Retrieval Examples

Three test queries were run against the live ChromaDB collection (138 chunks, top-k = 4, cosine distance).

---

### Query 1: "What do students say about the pacing and rigor of early computer science classes at GWU?"

| Rank | Source document | Cosine distance | Chunk preview |
|------|----------------|-----------------|---------------|
| 1 | `computer_science_at_gw` | 0.457 | *"to your question because I'm the new department chair for Computer Science… UMD has a fantastic program… I think equally highly of the GWU program. We have many fewer majors so: (a) our classes are much smaller, and (b) all students are required to do…"* |
| 2 | `how_is_the_computer_science_at_gwu_incoming` | 0.494 | *"GWU has a cybersecurity program and scholarship that you might be interested in… IF you take CS at GWU, try to avoid Professor Aviv if you can."* |
| 3 | `cs_jobs` | 0.516 | *"I have a friend in computer engineering (in the work force), says that CS is tough right now. A little over saturated, can be harder to get a job than other tech fields."* |
| 4 | `computer_science_at_gw` | 0.519 | *"guy I tangentially knew was in the GW Computer Science program and apparently it was actually trash… GWU is trying hard to fight the idea that we're only a political science school."* |

**Why these chunks are relevant:** The query asks specifically about *CS class pacing and rigor*. Chunks 1 and 2 are from the two most directly relevant threads — the department chair's response comparing GWU and UMD class sizes, and the incoming freshman CS advice thread. The embedding model correctly identified both as semantically close to the query because they share vocabulary around "CS program," "GWU," and academic experience. Chunks 3 and 4 are adjacent in semantic space (CS at GWU) but answer a different sub-question (job market, not coursework difficulty), which explains why the bot returned "I don't have enough information" — none of the top-4 chunks contained the specific pacing/rigor commentary the question needed.

---

### Query 2: "Is the freshman housing lottery actually random, or does the placement matrix favor certain preferences?"

| Rank | Source document | Cosine distance | Chunk preview |
|------|----------------|-----------------|---------------|
| 1 | `incoming_student_housing_questions` | 0.486 | *"Madison and Guthridge are the best freshman dorms by far. I went random for roommates and I got lucky… I would say Madison and Potomac."* |
| 2 | `how_to_get_the_dorm_you_want_as_a_first_year` | 0.508 | *"You don't get to choose. You rank the dorms in order from most to least preferred and CLRE will place you from there."* |
| 3 | `gwu_housing` | 0.551 | *"Just so you know, they tell you that your preferences influence your placement, but it's really a lottery. Especially now that Thurston is under renovation and there are fewer options."* |
| 4 | `i_didnt_get_any_of_my_15_housing_choices` | 0.567 | *"Way more admitted students than they anticipated committed to going to GW as freshmen… What are the chances that during the year we can switch into vacant rooms or a different residence hall second semester?"* |

**Why these chunks are relevant:** All four retrieved chunks come from housing-specific threads and contain direct student commentary on the lottery and placement mechanism — exactly what the query asks about. Chunk 2 (dist=0.508) from `how_to_get_the_dorm_you_want_as_a_first_year` directly answers the question: *"You rank the dorms in order from most to least preferred and CLRE will place you from there"* — describing the preference submission process. Chunk 3 from `gwu_housing` directly states *"it's really a lottery"* despite preferences — the core factual claim. The cosine distances (0.49–0.57) show solid but not perfect semantic alignment, reflecting that the query uses the term "placement matrix" (more formal language) while the source documents use colloquial Reddit phrasing like "lottery" and "random." Despite the vocabulary gap, the model still retrieved the right threads.

---

### Query 3: "What are the best strategies for navigating the high-stress course registration process at GWU?"

| Rank | Source document | Cosine distance | Chunk preview |
|------|----------------|-----------------|---------------|
| 1 | `computer_science_at_gw` | 0.498 | *"…but I still have a lot of thinking to do. Did you go to GWU?"* |
| 2 | `social_scene_in_gw` | 0.572 | *"I mean if you are looking for that stuff as part of your college experience GWU isn't for you. If you don't care about that stuff and GWU has a program that you are interested in then GWU could be an option… DC is really a lonely place."* |
| 3 | `registration_tipschances` | 0.592 | *"…all but one of the classes I'm trying to register for. Good luck."* |
| 4 | `computer_science_at_gw` | 0.601 | *"I think equally highly of the GWU program. We have many fewer majors so: (a) our classes are much smaller, and (b) all students are required to do senior design projects with faculty interaction, and (c) it is easier to get involved in faculty research projects."* |

**Note — retrieval failure:** The correct document (`registration_tipschances`) was retrieved at rank 3, but the specific chunk returned was just the tail end of the keyboard-macro comment: *"all but one of the classes I'm trying to register for. Good luck."* — a single sentence with no actionable advice. The strategy-dense chunk (split-screen CRNs, register UW first, use macros) was in a different chunk that ranked outside the top-4. Ranks 1, 2, and 4 are completely off-topic (`computer_science_at_gw`, `social_scene_in_gw`), which left the context window with no usable registration guidance — causing the bot to correctly fall back to "I don't have enough information."

---

## Grounded Generation

**System prompt grounding instruction:**

You are GWU Guide Bot, a helpful assistant for students at George Washington University.

You will be given a set of CONTEXT passages extracted from real Reddit discussions by GWU students.

Rules you must follow — no exceptions:
1. Answer using ONLY information that appears in the CONTEXT passages below.
2. Do NOT use any outside knowledge, even if you are confident it is correct.
3. If the CONTEXT does not contain enough information to answer the question,
   respond with exactly: "I don't have enough information on that topic in my sources."
4. Do NOT invent details, statistics, professor names, building names, or policies
   that are not explicitly stated in the CONTEXT.
5. Keep your answer concise and direct. Quote or closely paraphrase the CONTEXT where possible.
6. Do NOT include a source list — that will be added separately.

**How grounding is enforced:**  
Grounding is enforced at **two independent levels** so neither can be circumvented alone:

1. **System prompt hard constraints** — The 6-rule system prompt explicitly forbids the model from using any knowledge outside the provided CONTEXT block. Rule 3 specifies the *exact* fallback phrase the model must return when context is insufficient, so the app can detect and style it consistently.
2. **Distance threshold filter** — Before the prompt is built, `generator.py` drops any retrieved chunk with `cosine_distance >= 0.6`. This means the LLM never even *sees* loosely related material; the context block only contains chunks that are meaningfully similar to the query. If all chunks are filtered out, the system returns a fallback message without ever calling the LLM.
3. **Programmatic source attribution** — Sources are appended by `_build_source_list()` in Python *after* the LLM responds, and are never generated by the model. This guarantees that source titles and URLs are always accurate, even if the model paraphrases or reorders content.

---

**Example Response 1 — In-scope query with source attribution**

**Query:** "Is the freshman housing lottery actually random, or does placement favor certain preferences?"
**Bot response:**
According to the CONTEXT, "You rank the dorms in order from most to least preferred and CLRE will place you from there." This suggests that placement is not entirely random, but rather takes into account the student's preferences. However, one student also describes the process as "really a lottery", implying that there is an element of chance involved.
**Sources:**  
- Incoming student housing questions  
  https://www.reddit.com/r/gwu/comments/1jvbdjc/incoming_student_housing_questions/  
- how to get the dorm you want as a first year  
  https://www.reddit.com/r/gwu/comments/1pyc0s6/how_to_get_the_dorm_you_want_as_a_first_year/  
- I didn't get any of my 15 housing choices...  
  https://www.reddit.com/r/gwu/comments/8ouwev/i_didnt_get_any_of_my_15_housing_choices/  
- GWU Housing  
  https://www.reddit.com/r/gwu/comments/gwsp0i/gwu_housing/

---

**Example Response 2 — In-scope query with source attribution**

**Query:** "What do students say about the quality and variety of food at GWU dining halls?"
**Bot response:**  
Students express dissatisfaction with the quality and variety of food at GWU dining halls. One student says the food is "shitty" and that it's "not that hard to put out high quality meals, even at scale, GW just doesn't care to do so." Another student mentions that the rice was "CONSISTENTLY awful" last semester, but notes that breakfast at Thurston is good, specifically the omelets. Additionally, a student compares the food to "commercial grade frozen shit", implying that the food is of low quality.
**Sources:**  
- My honest review on GW Dining  
  https://www.reddit.com/r/gwu/comments/1bw4x7a/my_honest_review_on_gw_dining/  
- GWU Housing  
  https://www.reddit.com/r/gwu/comments/gwsp0i/gwu_housing/

---

**Out-of-scope Query — Refusal example**

**Query:** "What is the best way to prepare for a machine learning interview?"
**Bot response:**  
I don't have enough information on that topic in my sources. (Best match had distance 0.720, threshold is 0.6.)

*This query is outside the GWU Freshman Guide domain entirely. The distance threshold filter caught it before the LLM was called — the closest matching chunk scored 0.720, well above the 0.6 cutoff, so no context was passed to the model and the pipeline returned the fallback message directly.*



---

## Query Interface

The system is served as a **Gradio ChatInterface** running locally at `http://127.0.0.1:7860`.

**Input field:**  
A single-turn free-text box labelled *"Ask a question about GWU…"*. The user types any natural-language question about freshman life at George Washington University and submits it by pressing Enter or clicking the Send button. No special syntax or keywords are required.

**Output field:**  
The response area displays two parts rendered as Markdown:
1. **Grounded answer** — a concise prose response written by the LLM using only the retrieved Reddit passages as its context source.
2. **Sources block** — a programmatically appended `**Sources:**` list of deduplicated post titles and their full Reddit URLs, added by `generator.py` after generation so attribution is always accurate regardless of what the model says.

If no retrieved chunk passes the `cosine_distance < 0.6` threshold, the sources block is omitted and the response is a fallback message indicating the query is out of scope.

---

**Sample interaction transcript**

```
User ▶  What do students say about the quality and variety of food at GWU dining halls?

Bot  ▶  Students express dissatisfaction with the quality and variety of food at GWU
        dining halls. One student says the food is "shitty" and that it's "not that hard
        to put out high quality meals, even at scale, GW just doesn't care to do so."
        Another student mentions that the rice was "CONSISTENTLY awful" last semester,
        but notes that breakfast at Thurston is good, specifically the omelets.
        Additionally, a student compares the food to "commercial grade frozen shit",
        implying that the food is of low quality.

        **Sources:**
        - My honest review on GW Dining
          https://www.reddit.com/r/gwu/comments/1bw4x7a/my_honest_review_on_gw_dining/
        - GWU Housing
          https://www.reddit.com/r/gwu/comments/gwsp0i/gwu_housing/
```

---

## Evaluation Report


| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about the pacing and rigor of early computer science classes at GWU? | Students describe early CS classes as challenging; they recommend checking Rate My Professor, note small class sizes as a benefit, and warn about certain professors. | "I don't have enough information on that topic in my sources." — The retrieved chunks were from Computer Science at GW, How is the CS at GWU (Incoming), and Social Scene in GW, but those chunks did not contain specific pacing/rigor commentary; the relevant comments were split across chunk boundaries and fell outside the top-4. | Off-target | Inaccurate |
| 2 | Is the freshman housing lottery actually random, or does the placement matrix favor certain preferences? | The lottery is effectively random — rank Foggy Bottom first, Vern last, but placement is not guaranteed. Room-swapping is a real fallback. | "The freshman housing placement is described as 'really a lottery', implying it is random. However, students are allowed to 'rank the dorms in order from most to least preferred' and CLRE will place them based on that, suggesting preferences are taken into account." Retrieved from 4 relevant housing threads. | Relevant | Accurate |
| 3 | What are the best strategies for navigating the high-stress course registration process at GWU? | Pre-load CRNs, split-screen with the portal, register UW sections first, prepare backup schedules, use keyboard macros. | "I don't have enough information on that topic in my sources." — The Registration tips/chances thread was retrieved but the specific strategy chunks (CRN split-screen, UW-first advice, macros) were not among the top-4; the retrieved chunk was mid-thread context that didn't contain actionable advice. | Partially relevant | Inaccurate |
| 4 | What are the realistic pros and cons of living on the Mount Vernon campus versus Foggy Bottom? | Vern: quiet, camaraderie, chance at single room, but isolated and VEX-dependent. Foggy Bottom: central, walkable, social, but cramped dorms. | "I don't have enough information on that topic in my sources." — Retrieved chunks were from Campus Safety, GWU Housing, Social Scene, and Commuting by Metro — none of which directly compared Vern vs Foggy Bottom pros/cons in the top-4 results. The relevant housing thread content was not ranked high enough. | Off-target | Inaccurate |
| 5 | What do students say about the quality and variety of food at GWU dining halls? | "Decent at best, borderline dangerous at worst" — mushy chicken, stale bread, forced ~$3,000 meal plans. Highlights: Thurston omelettes, Halal Shack. | "Students express dissatisfaction with food quality. One student says it's 'not that hard to put out high quality meals, GW just doesn't care.' Another notes rice was 'CONSISTENTLY awful' but breakfast at Thurston is good, especially the omelets. A student compares the food to 'commercial grade frozen shit'." Retrieved from My Honest Review on GW Dining. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**  
*"What are the best strategies for navigating the high-stress course registration process at GWU?"*

**What the system returned:**  
`"I don't have enough information on that topic in my sources."`  
Sources cited included *Registration tips/chances?* (the correct thread), *Computer Science at GW*, and *Social Scene in GW*.

**Root cause (tied to a specific pipeline stage):**  
This is a **two-stage failure** in the retrieval pipeline:

1. **Chunking stage — strategy content split across boundaries.** The actionable advice in the `registration_tipschances` document (split-screening CRNs, UW-first registration, keyboard macros) is densely packed into the middle of the thread. With a 500-character chunk size, the most strategy-rich passage — *"pull up all the CRNs for the classes you want in the notes on your computer and split screen it with the registration screen... if you have your heart set on a specific class, enter that CRN first"* — was chunked together with surrounding conversational filler ("That's what I want lol. Is it not popular?"). This diluted the semantic signal of that chunk. A strategy-dense passage became a mixed chunk whose embedding drifted toward general course-choice discussion rather than registration tactics.

2. **Retrieval stage — semantic mismatch at top-k cutoff.** The query *"best strategies for navigating high-stress course registration"* matched the `registration_tipschances` document, but the specific chunk retrieved from it was a later mid-thread exchange about Math & Politics difficulty — not the strategy content. The strategy chunk ranked 5th or lower, just beyond the `N_RESULTS=4` hard cutoff. Because the top-4 slots were partially occupied by off-topic documents (`Computer Science at GW`, `Social Scene in GW`), the grounding instruction correctly refused to answer — there genuinely was no strategy content in the retrieved context window.

**What you would change to fix it:**  
Two targeted changes would fix this:  
- **Increase top-k from 4 to 6–8** so that the strategy-dense chunk has a chance to enter the context window even when higher-scoring but off-topic chunks are present.  
- **Apply paragraph-level chunking** instead of fixed-character splitting for this corpus. Since Reddit advice threads naturally group into self-contained paragraphs (one commenter = one idea), splitting strictly at `\n\n` boundaries would keep the full split-screening tip in a single chunk rather than merging it with adjacent small-talk replies. This would preserve the semantic density of the actionable advice and raise its retrieval score for strategy queries.


---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**  
The Chunking Strategy section of `planning.md` gave Claude a precise target to implement against: 500-character chunks, 100-character overlap, and the explicit goal of not splitting key proper nouns (residence hall names, course codes) across boundaries. This meant when Claude generated the initial `chunk_document()` function, it already included the paragraph-snap logic to break at the nearest double-newline rather than mid-sentence — a design decision that came directly from reading the overlap rationale in the spec. Without that written reasoning, Claude would have produced a plain fixed-stride split with no boundary awareness.

**One way your implementation diverged from the spec, and why:**  
The original spec treated the `[POST BODY]` and community comments as a single undifferentiated block of text to be chunked together. During testing it became clear that the original Reddit question (the post body) was appearing in retrieved chunks as if it were an answer — polluting results with the question text itself. The implementation was updated to extract `post_body` as a separate metadata field stored in ChromaDB and excluded from chunk text entirely, so that only community replies (the actual answers) are embedded. This separation was not planned in `planning.md` because the issue only became visible after running real retrieval queries and inspecting the raw chunk output.

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

- *What I gave the AI:* I asked claude to scrape all the provided urls and extract the content of each Reddit page and store them as raw files and asked it to clean up any extra junk .
- *What it produced:* It gave me code to extract the content and store them as raw files and also clean up the junk. When I ran the code it produced clean files, but the post body was same in all the files and also it is not using beautifulsoup and instead using regex for scrapping which is not efficient.
- *What I changed or overrode:* I then changed the code to reflect the post body correctly and in addtion to using regex I used beautifulsoup for scrapping and clean up.

**Instance 2**

- *What I gave the AI:* I gave Claude the Chunking Strategy section from `planning.md` (500-char chunks, 100-char overlap, paragraph-boundary snapping) and the raw structure of the cleaned `.txt` files — including the `[POST TITLE]`, `[POST BODY]`, and comment layout — and asked it to implement `load_documents()` and `chunk_document()` in `ingest.py`.
- *What it produced:* Claude implemented both functions correctly for the chunking logic, but it treated the entire file as one flat block of text: the `[POST BODY]` label was simply stripped and the post body content was left in the `text` field alongside the comments, meaning the original question was being chunked and embedded as if it were an answer.
- *What I changed or overrode:* I directed Claude to refactor `load_documents()` to use a three-state parser that separates the post body from the comment replies. The post body was moved to a dedicated `post_body` metadata field (propagated through `chunk_document()` into every chunk dict and stored in ChromaDB), while the `text` field passed to the chunker was restricted to comments only. I also changed `chunk_document()` from a two-argument function `(text, doc_name)` to a single-argument function that accepts the full doc dict, so all metadata flows through automatically without manual enrichment at the call site.
