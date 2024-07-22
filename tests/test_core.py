from syml import compute


def test_compute():
    assert compute(["a", "bc", "abc"]) == "abc"
