import unittest
import functools
from framework.tags import ProductTag


def skip_decorator(test_item, reason):
    if not isinstance(test_item, type):
        @functools.wraps(test_item)
        def skip_wrapper(*args, **kwargs):
            raise SkipTest(reason)

        test_item = skip_wrapper

    test_item.__unittest_skip__ = True
    test_item.__unittest_skip_why__ = reason
    return test_item


class FilterableTestSuite(unittest.TestSuite):

    def __init__(self, tests=()):
        super().__init__(tests)

    def addTest(self, test):
        if isinstance(test, unittest.TestCase):
            test_methods = [func for func in dir(test) if callable(getattr(test, func)) and func.startswith("test_")]
            for method_name in test_methods:
                method = getattr(test, method_name)
                tags = getattr(method, 'tags', None)
                if tags is not None:
                    # Abort insertion of test case
                    if tags.product == ProductTag.BME:
                        #setattr(method, '__unittest_skip__', True)
                        #setattr(method, '__unittest_skip_why__', 'Disabled by filters')
                        print(type(method))
                        setattr(test, method_name, skip_decorator(method, "Implicitly disabled"))


                        print(method.__name__) #, tags.product, tags.categories)

        super().addTest(test)


    def run(self, result, debug=False):
        super().run(result, debug)
