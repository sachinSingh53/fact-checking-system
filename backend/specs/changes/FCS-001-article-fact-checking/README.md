# FCS-001: Article fact checking

**Status:** Draft for review  
**Owner:** Product and engineering  
**Scope:** First article-to-report workflow using Google Gemini's internal knowledge

Read [proposal.md](proposal.md) for the goal, [requirements.md](requirements.md) for behavior, [design.md](design.md) for the implementation shape, [tasks.md](tasks.md) for delivery order, and [verification.md](verification.md) for acceptance evidence.

This specification contains no claim extraction, verification, or report synthesis prompt text. The user will provide all three prompts later. Prompt versions, a labeled evaluation set, and provider capacity must be available before a production launch.

## Decisions still to make

1. Set an article text size limit. More than 30 extracted claims produces `out_of_scope` and never silently drops claims. Articles with 0–30 claims continue normally.
2. Choose the Gemini model ID and version for each stage, along with approved per-project rate and concurrency limits.
3. Set and validate the confidence calibration and decision threshold using a labeled evaluation set. Until then, no production verdict may be called `supported` or `refuted`.
4. Decide retention periods and access policy for submitted text, raw model responses, and reports before handling real articles.

These are explicit launch decisions, not permission to invent prompt content or a confidence formula during implementation.
