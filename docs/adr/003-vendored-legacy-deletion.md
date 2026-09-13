# ADR-003: Delete the vendored YOLOv5 toolchain

**Status:** Accepted · **Date:** 2026-09-09 (commit `ddc2e3a`)

## Context

The repo carried `legacy/old_project/` — a 13.8 MB vendored copy of the
GPL-3.0-era Ultralytics YOLOv5 (177 files), inherited from the original
fork. It had no tests, no CI coverage, and made every license question
about the repo ambiguous. Options considered: (a) delete, (b) keep and
document, (c) archive to a branch.

## Decision

**Delete it, behind a documented audit.** A read-only dependency audit
(`rg` over src/CI/Dockerfile/docs) proved:

- nothing in `src/hokage_vision` imports the legacy package,
- no workflow, Dockerfile, or docs *depend* on it existing,
- the only linkage is `YOLOv5LegacyBackend`, which `torch.hub`-loads
  the tree *if and only if* a user explicitly selects that backend.

The deletion (`git rm -r legacy/`, 24,111 lines) kept the boundary
class: with the tree gone, that backend now raises
`VisionBackendError` pointing users at the migration guide — a
designed behavior, tested in `tests/unit/test_real_backends.py`.

## Consequences

- ✅ Repo shrank 13.8 MB; the Apache-2.0 story became unambiguous.
- ✅ Provenance preserved: `docs/license-audit.md` cites the git
  history snapshot instead of the working tree.
- ⚠️ Anyone wanting the old toolchain must check out a pre-deletion
  commit (documented in the migration guide).
- ⚠️ `yolov5_legacy` remains a registered backend that errors without
  the tree — intentional, so old configs fail loudly instead of
  silently switching backends.
