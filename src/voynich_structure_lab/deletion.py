"""Deletion DAG and reachable-sink metrics."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from functools import cache

from .graph import one_deletions


def deletion_children(
    words: Mapping[str, Sequence[str]],
    min_length: int = 1,
) -> dict[str, set[str]]:
    """Orient present one-deletion relations from longer to shorter types."""

    by_units = {tuple(units): word for word, units in words.items()}
    children: dict[str, set[str]] = {word: set() for word in words}
    for word, units in words.items():
        if len(units) <= min_length:
            continue
        for shortened in one_deletions(units):
            child = by_units.get(shortened)
            if child is not None and len(shortened) >= min_length:
                children[word].add(child)
    return children


def reachable_sinks(
    words: Mapping[str, Sequence[str]],
    min_length: int = 1,
) -> dict[str, frozenset[str]]:
    """Return every attested terminal deletion type reachable from each type."""

    children = deletion_children(words, min_length=min_length)

    @cache
    def visit(word: str) -> frozenset[str]:
        if not children[word]:
            return frozenset((word,))
        return frozenset(sink for child in children[word] for sink in visit(child))

    return {word: visit(word) for word in words}
