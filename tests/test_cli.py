from voynich_structure_lab.cli import summarize


def test_summary_is_deterministic():
    result = summarize(["abc", "ab", "ac", "a", "abc"])
    assert result["tokens"] == 5
    assert result["types"] == 4
    assert result["deletion_diamonds"] == 1
    assert result["giant_indel_component_fraction"] == 1.0
