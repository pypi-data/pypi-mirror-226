"""
Lightweight Kit Jumpstart
"""

from lkj.filesys import get_app_data_dir, get_watermarked_dir


def add_as_attribute_of(obj, name=None):
    """Decorator that adds a function as an attribute of a container object ``obj``.

    If no ``name`` is given, the ``__name__`` of the function will be used, with a
    leading underscore removed. This is useful for adding helper functions to main
    "container" functions without polluting the namespace of the module, at least
    from the point of view of imports and tab completion.

    >>> def foo():
    ...    pass
    >>>
    >>> @add_as_attribute_of(foo)
    ... def helper():
    ...    pass
    >>> hasattr(foo, 'helper')
    True
    >>> callable(foo.helper)
    True

    In reality, any object that has a ``__name__`` can be added to the attribute of
    ``obj``, but the intention is to add helper functions to main "container" functions.

    Note that if the name of the function starts with an underscore, it will be removed
    before adding it as an attribute of ``obj``.

    >>> @add_as_attribute_of(foo)
    ... def _helper():
    ...    pass
    >>> hasattr(foo, 'helper')
    True

    This is useful for adding helper functions to main "container" functions without
    polluting the namespace of the module, at least from the point of view of imports
    and tab completion. But if you really want to add a function with a leading
    underscore, you can do so by specifying the name explicitly:

    >>> @add_as_attribute_of(foo, name='_helper')
    ... def _helper():
    ...    pass
    >>> hasattr(foo, '_helper')
    True

    Of course, you can give any name you want to the attribute:

    >>> @add_as_attribute_of(foo, name='bar')
    ... def _helper():
    ...    pass
    >>> hasattr(foo, 'bar')
    True

    :param obj: The object to which the function will be added as an attribute
    :param name: The name of the attribute to add the function to. If not given, the

    """

    def _decorator(f):
        attrname = name or f.__name__
        if not name and attrname.startswith('_'):
            attrname = attrname[1:]  # remove leading underscore
        setattr(obj, attrname, f)
        return f

    return _decorator


def get_caller_package_name(default=None):
    """Return package name of caller

    See: https://github.com/i2mint/i2mint/issues/1#issuecomment-1479416085
    """
    import inspect

    try:
        stack = inspect.stack()
        caller_frame = stack[1][0]
        return inspect.getmodule(caller_frame).__name__.split('.')[0]
    except Exception as error:
        return default
