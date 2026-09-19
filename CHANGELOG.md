# Changelog

All notable public changes are recorded here.

## Unreleased

- scan exact staged file contents and full `HEAD` history for selected release hazards;
- cover deleted historical files, tracked generated paths, and broken symlinks in tests;
- clarify rights-review limits, AI assistance, and the post-upload timing of CI;
- use read-only CI permissions without persisted checkout credentials.

## 0.2.0 — 2026-09-19

- expose graph, deletion, and diamond functions from the top-level package;
- accept explicit multi-character units in the command-line interface;
- accept token streams on standard input;
- include a schema version, software version, and analysis configuration in JSON output;
- add contributor support documents, issue forms, and a public roadmap.

## 0.1.0 — 2026-09-18

- initial public release of unit splitting, insertion/deletion graphs,
  deletion sinks, closed diamonds, JSON summaries, tests, and CI.
