# Delivery tasks

Each task should end with a reviewable slice and evidence linked to [verification.md](verification.md). Begin domain implementation after this draft is reviewed and the relevant decisions are made.

1. **Contracts and persistence:** finalize request limits and API schemas; add article, claim, vote attempt/slot, assessment, and report tables with migrations and idempotent transitions. Covers FCS-REQ-01, 04, 06, 11–14.
2. **Gemini integration and prompt assets:** implement a structured Gemini adapter with quota control, metrics, and versioned user-supplied prompts. Keep the workflow disabled until the prompts exist. Covers FCS-REQ-02, 05, 06, 10, 18.
3. **Extraction workflow:** implement article submission, claim extraction, strict validation, and claim persistence. Cover atomicity and out-of-contract behavior. Covers FCS-REQ-01–04, 13–14.
4. **Verification workflow:** implement three vote slots, retry records, fair scheduling, conservative vote finalization, and explicit failure handling. Covers FCS-REQ-05–09, 14–15.
5. **Confidence and evaluation:** assemble a labeled evaluation set, freeze a calibrated score policy and directional threshold, and test temporal/ambiguous/unknown cases. Covers FCS-REQ-07–09.
6. **Report and retrieval:** implement constrained synthesis, deterministic validation, durable report save, status/result reads, and method disclosure. Covers FCS-REQ-10–14.
7. **Capacity and release evidence:** run the defined load tests with real Gemini quota, tune fair scheduling and concurrency, document latency and quality metrics, and resolve the launch decisions in README. Covers FCS-REQ-15–18.

No task is authorized to invent prompt text. If user-supplied prompts are absent, build and test schemas and workflow boundaries with explicitly labeled test fixtures only.
