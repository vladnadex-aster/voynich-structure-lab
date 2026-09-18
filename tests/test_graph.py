from voynich_structure_lab.graph import connected_components, indel_adjacency, one_deletions


def test_one_deletions_deduplicates_positions():
    assert one_deletions(("a", "a")) == {("a",)}


def test_indel_components():
    words = {
        "a": ("a",),
        "ab": ("a", "b"),
        "abc": ("a", "b", "c"),
        "z": ("z",),
    }
    graph = indel_adjacency(words)
    assert graph["ab"] == {"a", "abc"}
    assert connected_components(graph) == [{"a", "ab", "abc"}, {"z"}]
