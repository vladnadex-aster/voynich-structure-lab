# Contributing

Small contributions to the public software are welcome. Do not submit research data, transcriptions, manuscript images, source information, private results, hypotheses, prompts, logs, or confidential material.

By submitting a contribution, you certify that:

1. you created it or otherwise have the right to submit it;
2. you have the right to license it under this repository's MIT License;
3. it contains no confidential or restricted material; and
4. you understand that maintainers may reject or remove it to protect the public-release boundary.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python scripts/check_public_release.py
```

Tests must use synthetic strings created for this repository.

## Before opening a pull request

```bash
python -m pytest
python -m ruff check .
python scripts/check_public_release.py
```

Explain the general problem, include a minimal synthetic example, and document
any output-schema or compatibility change in `CHANGELOG.md`. Keep each pull
request focused enough to review without access to a private corpus.
