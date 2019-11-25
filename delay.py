"""Helpful decorator for separating the decision taking and enforcing rounds."""


class Order:
    """Execute actions when called.
    Orders can be chained by addition.
    """

    def __init__(self, *actions):
        self.actions = actions

    def __add__(self, other):
        return Order(*(self.actions + other.actions))

    def __call__(self):
        for action in self.actions:
            action()


def delay(action):
    """Call returns callable to enforce ordered action.
    >>> @delay
    ... def hello(name):
    ...     print(f"Hello {name}")
    >>> @delay
    ... def bye(name):
    ...     print(f"Bye {name}")
    >>> order = hello("World") + bye("World")
    >>> order()
    Hello World
    Bye World
    """

    def order(*args):
        """Place order and recieve 'reciept'."""
        return Order(lambda: action(*args))

    return order


if __name__ == "__main__":
    import doctest

    doctest.testmod()
