from __future__ import annotations

from enum import Enum
from typing import Any

import numpy as np
import pytest

from ch5mpy import File, Group
from ch5mpy.write import write_dataset, write_object


class State(Enum):
    RNA = "RNA"


@pytest.mark.parametrize("obj, expected", [(1, 1), ("abc", "abc"), (None, None)])
def test_should_write_simple_attribute(obj, expected, group):
    group.attrs["something"] = obj

    assert "something" in group.attrs.keys()
    assert group.attrs["something"] == expected


def test_should_write_list_attribute(group):
    group.attrs["something"] = [1, 2, 3]

    assert "something" in group.attrs.keys()
    assert np.all(group.attrs["something"] == [1, 2, 3])


def test_should_write_complex_objects_as_strings_in_attributes(group):
    group.attrs["something"] = State.RNA

    assert "something" in group.attrs.keys()
    assert group.attrs["something"] == State.RNA


@pytest.mark.parametrize(
    "array, expected",
    [
        (np.array([1, 2, 3]), [1, 2, 3]),
        ([1, 2, 3], [1, 2, 3]),
        (np.array(["a", "b", "c"]), [b"a", b"b", b"c"]),
    ],
)
def test_should_write_array(group, array, expected):
    write_dataset(group, "something", array)

    assert "something" in group.keys()
    assert np.all(group["something"][()] == expected)


def test_should_write_dict_of_arrays(group):
    write_dataset(group, "some_dict", {"some_a": [1, 2, 3], "some_b": ["a", "b", "c"]})

    assert np.all(group["some_dict"]["some_a"][()] == [1, 2, 3])
    assert np.all(group["some_dict"]["some_b"][()] == [b"a", b"b", b"c"])


def are_equal(obj1: Any, obj2: File | Group) -> bool:
    if isinstance(obj1, (np.ndarray, list)):
        return np.array_equal(obj1, obj2[()])

    return obj1 == obj2


@pytest.mark.parametrize(
    "name, obj",
    [
        ("list_", [1, 2, 3]),
        ("array_", np.array([4, 5, 6])),
        # ('dict_', {'a': 'test', 'b': 1})
    ],
)
def test_write_object(group, name, obj):
    write_object(group, name, obj)

    assert are_equal(obj, group[name])
