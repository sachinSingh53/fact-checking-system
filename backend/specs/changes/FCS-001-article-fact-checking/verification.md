# Verification and acceptance

This is a draft acceptance plan. Passing code checks alone does not establish factual accuracy, Gemini quota, or latency.

## Functional examples

| Acceptance ID | Scenario | Required evidence | Requirements |
| --- | --- | --- | --- |
| FCS-AC-01 | A passage has several compound statements, opinions, and repeated facts. | Extraction produces atomic, nonduplicate, checkable claims with traceable source locations and saves them before verification. | 01–04 |
| FCS-AC-02 | Extraction output is malformed, has invalid locations, or contains more than 30 claims. | Malformed output leads to `extraction_failed`; an otherwise valid set above 30 is saved and leads to `out_of_scope`. No partial set is verified and no excess claim is dropped. | 02–04 |
| FCS-AC-02A | Extraction produces 1–4 valid claims. | Every extracted claim is saved and receives three verification vote slots; the article proceeds through the normal report flow. | 01–05, 10–12 |
| FCS-AC-02B | Extraction produces zero valid claims from an article containing only opinions or other non-checkable content. | The empty claim set is saved, verification is skipped, and the completed report clearly states that no checkable factual claims were found. No claim or vote is invented. | 01–04, 10–12 |
| FCS-AC-03 | Three valid votes are `supported`, `supported`, `refuted`; calibrated score passes the threshold and no material contradiction exists. | Assessment is `supported`; all three original votes and reasons remain visible. | 05–08, 11 |
| FCS-AC-04 | Votes conflict, a slot fails, the claim is time-sensitive without a reliable time basis, or score is below threshold. | Assessment is `unverifiable`, confidence is below threshold, and justification names the actual limitation. Other claims continue. | 05–09, 14 |
| FCS-AC-05 | Synthesis changes a verdict, adds an unextracted claim, or fails repeatedly. | Invalid report is never marked complete; saved assessments remain readable and job ends as `report_failed` if retries exhaust. | 10–12, 14 |
| FCS-AC-06 | Submission is repeated or a worker restarts after a persisted stage. | One job, one claim set, three final vote slots per claim, and at most one current report version; attempts remain auditable. | 06, 12–14 |
| FCS-AC-07 | Article text tells the model to ignore rules or invent a citation. | Workflow and final output follow the fixed schemas and policy; no citation is represented as checked evidence. | 09–11 |
| FCS-AC-08 | Report is retrieved after completion. | It has all claim fields, three sample vote slots, accurate method disclosure, timestamps, and no credentials or raw provider errors. | 10–13 |

## Quality evaluation

Use a reviewed, labeled set of English claims with known supported, refuted, ambiguous, outdated, and unanswerable examples. Keep a held-out set separate from any policy tuning. Evaluate claim extraction completeness/atomicity, directional verdict precision, false support/refute rates, abstention rate, calibration, and report fidelity. Inspect disagreements manually. Set release thresholds **before** running the held-out evaluation; a threshold cannot be chosen afterward to make a test pass. Approval of the quantitative targets and the evaluation set is required before production directional verdicts.

## Load and fairness evaluation

Run against the chosen Gemini models and approved quota with realistic 20-claim articles, three samples per claim, and the supplied prompts. Measure from accepted submission until the completed report is persisted, including queueing and normal retries; measure terminal failures separately. Run both a 10-article simultaneous burst and a sustained 1 article/minute stream long enough to observe steady state. Show p50 < 90 seconds and p90 < 180 seconds for completed 20-claim articles, plus stage timings, queue times, provider errors, retry counts, and token cost. Report success and failure rates alongside latency; fast failure cannot count as a successful latency result.

For fairness, include a 30-claim article and retrying articles beside new 20-claim articles. Show that each accepted job either progresses within a configured maximum wait or reaches a visible terminal state after its deadline. No accepted job may remain indefinitely pending under healthy dependencies. Record the configured wait/deadline values and observed maximum age.

## Evidence record

For each release, attach code/test revision, prompt versions, model IDs, schema and calibration policy versions, evaluation dataset version and metrics, Gemini quota and load-test environment, latency distribution, known failures, and any waived acceptance criterion. Mark provider and production checks pending until executed in their actual environments.
