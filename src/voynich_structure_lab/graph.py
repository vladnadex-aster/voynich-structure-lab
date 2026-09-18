"""Insertion/deletion family graphs without third-party dependencies."""

from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Iterable, Mapping, Sequence

Units = tuple[str, ...]


def one_deletions(units: Sequence[str]) -> set[Units]:
    """Return unique sequences formed by deleting exactly one unit."""

    value = tuple(units)
    return {value[:index] + value[index + 1 :] for index in range(len(value))}


def indel_adjacency(words: Mapping[str, Sequence[str]]) -> dict[str, set[str]]:
    """Build an undirected graph joining types one insertion/deletion apart."""

    by_units: dict[Units, list[str]] = defaultdict(list)
    for word, units in words.items():
        by_units[tuple(units)].append(word)

    adjacency = {word: set() for word in words}
    for longer, units in words.items():
        for shortened in one_deletions(units):
            for shorter in by_units.get(shortened, ()):
                if shorter != longer:
                    adjacency[longer].add(shorter)
                    adjacency[shorter].add(longer)
    return adjacency


def connected_components(adjacency: Mapping[str, Iterable[str]]) -> list[set[str]]:
    """Return connected components, largest first."""

    remaining = set(adjacency)
    components: list[set[str]] = []
    while remaining:
        seed = min(remaining)
        component = {seed}
        queue = deque([seed])
        remaining.remove(seed)
        while queue:
            current = queue.popleft()
            for neighbor in adjacency[current]:
                if neighbor in remaining:
                    remaining.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        components.append(component)
    return sorted(components, key=lambda group: (-len(group), min(group)))
