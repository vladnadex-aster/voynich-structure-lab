"""Fail CI when common private or non-source artifacts enter public Git history."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 500_000

BLOCKED_SUFFIXES = {
    ".7z",
    ".csv",
    ".db",
    ".gz",
    ".ipynb",
    ".jpeg",
    ".jpg",
    ".jsonl",
    ".key",
    ".p12",
    ".pdf",
    ".pem",
    ".png",
    ".sqlite",
    ".tar",
    ".tif",
    ".tiff",
    ".token",
    ".tsv",
    ".txt",
    ".zip",
}

BLOCKED_PARTS = {"private", "sources", "working", "notebooks", "results", "raw", "derived"}

BLOCKED_NAMES = {
    ".env",
    ".netrc",
    ".npmrc",
    ".pypirc",
    "credentials",
    "credentials.json",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
}

SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "OpenAI organization identifier": re.compile(r"\borg-[A-Za-z0-9_-]{8,}\b"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "generic bearer token": re.compile(r"(?i)authorization\s*:\s*bearer\s+[A-Za-z0-9._~+/-]{16,}"),
    "generic assigned secret": re.compile(
        r"(?i)\b(?:api[_-]?key|client[_-]?secret|password|secret|token)\b\s*[:=]\s*"
        r"['\"]?[A-Za-z0-9._~+/-]{16,}"
    ),
}

ALLOWED_BLOCKED_SUFFIX_PATHS = {Path("data/README.md")}


def is_generated(path: Path) -> bool:
    return any(
        part == "__pycache__"
        or part.endswith(".egg-info")
        or part in {".git", ".pytest_cache", ".ruff_cache"}
        for part in path.parts
    )


def tracked_files() -> list[Path]:
    try:
        output = subprocess.check_output(
            ["git", "ls-files"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        )
        return [Path(line) for line in output.splitlines() if line]
    except (OSError, subprocess.CalledProcessError):
        return [path.relative_to(ROOT) for path in ROOT.rglob("*") if path.is_file()]


def main() -> int:
    problems: list[str] = []
    for relative in tracked_files():
        path = ROOT / relative
        if not path.exists() or is_generated(relative):
            continue
        if path.is_symlink():
            problems.append(f"symbolic link requires manual approval: {relative}")
            continue
        if any(part.lower() in BLOCKED_PARTS for part in relative.parts):
            problems.append(f"blocked private-workspace path: {relative}")
        if relative.name.lower() in BLOCKED_NAMES or relative.name.lower().startswith(".env."):
            problems.append(f"blocked credential filename: {relative}")
        if relative.suffix.lower() in BLOCKED_SUFFIXES and relative not in ALLOWED_BLOCKED_SUFFIX_PATHS:
            problems.append(f"blocked data/binary extension: {relative}")
        if path.stat().st_size > MAX_BYTES:
            problems.append(f"file exceeds {MAX_BYTES} bytes: {relative}")
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems.append(f"non-UTF-8 file: {relative}")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                problems.append(f"possible {label}: {relative}")

    if problems:
        print("Public-release boundary check failed:")
        for problem in sorted(set(problems)):
            print(f"- {problem}")
        return 1
    print("Public-release boundary check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
