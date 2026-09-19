# Security

## Reporting a vulnerability

Please do not disclose a suspected vulnerability in a public issue. Use
GitHub's private vulnerability reporting feature if it is enabled. Otherwise,
open a minimal issue asking the maintainer for a private contact method; do not
include vulnerability details in that issue. Include the affected version, a
minimal reproduction, and the practical impact.

The maintainer will acknowledge a usable report as soon as practical and will
coordinate disclosure after a fix is available. This is a small volunteer
project and cannot promise a service-level response time.

## Data handling

The package reads user-supplied local text. It has no network client, telemetry,
or bundled research corpus. Users should still avoid passing confidential text
through untrusted wrappers, shells, notebooks, or automation around the package.
