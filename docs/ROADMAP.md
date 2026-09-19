# Public roadmap

Voynich Structure Lab aims to make structural comparisons of tokenized
historical texts easier to reproduce without distributing the texts themselves.

## Near term

- provenance manifests generated alongside analysis output;
- length- and type-count-matched comparison utilities;
- edit-operation summaries for connected token families;
- bounded-memory processing for larger vocabularies;
- documented Python and command-line examples using synthetic inputs;
- stable JSON schemas with compatibility tests.

## Later

- optional graph exports in common open formats;
- resampling and permutation helpers with explicit seeds;
- validation against openly licensed benchmark corpora;
- packaged releases and archival software citations.

Each addition must remain corpus-agnostic, deterministic where possible, and
covered by synthetic tests. Research interpretations and source materials are
outside the public package.
