def add_on(lst: list[tuple], new) -> None:
    """Add new to the end of each tuple in lst.
    >>> things = [(), (1, 2), (1,)]
    >>> add_on(things, 99)
    >>> things
    [(99,), (1, 2, 99), (1, 99)]
    >>> things = []
    >>> add_on(things, 99)
    >>> things
    []
    >>> things = [(), (), ()]
    >>> add_on(things, 99)
    >>> things
    [(99,), (99,), (99,)]
    """
    for item in lst:
        item = item + (new,)
        print(item)

add_on([(3,4,), (1, 2), (1,)],99)
