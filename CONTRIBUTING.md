# Contributing

Thank you for helping improve evidence-based relationship analysis.

## Before opening an issue

1. Remove all names, accounts, contact details, locations, institutions, and unique identifying details.
2. Prefer a synthetic minimal example that reproduces one problem.
3. State the exact claim the Skill mishandled and the safer expected boundary.
4. Do not ask maintainers to determine whether a real person is abusive, unfaithful, mentally ill, or secretly motivated by money.

## Contribution types

- **Bug:** a reproducible activation, reasoning-boundary, validation, or documentation problem.
- **Rule proposal:** a durable rule change supported by at least one test case and a counterexample.
- **Synthetic case:** invented material designed to test one distinct failure mode.
- **Documentation:** clearer installation, privacy, or maintenance instructions.

## Rule-change standard

A proposed rule should include:

1. the failure it prevents;
2. the narrowest wording that fixes it;
3. one positive test case;
4. one counterexample showing when the rule must not apply;
5. a gender/role swap check;
6. any new safety or privacy consequence.

Do not add a universal rule from one anecdote. Cases are tests of rules, not votes that automatically rewrite them.

## Local checks

```bash
python -m unittest discover -s tests -v
python scripts/check_skill_consistency.py
```

All checks must pass before opening a pull request. Complete the pull request template and disclose any AI-assisted contribution.

## Real case submissions

Raw private chats and screenshots are not accepted. A real case may be considered only after de-identification, explicit analysis permission, explicit publication permission, automated scanning, and human review. Maintainers may still reject it when re-identification or retaliation risk remains.
