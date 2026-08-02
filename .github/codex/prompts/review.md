# Pull request review task

Review the current pull request as a read-only maintainer. Follow `AGENTS.md` and inspect the diff, affected tests, and nearby rules.

Prioritize only consequential findings:

1. A report, expression, inference, correlation, or single event is upgraded into an established event, hidden motive, diagnosis, stable pattern, or certain prediction.
2. Duplicate screenshots or same-event retellings are counted as independent evidence.
3. A rule changes when gender, income, narrator, or provider/recipient roles are swapped without a relevant evidence difference.
4. Symmetry is used to create false equivalence in power, fear, harm, or responsibility.
5. Real or potentially identifiable relationship material can enter a public issue, test, log, artifact, or release without separate analysis and publication authorization.
6. Ordinary communication advice is applied to reported violence, stalking, sexual coercion, coercive control, threats, or credible retaliation.
7. A rule change lacks a synthetic regression test, counterexample, or clear statement of what must remain uncertain.
8. The Skill, validator, examples, policies, and version metadata drift apart.

Do not reformat files or comment on style already enforced by deterministic checks. Do not infer facts about real people. Return a concise list of findings with file paths, impact, and the safest correction. If there are no consequential findings, say so plainly.
