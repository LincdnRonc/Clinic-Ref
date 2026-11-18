# Working on this site

## Version number (every change)
Every commit that changes the site must bump the version in `version.py` and add a line to `HISTORY`:
- Format `MONTH.RELEASE[.PATCH]`, e.g. `11.4` = fourth November update.
- Normal update (new page, section or content change): bump RELEASE, `11.3` → `11.4`.
- Small fix (typo, link, single figure): add or bump PATCH, `11.3` → `11.3.1` → `11.3.2`.
- New month: restart at `.1` (first December update is `12.1`).
- Also update `VERSION_DATE`. `build.py` writes the version into every page header and the home-page footer; never hard-code a date label like "Synthesised Nov 2026".
- Mention the new version number in the commit message and the session report.

## Finishing a session
1. `python3 build.py`, then `python3 tools/check.py <changed pages>`.
2. One commit per session, pushed to `main`.
