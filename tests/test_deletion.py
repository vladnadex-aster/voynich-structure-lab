from voynich_structure_lab.deletion import reachable_sinks


def test_multiple_reachable_sinks():
    words = {
        "abc": ("a", "b", "c"),
        "ab": ("a", "b"),
        "bc": ("b", "c"),
        "a": ("a",),
        "c": ("c",),
    }
    sinks = reachable_sinks(words)
    assert sinks["abc"] == frozenset({"a", "c"})
