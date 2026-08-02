# Codex automation design

Codex is an additional reviewer, not the source of truth and not a replacement for deterministic tests or human privacy review.

## Implemented workflow

`.github/workflows/codex-review.yml` runs `openai/codex-action@v1` on pull requests when an `OPENAI_API_KEY` repository secret is available. It uses a committed review prompt and a read-only sandbox. The output is stored as a workflow artifact for maintainer review.

The prompt asks Codex to inspect:

- evidence-to-claim mismatches;
- mind-reading, diagnosis, or unsupported certainty;
- duplicate evidence counted as independent events;
- gender or income asymmetry;
- privacy and publication authorization;
- safety advice that incorrectly treats coercive control as ordinary conflict;
- missing regression tests for rule changes.

## Deterministic checks stay separate

CI always runs without an OpenAI key and verifies:

- case JSON structure;
- consent and de-identification fields;
- obvious privacy patterns;
- Skill file links and required boundaries;
- parity between the packaged validator and the Skill validator;
- unit tests.

## Security controls

- Keep the Codex action read-only and use the default privilege-dropping strategy.
- Do not expose repository secrets to arbitrary fork code.
- Do not interpolate PR bodies, issue text, or hidden HTML directly into the system prompt.
- Treat Codex output as untrusted review advice requiring maintainer judgment.
- Rotate the API key if workflow output or logs may have exposed it.

## Future automation

After the project has real maintainers and stable tests, consider adding:

1. issue triage that suggests labels but does not publish private case details;
2. release-note drafting from merged, labeled pull requests;
3. structured review output enforced by a JSON schema;
4. scheduled drift checks comparing the Skill, examples, and policies;
5. Codex Security only after repository ownership and authorization are verified.
