def apply(fun, *iterables):
    for args in zip(*iterables):
        fun(*args)
