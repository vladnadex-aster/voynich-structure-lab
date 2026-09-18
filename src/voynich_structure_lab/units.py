"""Configurable token unitization with no corpus-specific defaults."""

from __future__ import annotations

from collections.abc import Iterable


def split_units(
    token: str,
    multigraphs: Iterable[str] = (),
) -> tuple[str, ...]:
    """Split a token using caller-supplied multi-character units.

    Matching is longest-first. With no supplied inventory, each character is a
    unit. The public package intentionally contains no corpus-derived inventory.
    """

    choices = tuple(sorted(set(multigraphs), key=lambda item: (-len(item), item)))
    units: list[str] = []
    index = 0
    while index < len(token):
        match = next((item for item in choices if token.startswith(item, index)), None)
        if match is None:
            units.append(token[index])
            index += 1
        else:
            units.append(match)
            index += len(match)
    return tuple(units)
