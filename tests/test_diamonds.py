from voynich_structure_lab.diamonds import DeletionDiamond, deletion_diamonds


def test_closed_deletion_diamond():
    words = {
        "abc": ("a", "b", "c"),
        "ab": ("a", "b"),
        "ac": ("a", "c"),
        "a": ("a",),
    }
    assert deletion_diamonds(words) == {DeletionDiamond("abc", "ab", "ac", "a")}
