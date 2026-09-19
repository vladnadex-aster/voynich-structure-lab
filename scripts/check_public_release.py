"""Check working files, the Git index, or HEAD history for common release hazards."""

from __future__ import annotations

import argparse
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

def git_output(*args: str) -> bytes:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, stderr=subprocess.DEVNULL
    )


def check_content(relative: Path, data: bytes) -> list[str]:
    """Return labels and paths, never matched secret values."""
    problems: list[str] = []
    if any(part.lower() in BLOCKED_PARTS for part in relative.parts):
        problems.append(f"blocked private-workspace path: {relative}")
    if relative.name.lower() in BLOCKED_NAMES or relative.name.lower().startswith(".env."):
        problems.append(f"blocked credential filename: {relative}")
    if relative.suffix.lower() in BLOCKED_SUFFIXES:
        problems.append(f"blocked data/binary extension: {relative}")
    if len(data) > MAX_BYTES:
        problems.append(f"file exceeds {MAX_BYTES} bytes: {relative}")
    try:
        content = data.decode("utf-8")
    except UnicodeDecodeError:
        return [*problems, f"non-UTF-8 file: {relative}"]
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(content):
            problems.append(f"possible {label}: {relative}")
    return problems


def check_working_files() -> list[str]:
    output = git_output("ls-files", "-z", "--cached", "--others", "--exclude-standard")
    problems: list[str] = []
    for name in set(output.split(b"\0")) - {b""}:
        relative = Path(name.decode("utf-8"))
        path = ROOT / relative
        if path.is_symlink():
            problems.append(f"symbolic link requires manual approval: {relative}")
        elif path.is_file():
            problems.extend(check_content(relative, path.read_bytes()))
        elif path.exists():
            problems.append(f"non-regular file requires manual approval: {relative}")
        # Deleted working files are absent here; --staged and --history check Git objects.
    return problems


def check_git_objects(history: bool) -> list[str]:
    problems: list[str] = []
    seen: set[tuple[bytes, bytes, bytes]] = set()
    if history:
        if git_output("rev-parse", "--is-shallow-repository").strip() == b"true":
            return ["history is incomplete: fetch the full history before checking"]
        revisions = git_output("rev-list", "HEAD").decode("ascii").splitlines()
    else:
        revisions = [None]
    for revision in revisions:
        if revision is None:
            output = git_output("ls-files", "--stage", "-z")
        else:
            output = git_output("ls-tree", "-r", "-z", revision)
        for record in output.split(b"\0"):
            if not record:
                continue
            metadata, name = record.split(b"\t", 1)
            fields = metadata.split()
            mode, sha = fields[0], fields[2] if history else fields[1]
            key = (name, mode, sha)
            if key in seen:
                continue
            seen.add(key)
            relative = Path(name.decode("utf-8"))
            if not history and fields[2] != b"0":
                problems.append(f"unmerged index entry: {relative}")
                continue
            if mode not in {b"100644", b"100755"}:
                problems.append(f"non-regular Git entry requires manual approval: {relative}")
                continue
            data = git_output("cat-file", "blob", sha.decode("ascii"))
            location = f"history {revision[:12]}" if revision else "index"
            problems.extend(f"{item} ({location})" for item in check_content(relative, data))
        if revision is not None:
            message = git_output("show", "-s", "--format=%B", revision).decode("utf-8")
            for label, pattern in SECRET_PATTERNS.items():
                if pattern.search(message):
                    problems.append(f"possible {label} in commit message {revision[:12]}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--staged", action="store_true", help="inspect exact Git index contents")
    modes.add_argument("--history", action="store_true", help="inspect all commits reachable from HEAD")
    args = parser.parse_args(argv)
    try:
        problems = (
            check_git_objects(history=args.history)
            if args.staged or args.history
            else check_working_files()
        )
    except (OSError, UnicodeError, subprocess.CalledProcessError):
        print("Public-release boundary check could not complete; stop and inspect the repository.")
        return 2

    if problems:
        print("Public-release boundary check failed:")
        for problem in sorted(set(problems)):
            print(f"- {problem}")
        return 1
    scope = "HEAD history" if args.history else "Git index" if args.staged else "working files"
    print(f"Public-release boundary check passed ({scope}); manual rights review is still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
