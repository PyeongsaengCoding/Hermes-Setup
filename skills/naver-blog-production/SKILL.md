---
name: naver-blog-production
description: Produce and schedule Naver blog posts with verification.
version: 1.0.0
license: MIT
platforms: [macos]
---

# Naver blog production

Use for an authorized Naver blog production or scheduling request. Account-specific details belong in the user's project, not this skill.

1. Read the target project's `AGENTS.md` and its production, approval and evidence rules. Ask for a target blog and requested work if missing.
2. Identify the existing authenticated browser profile. Confirm the actual logged-in account and target blog before writing; a fresh isolated browser does not prove the user's account is logged out.
3. Read the actual scheduled-post list for the requested date. Preserve existing reservations and avoid duplicate topics, questions, products and publication dates according to the project rules.
4. Preserve open drafts and unrelated tabs. Use only supported background actions when the user requires uninterrupted work; do not activate a browser after a background input refusal.
5. Use real images, source evidence and affiliate links. Do not fabricate content-source or scheduling receipts.
6. Verify the saved draft or reservation on the actual site, including its target and time zone. Report pre-existing and newly created reservations separately.
7. Close only task-created tabs after verifying saved work.

Project instructions are not skills. Login credentials, blog IDs and profile names stay in the user's local project configuration.
