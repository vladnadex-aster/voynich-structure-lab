"""Closed deletion-diamond enumeration."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations

from .deletion import deletion_children


@dataclass(frozen=True, order=True)
class DeletionDiamond:
    top: str
    left: str
    right: str
    bottom: str


def deletion_diamonds(
    words: Mapping[str, Sequence[str]],
    min_length: int = 1,
) -> set[DeletionDiamond]:
    """Enumerate four-type diamonds closed under two one-unit deletions."""

    children = deletion_children(words, min_length=min_length)
    diamonds: set[DeletionDiamond] = set()
    for top, arms in children.items():
        for first, second in combinations(sorted(arms), 2):
            for bottom in children[first] & children[second]:
                diamonds.add(DeletionDiamond(top, first, second, bottom))
    return diamonds
