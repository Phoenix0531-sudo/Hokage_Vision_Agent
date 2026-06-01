from __future__ import annotations

from collections import Counter


def class_distribution(labels: list[list[float]]) -> dict[int, int]:
    counts: Counter[int] = Counter()
    for row in labels:
        if row:
            counts[int(row[0])] += 1
    return dict(sorted(counts.items()))
