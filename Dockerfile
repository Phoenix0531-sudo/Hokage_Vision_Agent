# syntax=docker/dockerfile:1.7

ARG PYTHON_IMAGE=python:3.12-slim-bookworm

FROM ${PYTHON_IMAGE} AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=0 \
    PYTHONPATH=/workspace/src

WORKDIR /workspace

ARG DEBIAN_MIRROR=
ARG DEBIAN_SECURITY_MIRROR=

RUN set -eux; \
    if [ -n "$DEBIAN_MIRROR" ] && [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i "s|http://deb.debian.org/debian-security|${DEBIAN_SECURITY_MIRROR:-http://mirrors.ustc.edu.cn/debian-security}|g" /etc/apt/sources.list.d/debian.sources; \
        sed -i "s|http://deb.debian.org/debian|${DEBIAN_MIRROR}|g" /etc/apt/sources.list.d/debian.sources; \
    fi; \
    rm -f /etc/apt/apt.conf.d/docker-clean; \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    set -eux; \
    apt-get update -o Acquire::Retries=5; \
    apt-get install -y -o Acquire::Retries=5 --no-install-recommends ca-certificates; \
    apt-get clean

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip

FROM base AS test-deps

COPY requirements-docker.txt ./

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements-docker.txt

FROM test-deps AS test

COPY pyproject.toml README.md ./
COPY src ./src

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-deps -e .

COPY apps ./apps
COPY configs ./configs
COPY docs ./docs
COPY examples ./examples
COPY scripts ./scripts
COPY tests ./tests
COPY mkdocs.yml ./

CMD ["python", "-c", "import hokage_vision; print(hokage_vision.__version__)"]

FROM test-deps AS api-deps

COPY requirements-api.txt ./

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements-api.txt

FROM api-deps AS api

COPY pyproject.toml README.md ./
COPY src ./src

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-deps -e .

COPY apps ./apps
COPY configs ./configs
COPY docs ./docs
COPY examples ./examples
COPY scripts ./scripts
COPY mkdocs.yml ./

CMD ["hokage-vision", "api", "--host", "0.0.0.0", "--port", "8000"]

FROM test-deps AS docs-deps

COPY requirements-docs.txt ./

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements-docs.txt

FROM docs-deps AS docs

COPY pyproject.toml README.md ./
COPY src ./src

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-deps -e .

COPY docs ./docs
COPY mkdocs.yml ./

CMD ["mkdocs", "build"]

FROM test-deps AS train-deps

COPY requirements-train.txt ./

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements-train.txt

FROM train-deps AS train

COPY pyproject.toml README.md ./
COPY src ./src

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-deps -e .

COPY apps ./apps
COPY configs ./configs
COPY data ./data
COPY examples ./examples
COPY models ./models
COPY scripts ./scripts
COPY mkdocs.yml ./

CMD ["hokage-vision", "train", "yolo", "--data", "configs/dataset.example.yaml", "--epochs", "1", "--dry-run"]

FROM base AS gui-system-deps

ENV QT_QPA_PLATFORM=offscreen \
    QT_API=pyside6 \
    XDG_RUNTIME_DIR=/tmp/runtime-root

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    set -eux; \
    for attempt in 1 2 3; do \
        apt-get update -o Acquire::Retries=5; \
        apt-get install -y -o Acquire::Retries=5 --no-install-recommends \
            libdbus-1-3 \
            libegl1 \
            libfontconfig1 \
            libgl1 \
            libglib2.0-0 \
            libxkbcommon0 && break; \
        if [ "$attempt" = "3" ]; then exit 1; fi; \
        sleep 5; \
    done; \
    mkdir -p /tmp/runtime-root; \
    chmod 700 /tmp/runtime-root; \
    apt-get clean

FROM gui-system-deps AS gui-python-deps

COPY requirements-docker.txt requirements-gui.txt ./

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements-docker.txt -r requirements-gui.txt

FROM gui-python-deps AS gui-test

COPY pyproject.toml README.md ./
COPY src ./src

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-deps -e .

COPY apps ./apps
COPY configs ./configs
COPY docs ./docs
COPY examples ./examples
COPY scripts ./scripts
COPY tests ./tests
COPY mkdocs.yml ./

CMD ["pytest", "tests/gui"]

FROM gui-python-deps AS desktop-build-deps

COPY requirements-desktop-build.txt ./

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt/lists,sharing=locked \
    set -eux; \
    apt-get update -o Acquire::Retries=5; \
    apt-get install -y -o Acquire::Retries=5 --no-install-recommends binutils; \
    apt-get clean

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements-desktop-build.txt

FROM desktop-build-deps AS desktop-build

COPY pyproject.toml README.md ./
COPY src ./src

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-deps -e .

COPY apps ./apps
COPY configs ./configs
COPY docs ./docs
COPY examples ./examples
COPY scripts ./scripts
COPY mkdocs.yml ./

CMD ["python", "scripts/build_desktop.py"]
