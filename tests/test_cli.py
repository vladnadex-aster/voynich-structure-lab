from voynich_structure_lab.cli import summarize


def test_summary_is_deterministic():
    result = summarize(["abc", "ab", "ac", "a", "abc"])
    assert result["tokens"] == 5
    assert result["types"] == 4
    assert result["deletion_diamonds"] == 1
    assert result["giant_indel_component_fraction"] == 1.0
    assert result["schema_version"] == 1


def test_summary_uses_explicit_multigraph_inventory():
    character_result = summarize(["abc", "c"])
    multigraph_result = summarize(["abc", "c"], multigraphs=("ab",))
    assert character_result["giant_indel_component_fraction"] == 0.5
    assert multigraph_result["giant_indel_component_fraction"] == 1.0
    assert multigraph_result["unit_inventory"] == ["ab"]


def test_summary_rejects_invalid_configuration():
    try:
        summarize(["abc"], min_length=0)
    except ValueError as error:
        assert str(error) == "min_length must be at least 1"
    else:
        raise AssertionError("invalid minimum length was accepted")
