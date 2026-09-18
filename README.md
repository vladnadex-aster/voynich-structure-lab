# Voynich Structure Lab

An open-source Python toolkit for reproducible structural analysis of tokenized historical texts, developed as part of an independent Voynich Manuscript research project.

## Public scope

This repository contains only general-purpose software selected for public release:

- configurable multi-character unit splitting;
- insertion/deletion graph construction;
- connected-component measurement;
- deletion-sink and closed-diamond utilities;
- a command-line summary tool;
- synthetic tests and continuous integration.

It does **not** contain research corpora, transcriptions, manuscript images, source inventories, private notes, experimental notebooks, findings, interpretations, hypotheses, or decipherment material.

## Quick start

Requires Python 3.10 or later.

```bash
git clone https://github.com/vladnadex-aster/voynich-structure-lab.git
cd voynich-structure-lab
python -m pip install -e .
vsl-analyze path/to/your-own-tokenized-text.txt
```

Input is a UTF-8 file containing whitespace-separated tokens. Users are responsible for ensuring that they have the right to use their inputs. The program reads local input; it does not upload, bundle, or redistribute it.

Example with synthetic strings:

```python
from voynich_structure_lab import split_units
from voynich_structure_lab.deletion import reachable_sinks
from voynich_structure_lab.diamonds import deletion_diamonds

words = {"abcd", "abc", "abd", "ab"}
units = {word: split_units(word) for word in words}

print(reachable_sinks(units))
print(deletion_diamonds(units))
```

## Public-release boundary

[`PUBLIC_RELEASE_POLICY.md`](PUBLIC_RELEASE_POLICY.md) defines what may enter this repository. [`scripts/check_public_release.py`](scripts/check_public_release.py) enforces the basic file and secret boundary in CI.

## Independence

This is an independent research-software project. Descriptive references to the Voynich Manuscript do not imply endorsement by or affiliation with any library, university, researcher, data provider, or other organization.

## Development note

Parts of the code and documentation were developed with OpenAI Codex assistance and reviewed, tested, selected, and maintained by the project maintainer.

## License

The material committed to this repository is released under the [MIT License](LICENSE). No external dataset, transcription, image, publication, or other third-party research material is included or relicensed.
