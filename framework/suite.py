import unittest


class FilterableTestSuite(unittest.TestSuite):

    def __init__(self, tests=()):
        super().__init__(tests)

    def addTest(self, test):
        if isinstance(test, unittest.TestCase):
            test_methods = [func for func in dir(test) if callable(getattr(test, func)) and func.startswith("test_")]
            for method_name in test_methods:
                method = getattr(test, method_name)
                tags = getattr(method, 'tags', None)
                print(type(test), tags)

        super().addTest(test)


    def run(self, result, debug=False):
        super().run(result, debug)
