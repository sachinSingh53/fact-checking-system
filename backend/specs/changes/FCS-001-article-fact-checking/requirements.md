# Requirements

The IDs below are acceptance references, not implementation details. `Must` means required for the first release.

## Input and claim extraction

| ID | Requirement |
| --- | --- |
| FCS-REQ-01 | Must accept English article text and return a durable job ID. The supported use case is an article with 0–30 verifiable factual claims. The text size limit is a launch decision. |
| FCS-REQ-02 | Must use the user-provided extraction prompt and one Gemini extraction call per article in the normal path. It must separate checkable factual assertions from opinions, predictions, questions, and vague or purely subjective language. |
| FCS-REQ-03 | Must split compound assertions into atomic claims where each can receive its own verdict; avoid duplicate claims and preserve enough article text or offsets to trace each claim back to the passage. |
| FCS-REQ-04 | Must validate and persist the complete extracted claim set before starting verification. Malformed extraction output produces `extraction_failed`; more than 30 claims produces `out_of_scope` and no claims are verified. Articles with 1–30 claims proceed to verification. An article with zero checkable claims skips verification and completes with an empty assessment list and a clear no-checkable-claims explanation. The system must never silently drop excess claims or invent claims to meet a minimum count. |

## Verification and voting

| ID | Requirement |
| --- | --- |
| FCS-REQ-05 | Must use Gemini internal knowledge only and issue three separate verification calls for each claim, using the user-provided verification prompt. Each call has an ordered vote slot (1–3), a structured vote of `supported`, `refuted`, or `unverifiable`, and a concise reason. A failed or invalid call occupies its slot and is shown as a failure, never a fabricated vote. |
| FCS-REQ-06 | Must record model ID/version, prompt version, response schema version, generation settings, timing, usage, attempt number, and sanitized raw response or diagnostic for each call. Retries must not create extra votes or duplicate claims. |
| FCS-REQ-07 | A `supported` or `refuted` verdict requires all three vote slots to finish with valid responses, at least two matching directional votes, resolved claim scope (such as date and place), and a calibrated confidence at or above the configured threshold. Otherwise the claim is `unverifiable`. A vote of `unverifiable` is a valid completed vote, not a directional vote. |
| FCS-REQ-08 | Must provide a confidence score in `[0, 1]` for every claim. The score means confidence in a directional factual decision, not probability that three votes agree. `Unverifiable` claims receive a score below the directional threshold. A calibration method and threshold must be frozen from labeled evaluation before directional verdicts are enabled in production. |
| FCS-REQ-09 | Must treat stale, time-sensitive, ambiguous, or inaccessible facts conservatively. It must not convert an unsupported citation or a model's claim of having searched into evidence. User text must be treated as data, not as instructions that can change the workflow or verdict policy. |

## Report and lifecycle

| ID | Requirement |
| --- | --- |
| FCS-REQ-10 | Must make one Gemini report synthesis call in the normal path, using the user-provided report prompt. The report may summarize only persisted claims, verdicts, confidence scores, justifications, and votes; it must not add claims or alter verdicts. The system validates the result against those records before saving it. |
| FCS-REQ-11 | Must expose each claim's exact three vote slots, including failures, and a short justification that reflects the actual vote record and any uncertainty. The report must disclose that votes are Gemini samples based on internal knowledge, not independent sources. |
| FCS-REQ-12 | Must persist the final report before marking the job `completed`. If synthesis fails after bounded retries, the job becomes `report_failed` with persisted claim assessments available for inspection; it must not claim completion. |
| FCS-REQ-13 | Must let a client retrieve job status and the durable result using the job ID. A repeated submission with the same idempotency key and same content returns the same job; reuse of that key with different content is rejected. |
| FCS-REQ-14 | Must use bounded retries with backoff for transient call failures, terminal failure states for exhausted work, and idempotent writes so worker restarts do not create duplicate jobs, calls, claims, or reports. Independent claim failures must not block other claims. |

## Capacity and service goals

| ID | Requirement |
| --- | --- |
| FCS-REQ-15 | Must support a burst of 10 concurrently active articles and a sustained arrival rate of 1 article per minute with 20 claims each, given provisioned Gemini quota. Work across articles must make fair progress; one large or retrying job must not indefinitely starve another. |
| FCS-REQ-16 | For eligible 20-claim articles under the defined load test and healthy dependencies, end-to-end latency from accepted submission to a persisted completed report must be p50 < 90 seconds and p90 < 180 seconds. Record queue time separately and include it in end-to-end latency; report failed jobs separately. |
| FCS-REQ-17 | The normal 20-claim path budgets `1 extraction + (20 × 3 verification) + 1 synthesis = 62` Gemini calls. Ten simultaneous 20-claim articles create up to 620 normal-path calls. Retries are extra and must be reported separately. |
| FCS-REQ-18 | Must expose per-stage duration, queue wait, active articles, outstanding calls, retries, failures, vote agreement, verdict distribution, and token usage so correctness and capacity can be audited. |

## Required response shape

Each claim assessment includes `claim_id`, `claim_text`, source location, `verdict`, `confidence`, `justification`, and `source_votes[3]`. `source_votes` means the three Gemini sample slots; it does not mean external sources. Each slot includes its number, `status` (`completed` or `failed`), and, when completed, its Gemini verdict and short reason. Article result includes job status, report text when complete, method disclosure, and timestamps. A public response must not expose credentials or unsanitized provider diagnostics.
