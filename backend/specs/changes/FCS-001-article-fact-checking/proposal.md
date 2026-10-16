# Proposal

## Goal

Given an English article or passage containing up to 30 verifiable factual claims, produce a saved report with one assessment per atomic claim. Every assessment contains `supported`, `refuted`, or `unverifiable`, a confidence score from 0 to 1, a short justification, and the three Gemini sample votes or their recorded failure states. If the article contains no checkable factual claims, complete it with an empty assessment list and a clear explanation.

The system uses Gemini's internal knowledge only. A vote is one model response, not an independent documentary source. The report must say this plainly; it must not imply that a web page, paper, or primary source was consulted. Agreement among model samples is useful but cannot by itself establish truth.

## Priorities

1. Do not overstate factual certainty. Incomplete evidence, failed calls, disagreement, outdated knowledge, or low confidence should lead to `unverifiable` when a reliable directional verdict cannot be made.
2. Complete work despite isolated claim failures while exposing those failures in the report.
3. Give all accepted articles fair progress under load and bound retries.
4. Meet the latency targets under the stated workload, subject to measured Gemini capacity.

## In scope

- Submit an English article, obtain a job ID, inspect progress, and retrieve a saved report.
- Extract atomic, checkable factual claims; preserve their location in the source text.
- Persist claims before verification starts.
- Run three independent Gemini verification calls per claim, vote, and assign a calibrated confidence score.
- Synthesize a readable report without changing the recorded claim verdicts.
- Persist the final report and all vote and failure details.
- Make retries safe and visible, with fair scheduling across articles.

## Out of scope for this change

- Web search, retrieval, external citations, or validation of model-named sources.
- Non-English articles, opinion scoring, image/audio/video fact checking, and automatic correction of an article.
- Human review UI, publishing, and integrations with external content systems.
- Any prompt wording. The user supplies the three prompt bodies later.

## Success

An eligible article reaches a durable terminal result, including an honest `unverifiable` result for claims that cannot be assessed reliably. A report never invents missing votes, hides a failure, or turns a weak assessment into a confident verdict. Capacity and latency acceptance use the workload in [verification.md](verification.md).
