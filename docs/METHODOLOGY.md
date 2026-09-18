# Public software methodology

The public toolkit operates on abstract token sequences. It makes no claim about the meaning, origin, language, or interpretation of any manuscript.

## Unit splitting

A token can be represented as single characters or split with a caller-supplied list of multi-character units. The inventory is never inferred from private research data by the public package.

## Insertion/deletion graph

Each distinct token is represented as a tuple of units. Two types are adjacent when one can be obtained from the other by inserting or deleting exactly one unit.

## Deletion sinks

Edges can be oriented from longer to shorter types. A sink is a present type with no further one-unit deletion present above the selected length floor. The toolkit can list the sinks reachable from each type.

## Closed deletion diamonds

A closed diamond contains a top type, two distinct attested one-unit deletions, and a shared attested lower type. The toolkit enumerates these four-type structures.

## Reproducibility

Users should record their own software version, input checksum, preprocessing choices, unit inventory, command, and random seed where relevant. Those records are private unless separately approved for release.

The software reports structural measurements only. Interpretation remains outside the public package.
