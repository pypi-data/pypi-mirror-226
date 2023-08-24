import pytest

CSV_DATA = """
animal	carnivore	value
dog	TRUE	3
cat	TRUE	55
horse	FALSE	35
cat	TRUE	60
horse	FALSE	9
"""


@pytest.fixture()
def example():
    import io

    import pandas

    buffer = io.StringIO(CSV_DATA.strip())
    return pandas.read_csv(buffer, sep="\t")


def test_selection_select(example):
    from sensospot_tools.selection import select

    result = select(example, "animal", "horse")
    assert list(result["animal"]) == ["horse", "horse"]
    assert list(result["value"]) == [35, 9]


def test_selection_split_one_column(example):
    from sensospot_tools.selection import split

    result = dict(split(example, "carnivore"))

    assert sorted(result.keys()) == [False, True]
    assert list(result[True]["value"]) == [3, 55, 60]
    assert list(result[False]["value"]) == [35, 9]


def test_selection_split_multiple_columns(example):
    from sensospot_tools.selection import split

    result = {
        (key_1, key_2): value
        for key_1, key_2, value in split(example, "carnivore", "animal")
    }

    assert sorted(result.keys()) == [
        (False, "horse"),
        (True, "cat"),
        (True, "dog"),
    ]

    assert list(result[(True, "cat")]["value"]) == [55, 60]
    assert list(result[(True, "dog")]["value"]) == [3]
    assert list(result[(False, "horse")]["value"]) == [35, 9]
