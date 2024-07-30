"""Lab 6: Recursion

=== CSC148 Summer 2023 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains a few nested list functions for you to practice recursion.
"""
from typing import Union


def add_n(obj: Union[int, list], n: int) -> Union[int, list]:
    """Return a new nested list where <n> is added to every item in <obj>.

    >>> add_n(10, 3)
    13
    >>> add_n([1, 2, [1, 2], 4], 10)
    [11, 12, [11, 12], 14]
    """
    if isinstance(obj, int):
        return obj + n
    else:
        new_list = []
        for sublist in obj:
            new_list.append(add_n(sublist, n))
        return new_list


def nested_list_equal(obj1: Union[int, list], obj2: Union[int, list]) -> bool:
    """Return whether two nested lists are equal, i.e., have the same value.

    Note: order matters.

    >>> nested_list_equal(17, [1, 2, 3])
    False
    >>> nested_list_equal([1, 2, [1, 2], 4], [1, 2, [1, 2], 4])
    True
    >>> nested_list_equal([1, 2, [1, 2], 4], [4, 2, [2, 1], 3])
    False
    >>> nested_list_equal([1, 2, [1, 2]], [4, 2, [2, 1], 3])
    False
    >>> nested_list_equal([1, 2, [1, 2]], [])
    False
    >>> nested_list_equal([], [])
    True
    """
    # HINT: You'll need to modify the basic pattern to loop over indexes,
    # so that you can iterate through both obj1 and obj2 in parallel.

    if isinstance(obj1, int) and isinstance(obj2, int):
        return obj1 == obj2
    elif (isinstance(obj1, int) and isinstance(obj2, list)) or \
            (isinstance(obj1, list) and isinstance(obj2, int)):
        return False
    else:
        if len(obj1) != len(obj2):
            return False
        for i in range(len(obj1)):
            if not nested_list_equal(obj1[i], obj2[i]):
                return False
    return True


def duplicate(obj: Union[int, list]) -> Union[int, list]:
    """Return a new nested list with all numbers in <obj> duplicated.

    Each integer in <obj> should appear twice *consecutively* in the
    output nested list. The nesting structure is the same as the input,
    only with some new numbers added. See doctest examples for details.

    If <obj> is an int, return a list containing two copies of it.

    >>> duplicate(1)
    [1, 1]
    >>> duplicate([])
    []
    >>> duplicate([1, 2])
    [1, 1, 2, 2]
    >>> duplicate([1, [2, 3]])  # NOT [1, 1, [2, 2, 3, 3], [2, 2, 3, 3]]
    [1, 1, [2, 2, 3, 3]]
    """
    # HINT: in the recursive case, you'll need to distinguish between
    # when each <sublist> is an int vs. a list
    # (put an isinstance check inside the loop).

    if isinstance(obj, int):
        new_list = []
        new_list.append(obj)
        new_list.append(obj)
        return new_list
    else:
        new_list = []
        for i in obj:
            if isinstance(i, int):
                new_list.append(i)
                new_list.append(i)
            if isinstance(i, list):
                new_list.append(duplicate(i))
        return new_list


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all()
