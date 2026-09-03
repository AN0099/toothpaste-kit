# Before and After Examples

Paired transformations, one per pattern category in `structural-patterns.md` and `banned-words.md`. Used as calibration reference, not a template to copy phrasing from.

## Binary Contrast

**Before:** "The problem isn't the tooling. It's the process."
**After:** "The process is the problem; the tooling was never the bottleneck."

## Negative Listing

**Before:** "This isn't a workaround. It isn't a patch. It's a redesign."
**After:** "This is a redesign, not a patch applied on top of the existing architecture."

## Dramatic Fragmentation

**Before:** "Speed. Reliability. Cost. Pick two. That's it. That's the tradeoff."
**After:** "Speed, reliability, and cost trade off against each other; most teams can only optimize for two at once."

## Rhetorical Setup

**Before:** "What if the outage wasn't caused by the deploy at all? Here's what I mean: the timing was coincidental."
**After:** "The outage timing coincided with the deploy but wasn't caused by it, the root cause was an unrelated DNS TTL expiry."

## Triplets Used as Default Shape

**Before:** "The fix improves reliability, performance, and maintainability."
**After:** "The fix improves reliability. It also happens to simplify the on-call rotation, since fewer alerts fire."

## Tortured Metaphor

**Before:** "The seeds of the outage bloomed into a thunderstorm of alerts."
**After:** "A single misconfigured health check triggered a cascade of alerts across four downstream services."

## Inhuman Emotion

**Before:** "It's an exciting shade of grey in the logging output."
**After:** "The logging output uses a mid-grey that's easy to distinguish from warning-level red."

## False Agency

**Before:** "The bug becomes a fix once the patch lands."
**After:** "The on-call engineer fixes the bug once the patch lands."

## Narrator-from-a-Distance

**Before:** "Nobody designed this alert to fire at 3am. It just happens."
**After:** "The team never tuned this alert's threshold, so it fires whenever nightly batch jobs spike CPU, including at 3am."

## Parataxis

**Before:** "The deploy failed. The rollback triggered. The pager fired."
**After:** "The deploy failed, which triggered an automatic rollback and paged the on-call engineer within ninety seconds."

## Passive Voice

**Before:** "The config was updated and the service was restarted."
**After:** "The on-call engineer updated the config and restarted the service."

## Meta-Commentary Opener

**Before:** "In this runbook, we will walk through how to restart the ingestion pipeline."
**After:** "Restart the ingestion pipeline with the following steps."

## Buzzword Cleanup

**Before:** "This change leverages a holistic approach to optimize outcomes across the platform."
**After:** "This change touches shared config, so it affects every service on the platform, not just the one being deployed."
