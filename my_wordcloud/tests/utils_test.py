from .. import utils


def test_flatten():
    l = [[1, 2], [3, 4], [5, 6]]
    assert utils.flatten(l) == [1, 2, 3, 4, 5, 6]


def test_strip_list():
    l = ["stop", "other", "strings", "another_stop", "stop"]
    stripped = utils.strip_list(l, ["stop", "another_stop"])
    assert stripped == ["other", "strings"]


def test_split_by():
    split = utils.split_by("first part and other part", ["and", "or"])
    assert split == ["first part", "other part"]
    split = utils.split_by("first part other part", ["and", "or"])
    assert split == ["first part other part"]
