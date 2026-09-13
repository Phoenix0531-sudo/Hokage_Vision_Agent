# ADR-008: GHCR push + three-OS desktop releases

**Status:** Accepted · **Date:** 2026-09-11 (commit `719da43`)

## Context

The repo had CI builds but nothing consumable outside it: the Docker
workflow only *tested* the image, and the release workflow zipped a
Linux desktop build only. A portfolio project that says "download and
try it" needs artifacts people can actually pull.

## Decision

- **Docker**: `docker/login-action@v3` against GHCR on
  `packages:write`, pushing only after tests pass. `master` pushes
  tag `hokage_vision_agent:api` (+ short SHA); `v*` tags additionally
  push `vX.Y.Z`.
- **Desktop**: the release job's zip step became a 3-OS matrix
  (linux/windows/macos, non-ubuntu `continue-on-error`), all
  `desktop-*` artifacts collected and attached to the GitHub Release.
- **Notes**: a `changelog → release-notes.md` extraction step feeds
  `body_path`, plus `generate_release_notes: true` for the commit
  diff.

## Consequences

- ✅ v0.1.2 shipped `desktop-{linux,windows,macos}.zip`, wheel, and
  sdist; `docker pull ghcr.io/phoenix0531-sudo/hokage_vision_agent` works.
- ✅ Push-to-registry is coupled to test success — no untested image
  ever leaves the building.
- ⚠️ Desktop zips are ~100–240 MB and unsigned (no code-signing
  certs) — documented as "for evaluation".
- ⚠️ Non-ubuntu desktop jobs are `continue-on-error`; a macOS
  packaging failure won't block a release, trading strictness for
  shipping cadence (revisit when macOS contributors appear).
