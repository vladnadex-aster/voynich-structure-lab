"""Command-line summary for a whitespace-tokenized corpus."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .deletion import reachable_sinks
from .diamonds import deletion_diamonds
from .graph import connected_components, indel_adjacency
from .units import split_units


def summarize(tokens: list[str], min_length: int = 1) -> dict[str, int | float]:
    vocabulary = sorted(set(tokens))
    words = {word: split_units(word) for word in vocabulary}
    adjacency = indel_adjacency(words)
    components = connected_components(adjacency)
    sinks = reachable_sinks(words, min_length=min_length)
    diamonds = deletion_diamonds(words, min_length=min_length)
    unique_sink_types = sum(len(value) == 1 for value in sinks.values())
    mean_sinks = sum(map(len, sinks.values())) / len(sinks) if sinks else 0.0
    giant = len(components[0]) if components else 0
    return {
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path, help="UTF-8 whitespace-tokenized corpus")
    parser.add_argument("--min-length", type=int, default=1, help="minimum deletion-sink length")
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation")
    args = parser.parse_args()
    tokens = args.corpus.read_text(encoding="utf-8").split()
    print(json.dumps(summarize(tokens, args.min_length), indent=args.indent, sort_keys=True))


if __name__ == "__main__":
    main()
