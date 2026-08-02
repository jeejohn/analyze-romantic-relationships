# Twelve-week maintenance plan

This plan creates genuine maintenance evidence. Do not backfill, fabricate, or purchase activity.

## Weeks 1–2: publish and recruit testers

- Publish version `0.1.0` with all CI checks passing.
- Ask 5–10 people who understand the privacy rules to test only synthetic or self-authored anonymized examples.
- Open one issue per distinct failure; do not create fake user accounts or fake conversations.
- Record baseline metrics in `metrics/snapshot.json` after publication.
- Target: at least three independent test sessions and two actionable findings.

## Weeks 3–4: fix reproducible failures

- Prioritize incorrect evidence boundaries, safety routing, privacy leaks, and activation problems.
- Require a regression case and counterexample for every rule change.
- Publish `0.1.1` only for verified fixes.
- Target: close at least 80% of reproducible high-priority findings with tests.

## Weeks 5–6: improve onboarding

- Watch where new testers fail to install, invoke, or structure a case.
- Shorten instructions that create repeated confusion.
- Add one installation check covering a clean environment.
- Invite a contributor to improve documentation or a synthetic case.

## Weeks 7–8: broaden case diversity

- Add synthetic cases covering role swaps, same-sex couples, long-distance relationships, non-marital goals, disability or care constraints, and income/companionship conflicts.
- Do not add cases merely to increase count; each must cover a distinct failure mode.
- Run the symmetry and false-equivalence review on all new rules.

## Weeks 9–10: prove maintainer workflow

- Demonstrate issue triage, PR review, release notes, and response times.
- Enable optional Codex review for trusted maintainers after the API secret is configured.
- Publish a metrics snapshot with links to verifiable public activity.

## Weeks 11–12: release and OSS application review

- Publish a stable pre-1.0 release with a clear changelog.
- Summarize users, downloads, Stars, Forks, contributors, releases, closed issues, median first response time, and three verified use cases.
- Explain ecosystem importance without inflating numbers.
- Apply to Codex for Open Source only if the repository shows active maintenance and a defensible use case; otherwise continue building evidence.

## Weekly operating rhythm

- Monday: triage new issues and check privacy risks.
- Wednesday: reproduce accepted problems and prepare tests.
- Friday: merge reviewed fixes, update changelog, and record metrics.
- Monthly: audit rules for bias, contradictions, and stale guidance.
