"""Command-line summary for a whitespace-tokenized corpus."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .deletion import reachable_sinks
from .diamonds import deletion_diamonds
from .graph import connected_components, indel_adjacency
from .units import split_units


def summarize(
    tokens: list[str],
    min_length: int = 1,
    multigraphs: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Summarize the type-family geometry of a token sequence."""

    if min_length < 1:
        raise ValueError("min_length must be at least 1")
    if any(not value or any(character.isspace() for character in value) for value in multigraphs):
        raise ValueError("multigraphs must be nonempty and contain no whitespace")
    vocabulary = sorted(set(tokens))
    words = {word: split_units(word, multigraphs) for word in vocabulary}
    adjacency = indel_adjacency(words)
    components = connected_components(adjacency)
    sinks = reachable_sinks(words, min_length=min_length)
    diamonds = deletion_diamonds(words, min_length=min_length)
    unique_sink_types = sum(len(value) == 1 for value in sinks.values())
    mean_sinks = sum(map(len, sinks.values())) / len(sinks) if sinks else 0.0
    giant = len(components[0]) if components else 0
    return {
        "schema_version": 1,
        "software_version": __version__,
        "unit_inventory": sorted(set(multigraphs), key=lambda item: (-len(item), item)),
        "minimum_sink_length": min_length,
        "tokens": len(tokens),
        "types": len(vocabulary),
        "giant_indel_component_types": giant,
        "giant_indel_component_fraction": giant / len(vocabulary) if vocabulary else 0.0,
        "unique_sink_types": unique_sink_types,
        "unique_sink_fraction": unique_sink_types / len(vocabulary) if vocabulary else 0.0,
        "mean_reachable_sinks": mean_sinks,
        "deletion_diamonds": len(diamonds),
        "diamonds_per_1000_types": 1000 * len(diamonds) / len(vocabulary)
        if vocabulary
        else 0.0,
    }


def _read_tokens(source: str) -> list[str]:
    if source == "-":
        return sys.stdin.read().split()
    return Path(source).read_text(encoding="utf-8").split()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", help="UTF-8 whitespace-tokenized corpus, or - for stdin")
    parser.add_argument("--min-length", type=int, default=1, help="minimum deletion-sink length")
    parser.add_argument(
        "--multigraph",
        action="append",
        default=[],
        help="multi-character analysis unit; repeat for more than one",
    )
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    try:
        result = summarize(
            _read_tokens(args.corpus),
            min_length=args.min_length,
            multigraphs=tuple(args.multigraph),
        )
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=args.indent, sort_keys=True))


if __name__ == "__main__":
    main()
