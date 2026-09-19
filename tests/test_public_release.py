"""Synthetic release-check regressions in isolated temporary repositories."""

import importlib.util
import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def release_check(tmp_path, monkeypatch):
    script = Path(__file__).resolve().parents[1] / "scripts" / "check_public_release.py"
    spec = importlib.util.spec_from_file_location("release_check", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    return module, tmp_path


def git(root, *args):
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def commit(root):
    git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
        "-c", "commit.gpgsign=false", "commit", "-qm", "Synthetic fixture")


def test_untracked_file_is_checked(release_check):
    checker, root = release_check
    (root / "fixture.csv").write_text("a,b\n", encoding="utf-8")
    assert checker.main([]) == 1


def test_staged_bytes_are_checked_even_when_working_copy_is_safe(release_check, capsys):
    checker, root = release_check
    sample = "gh" + "p_" + "A" * 36
    (root / "example.md").write_text(sample, encoding="utf-8")
    git(root, "add", "example.md")
    (root / "example.md").write_text("Safe synthetic text", encoding="utf-8")
    assert checker.main([]) == 0
    assert checker.main(["--staged"]) == 1
    output = capsys.readouterr().out
    assert "possible GitHub token" in output
    assert sample not in output


def test_deleted_historical_file_is_checked(release_check):
    checker, root = release_check
    (root / "fixture.csv").write_text("a,b\n", encoding="utf-8")
    git(root, "add", "fixture.csv")
    commit(root)
    git(root, "rm", "fixture.csv")
    commit(root)
    assert checker.main(["--staged"]) == 0
    assert checker.main(["--history"]) == 1


def test_tracked_generated_path_is_not_exempt(release_check):
    checker, root = release_check
    generated = root / "__pycache__"
    generated.mkdir()
    (generated / "fixture.csv").write_text("a,b\n", encoding="utf-8")
    git(root, "add", "__pycache__/fixture.csv")
    assert checker.main([]) == 1


def test_broken_symlink_is_rejected(release_check):
    checker, root = release_check
    try:
        (root / "example.md").symlink_to("missing.md")
    except OSError:
        pytest.skip("Symlinks are unavailable on this platform")
    assert checker.main([]) == 1


def test_binary_content_is_rejected(release_check):
    checker, _ = release_check
    assert "non-UTF-8 file: example.md" in checker.check_content(Path("example.md"), b"\xff")


def test_git_failure_does_not_report_success(release_check, monkeypatch):
    checker, _ = release_check

    def failed_git(*args):
        raise subprocess.CalledProcessError(1, "git")

    monkeypatch.setattr(checker, "git_output", failed_git)
    assert checker.main(["--staged"]) == 2


def test_clean_history_passes(release_check):
    checker, root = release_check
    (root / "example.md").write_text("Invented example: abcd", encoding="utf-8")
    git(root, "add", "example.md")
    commit(root)
    assert checker.main(["--history"]) == 0
