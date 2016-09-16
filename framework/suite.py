import unittest

from framework.tags import ProductTag


def _reason(filters):
    """Generate a parameterized reason message based on the filters that exclude
    a given method
    """
    pass

def _mark_with_skip(func, reason):
    """unittest provides a built-in skip decorator that can be reused for
    disabled test cases that do not match the filter criteria. It is a
    parameterized decorator, so dynamic decoration syntax is convoluted
    """
    return unittest.skip(reason)(func)


class FilterableTestSuite(unittest.TestSuite):
    """ Pre-processes added test methods and filter items that need to be
        excluded based on the user-defined inclusion and/or exclusion rules
    """

    def __init__(self, tests=()):
        super().__init__(tests)

    def addTest(self, test):
        if isinstance(test, unittest.TestCase):
            test_methods = [func for func in dir(test) if callable(getattr(test, func)) and func.startswith("test_")]

            for method_name in test_methods:
                method = getattr(test, method_name)
                tags = getattr(method, 'tags', None)

                if tags is not None:
                    # TEST - Abort insertion of test case
                    if tags.product == ProductTag.BME:
                        print(type(method))
                        setattr(test, method_name, _mark_with_skip(method, "Implicitly disabled"))

                        print(method.__name__) #, tags.product, tags.categories)

        super().addTest(test)

