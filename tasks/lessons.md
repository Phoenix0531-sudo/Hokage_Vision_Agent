# Lessons

- Docker dependency layers must stay independent from source changes. Keep apt, pip, PySide6, and GUI system dependencies before any source `COPY`, split normal test and GUI test dependency chains, and use BuildKit cache mounts for apt and pip. Use pinned Docker requirement files to avoid slow pip backtracking. For PySide6 headless tests, start from the offscreen minimum set, but keep `libgl1` when pytest-qt imports `QtGui` because it requires `libGL.so.1`.
