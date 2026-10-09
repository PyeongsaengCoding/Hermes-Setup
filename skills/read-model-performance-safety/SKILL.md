---
name: read-model-performance-safety
description: Review slow read models without weakening access checks.
version: 1.0.0
license: MIT
---

# Read-model performance and safety

Use for slow projections, snapshots or graph read paths. Inspect the actual reader, writers and authorization contract before changing them.

1. Separate data availability, live access validation, storage I/O, computation and delivery. Measure real operations and latency before choosing a fix.
2. Distinguish the diagnostic identity, serving identity and end-user authority. A tool connection or one successful metadata read does not prove access to the target data. Do not bypass application authorization to diagnose a denial.
3. Keep immutable content integrity separate from fresh disclosure checks. Reproduce revocation, deletion and cancellation during a read; stable-data tests do not prove safe memoization.
4. Bound service-wide concurrency, retained results, admission and memory. Test fairness, input-order failure selection, cancellation and capacity losers.
5. Process projection changes idempotently. Preserve restrictive visibility fences before asynchronous updates; do not serve partially assembled snapshots.
6. Test the exact candidate and serving revision. Do not log credentials or private source contents. Distinguish synthetic benchmarks, real-storage checks and authenticated user flows.
7. Verify real open, refresh and reentry before reporting recovery. Record remaining latency or permission gaps rather than calling tests a fix.

Use the target project's tools and fixtures.
