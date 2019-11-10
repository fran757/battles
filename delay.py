"""Helpful decorator for separating the decision taking and enforcing rounds."""


def delay(action):
    """Call returns callable to enforce ordered action.
    >>> @delay
    ... def hello(name):
    ...     print(f"Hello {name}")
    >>> order = hello("World")
    >>> order()
    Hello World
    """

    def order(*args):
        """Place order and recieve 'reciept'."""

        def call():
            """Actually do action."""
            action(*args)

        return call

    return order


if __name__ == "__main__":
    import doctest

    doctest.testmod()
