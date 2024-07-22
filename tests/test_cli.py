import subprocess


def test_main():
    assert subprocess.check_output(["syml", "foo", "foobar"], text=True) == "foobar\n"
