# Repository guidance

## Commands

- Run tests: `python -m unittest discover -s tests -v`
- Check Skill consistency: `python scripts/check_skill_consistency.py`
- Validate a public case: `python relationship_case_validator.py --strict <case.json>`

## Code Review Rules

### Evidence boundaries

- Flag any change that turns a report, expression, or inference into an established event, hidden motive, diagnosis, or certain prediction. Safe path: preserve source attribution, proposition type, verdict status, evidence strength, confidence, and limitations.
- Flag a stable-pattern conclusion based only on duplicate screenshots or one event. Safe path: cluster same-event material and check observation opportunities, time span, contexts, recurrence, trend, and counterexamples.

### Safety and privacy

- Flag any public example containing identifiable private information or lacking separate analysis and publication permission. Safe path: use synthetic cases or fully de-identified, explicitly authorized material.
- Flag ordinary couple-communication advice applied to reported coercive control, violence, stalking, sexual coercion, or credible retaliation. Safe path: keep fact assessment separate from low-regret safety action and do not recommend solo confrontation.

### Symmetry without false equivalence

- Swap gender, income, and narrator roles when reviewing a rule. Flag asymmetric standards unsupported by the evidence.
- Do not force equal responsibility where behavior, power, fear, or harm is unequal.

Leave formatting and mechanical validation to CI.
