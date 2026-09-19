# Voynich Structure Lab

[![CI](https://github.com/vladnadex-aster/voynich-structure-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/vladnadex-aster/voynich-structure-lab/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](pyproject.toml)

A dependency-free Python toolkit for reproducible structural analysis of
tokenized historical texts. It was created for an independent Voynich
Manuscript research program, but every public API is corpus-agnostic.

Researchers often implement token-family graphs in one-off notebooks tied to a
particular transcription. That makes methods hard to audit, reuse, or compare
without copying source data. This project separates the general algorithms from
the corpus: users run the software locally on material they are authorized to
use and receive deterministic, machine-readable measurements.

## What it measures

- configurable longest-first multi-character unit splitting;
- insertion/deletion adjacency and connected components;
- directed one-unit deletion graphs;
- all attested deletion sinks reachable from each type;
- closed four-type deletion diamonds;
- corpus-level JSON summaries with configuration and version metadata.

The runtime package has no third-party dependencies, network client, telemetry,
or bundled corpus.

## Quick start

Requires Python 3.10 or later.

```bash
git clone https://github.com/vladnadex-aster/voynich-structure-lab.git
cd voynich-structure-lab
python -m pip install -e .
printf 'abcd abc abd ab' | vsl-analyze -
```

The output records results and the settings needed to interpret them:

```json
{
  "deletion_diamonds": 1,
  "diamonds_per_1000_types": 250.0,
  "giant_indel_component_fraction": 1.0,
  "minimum_sink_length": 1,
  "schema_version": 1,
  "software_version": "0.2.0",
  "tokens": 4,
  "types": 4,
  "unit_inventory": []
}
```

Analyze a UTF-8 file containing whitespace-separated tokens:

```bash
vsl-analyze path/to/your-tokenized-text.txt
```

Declare multi-character analysis units explicitly and repeat the option as
needed:

```bash
vsl-analyze corpus.txt --multigraph ch --multigraph sh --multigraph cth
```

## Python API

```python
from voynich_structure_lab import (
    deletion_diamonds,
    indel_adjacency,
    reachable_sinks,
    split_units,
)

tokens = {"abcd", "abc", "abd", "ab"}
units = {token: split_units(token) for token in tokens}

print(indel_adjacency(units))
print(reachable_sinks(units))
print(deletion_diamonds(units))
```

See [the methodology](docs/METHODOLOGY.md) for exact definitions and the
[public roadmap](docs/ROADMAP.md) for planned capabilities.

## Reproducible research boundary

The repository contains general-purpose software, synthetic tests, and public
documentation. It does not distribute transcriptions, manuscript images,
research corpora, private findings, or third-party publications. Users remain
responsible for lawful access to their inputs.

The [public-release policy](PUBLIC_RELEASE_POLICY.md) explains the boundary.
CI runs [`scripts/check_public_release.py`](scripts/check_public_release.py) to
catch common data, archive, credential, and private-workspace files before they
enter public history.

The repository's [provenance and rights statement](docs/PROVENANCE_AND_RIGHTS.md)
records what was created for this release, what is excluded, and how external
inputs and development tools are treated.

## Contributing

Bug reports and small, corpus-agnostic contributions are welcome. Please use
invented token strings in reproductions and tests; do not attach source texts.
See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and the
[code of conduct](CODE_OF_CONDUCT.md).

## Project status

This is an early public release under active development. The APIs and JSON
schema are small enough to audit, but compatibility guarantees have not yet
been declared. Releases record schema and behavior changes in the
[changelog](CHANGELOG.md).

Parts of the code and documentation were developed with OpenAI Codex
assistance and reviewed, tested, selected, and maintained by Vlad Kirgiz.

## Citation and license

Citation metadata is available in [CITATION.cff](CITATION.cff). The original
material committed to this repository is released under the [MIT License](LICENSE).
No external dataset, transcription, image, publication, or other third-party
research material is included or relicensed.
