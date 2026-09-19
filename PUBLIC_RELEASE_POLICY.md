# Public release policy

Last reviewed: 2026-09-19

This repository is a deliberately limited public software release. The underlying research project, its sources, working materials, analysis, and results are private unless the maintainer expressly approves a separate public release.

## Allowed public content

- original general-purpose source code selected for release;
- synthetic test fixtures created for this repository;
- minimal software documentation;
- build, test, and security configuration;
- the repository license and public citation metadata.

## Prohibited public content

- research corpora, transcriptions, source inventories, or source archives;
- manuscript scans, crops, annotations, or derived images;
- private or licensed documents and permission correspondence;
- research notebooks, working logs, prompts, handoffs, or conversation exports;
- findings, numerical results, interpretations, hypotheses, or proposed keys;
- unreleased methods or strategic research plans;
- credentials, organization identifiers, tokens, cookies, personal information, or private links;
- third-party code, prose, tables, figures, or data not separately approved for release;
- any material whose ownership, license, confidentiality, or release status is uncertain.

## Third-party material

No third-party research material is included in the initial release. Public availability elsewhere does not create permission to copy, modify, or relicense it. Any future exception requires a separate rights review, compatible license or written permission, required notices, and explicit maintainer approval before the material enters Git history.

General analytical ideas, facts, and methods are not claimed as exclusive inventions of this project. The repository licenses only the expression and code actually contributed here to the extent the contributor has rights to license it.

## Input responsibility

The software can process user-supplied local files. Possession of the software does not grant rights to any input material. Users are solely responsible for obtaining lawful access to and authorization for their inputs and for complying with any applicable terms.

## Contributions

Contributors must have the right to submit their work and license it under the repository's MIT License. Submissions containing external datasets, manuscript material, confidential information, or uncertain intellectual property will not be accepted.

## Automated boundary

The public-boundary checker blocks common data, archive, image, credential, notebook, and private-workspace formats; oversized files; and recognizable secret patterns. It reduces accidental disclosure but does not replace human review.

Before every public release, the maintainer must review the complete Git diff and confirm that every added line and file is intentionally public.

The release review must also confirm that examples are invented, API names and
documentation do not reveal private source identities or findings, third-party
dependencies are declared, and all copyright and attribution statements remain
accurate. Passing the automated check is necessary but not sufficient.

## No endorsement; no warranty

The project is independent and does not imply endorsement by any institution, researcher, platform, or data provider. The software is provided without warranty under the MIT License. This policy is a conservative project rule, not legal advice or a guarantee that disputes are impossible.

## Takedown

A person who believes that material in the repository infringes their rights may identify the specific path and basis of the concern through a GitHub issue. Disputed material will be reviewed promptly and may be disabled while the claim is evaluated.
