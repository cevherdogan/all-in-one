# Branch & Tag Strategy

## Branches
- `main` — protected. Only merged PRs.
- `feature/<short>` — new content/feature.
- `fix/<short>` — bug or typo fixes.
- `docs/<short>` — documentation‑only.

## Tags
- **TGIF tags**: `tgif-YYYYMMDD` (Friday ship ritual)
- **Semantic**: `vMAJOR.MINOR.PATCH`
  - MAJOR: breaking changes
  - MINOR: new features/content
  - PATCH: fixes

## PR Requirements
- Passing checks
- Linked issue (if applicable)
- Update `CHANGELOG.md` for meaningful changes
