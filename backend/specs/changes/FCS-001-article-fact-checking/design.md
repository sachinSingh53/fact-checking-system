# Design

## Flow

```text
Submit article → save job → extract claims → validate and save claims
             → verify claims fairly across jobs (3 Gemini slots per claim)
             → apply voting and calibrated confidence policy
             → synthesize and validate report → save report → completed
```

The API acknowledges submission quickly with a job ID. A Temporal workflow owns stage transitions and retries; PostgreSQL is the durable system of record. Gemini calls run in activities, not in deterministic workflow code. The workflow can resume after a worker restart by reading persisted stage records.

## Data and states

- **Article job:** id, idempotency key, input digest and text, status, timestamps, failure summary, model/prompt/policy versions.
- **Claim:** stable ID, article ID, order, atomic text, source span or quoted location, extraction version, status.
- **Vote slot:** article/claim ID, slot 1–3, status, final vote/reason, attempts, model and prompt metadata, usage, latency, sanitized raw output or error reference. Every retry belongs to the same slot.
- **Assessment:** claim ID, final verdict, confidence, short justification, policy version, reason for `unverifiable` when applicable.
- **Report:** article ID, version, validated content, disclosure, generation metadata, saved timestamp.

Normal states are `accepted → extracting → claims_saved → verifying → synthesizing → completed`. When extraction finds zero claims, the workflow skips `verifying` and continues from `claims_saved → synthesizing → completed`. Terminal non-success states are `out_of_scope` for more than 30 extracted claims, `extraction_failed` for invalid extraction, `verification_incomplete` when the workflow cannot produce a complete set of claim assessments, and `report_failed`. Per-claim failed calls can still yield a complete claim assessment of `unverifiable`, so isolated failures need not turn the whole article into `verification_incomplete`. State changes and persisted data must commit atomically where they belong to the same stage.

## Extraction boundary

Use a strict structured schema for claims and source locations. Reject malformed output; retry only according to the bounded retry policy. The validator accepts an empty claims list; for populated lists it checks nonempty claim text, unique IDs/order, and plausible spans. Save a valid extracted set, then mark the job `out_of_scope` without verification only when its count exceeds 30. It must not ask another model to silently rewrite an invalid extraction, drop excess claims, or add claims to reach a minimum. The user-supplied extraction prompt will be attached by immutable version when available.

## Voting and confidence

Each verification slot is a separate Gemini request against the same normalized claim and relevant article context. Pin the chosen Gemini model/version and generation settings for an article run. Separate calls can still be correlated because they share a provider and training data; 2-of-3 agreement is a decision rule, not three independent sources.

The finalizer waits for all three slots to complete or exhaust bounded retries. Two or three matching `supported` votes can yield `supported`; two or three matching `refuted` votes can yield `refuted`. Before assigning either, it checks vote validity, the claim's date/place scope, and a calibrated confidence threshold. Any failed slot, unresolved scope, lack of a two-vote directional majority, or subthreshold score yields `unverifiable`. An `unverifiable` vote may coexist with a 2-of-3 directional majority, but the confidence gate still applies. A dissenting directional vote lowers confidence according to the calibrated policy; its reason remains visible.

Confidence calibration is a versioned policy trained and evaluated on labeled claims. Candidate inputs may include vote pattern, model response quality, claim type, time sensitivity, and disagreement; the exact formula and threshold are chosen from evaluation results, then frozen for a release. No value is presented as an empirically calibrated confidence until that evidence exists. If the policy is unavailable, produce `unverifiable` with a low score and an explicit calibration-unavailable reason. Build the short justification from the recorded vote reasons and any failure or uncertainty reason; do not make another hidden model call.

## Report safety

Synthesis receives only the persisted assessments and vote summaries. The service constructs the report's claim rows from saved assessments; Gemini may provide the readable overview. A deterministic validator compares any structured claim references, verdicts, and scores in the synthesis output to the database; unrecognized or altered claims make the synthesis invalid. Report fidelity is also measured in evaluation because free-text overviews cannot be fully validated by a schema. Bounded retries may repair a malformed synthesis using the user-supplied prompt version, but no prompt text is created by this specification. Save an immutable report version before publishing `completed`. Failure leaves assessments queryable with `report_failed`.

## Fair scheduling and call control

Limit both global Gemini calls and calls per article. Dispatch ready verification work in rotating article order so a 30-claim article cannot occupy every slot while other articles wait. Admission control caps active articles at 10; accepted queued jobs retain their enqueue time and are promoted fairly. Retries return to the fair queue with backoff instead of monopolizing workers. Apply a shared rate limiter using actual Gemini quotas, and propagate provider overload into bounded backoff and visible job status.

Provisioning must be measured: 1 article/minute at 20 claims means 62 normal calls/minute on average; a 10-article burst means 620 calls before retries. The required concurrency depends on observed Gemini latency and quota. The implementation must measure this rather than assume the provider can serve it. At 30 claims, the normal path is 92 calls per article.

## Reliability and privacy

Use idempotent activity keys based on job, stage, claim, vote slot, and attempt. Save each provider attempt and its outcome before retry decisions. Give each stage a deadline and a finite retry budget. On a provider outage, record a terminal failure or `unverifiable` assessment as appropriate; never wait forever. Use structured logs with job/claim IDs, omit article text and secrets from logs, and restrict access to stored text and raw responses. Retention and deletion periods are launch decisions.

## Prompt boundary

Three user-supplied, versioned prompt assets are required: extraction, verification, and report synthesis. Until they are supplied, the domain workflow cannot be enabled. The service validates prompt presence and records prompt versions for each run. This spec defines input/output contracts and validation around those prompts, not their wording.
