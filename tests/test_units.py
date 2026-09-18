from voynich_structure_lab.units import split_units


def test_longest_match_unitization():
    assert split_units("abcd", multigraphs=("ab", "abc")) == ("abc", "d")


def test_default_is_character_units():
    assert split_units("abcd") == ("a", "b", "c", "d")
