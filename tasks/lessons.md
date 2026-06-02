# Lessons

- Docker dependency layers must stay independent from source changes. Keep apt, pip, PySide6, and GUI system dependencies before any source `COPY`, split normal test and GUI test dependency chains, and use BuildKit cache mounts for apt and pip. Use pinned Docker requirement files to avoid slow pip backtracking. For PySide6 headless tests, start from the offscreen minimum set, but keep `libgl1` when pytest-qt imports `QtGui` because it requires `libGL.so.1`.
- For portfolio/open-source cleanup, keep `tests/` in the repository because CI, GUI smoke tests, and reproducible demos are part of the deliverable. Reduce clutter by consolidating docs and old template files instead of deleting tests.
- Preserve legacy visibility explicitly. If a refactor keeps old code only in git history, create or document an archive branch before pruning branch clutter so the original version is easy to find.
- Portfolio projects need visible identity, not only scaffolding. GUI, docs, README, and About pages should carry the project theme while avoiding copyrighted official logos or redistributed fan assets.
- GitHub repository About is repository metadata, not a README section. Use the repo description/homepage/topics for the right sidebar and keep README content focused on usage.
- Release workflows should upload packaged artifacts, not raw PyInstaller directories. Zip desktop bundles first so GitHub Releases contain a small, readable asset set.
- For this project, Docker is the primary validation environment. Local Python or Anaconda checks are only supplementary and must not be presented as the main acceptance result.
- Remove unused reserved backends instead of keeping placeholder code when the user is asking for a polished, runnable portfolio project.
