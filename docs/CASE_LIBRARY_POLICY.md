# Case library policy

The public case library is a regression-test collection, not a database of real couples.

## Accepted material

- Synthetic cases that do not map to a specific real person.
- Fully de-identified real cases with explicit permission for analysis and separate explicit permission for publication.
- Publicly available material only when reuse is lawful, ethical, necessary, and documented; public availability alone is not permission to repackage intimate details.

## Rejected material

- Raw chat screenshots, names, handles, phone numbers, addresses, employers, schools, IDs, or exact locations.
- Material obtained by account access, surveillance, impersonation, tracking, or another privacy violation.
- Cases involving minors' identifiable information.
- Submissions intended to prove that a named person cheated, has a disorder, is abusive, or acted from one hidden motive.
- Material whose publication may increase retaliation, stalking, coercion, or reputational harm.

## Review pipeline

1. Submit a minimal synthetic case when possible.
2. Run the strict case validator.
3. Confirm separate analysis and publication permissions.
4. Perform human re-identification and safety review.
5. Identify the exact regression the case covers.
6. Add an expected-boundary test, not a predetermined verdict about a real person.
7. Re-review after each rule change that affects the case.

Automated scanning only detects obvious patterns. Passing it does not prove anonymity, consent, truth, legal compliance, or safety.
