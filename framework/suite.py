import logging
import unittest

from framework.filters import FilterSystem


class FilterableTestSuite(unittest.TestSuite):
    """ Pre-processes added test methods and filter items that need to be
        excluded based on the user-defined inclusion and/or exclusion rules
    """
    _filters = None

    def __init__(self, tests=()):
        self._logger = logging.getLogger(__name__)
        super().__init__(tests)

    @classmethod
    def set_filters(cls, filters: FilterSystem):
        """ Provide the filter system so that all suite instances can access
        the filter rules during test registration
        """
        cls._filters = filters

    def addTest(self, test):
        """ Registers a TestCase in the TestSuite
        Filtration of test functions based on the configuration is done here by marking the
        excluded test cases for skipping. All excluded tests will explicitly log their skip
        status in the test report

        :param test: Test case containing tests to be pre-processed for queuing
        :type: unittest.TestCase (or derivative)
        :return:
        """
        assert FilterableTestSuite._filters, 'Filter system not configured'

        if isinstance(test, unittest.TestCase):
            test_methods = [func for func in dir(test) if callable(getattr(test, func)) and func.startswith("test_")]

            for method_name in test_methods:
                method = getattr(test, method_name)
                tags = getattr(method, 'tags', None)

                if self._filters.filter_by_product(test, method, tags):
                    continue

                if self._filters.filter_by_priority(test, method, tags):
                    continue

                if self._filters.filter_by_blacklist(test, method, tags):
                    continue

                if self._filters.filter_by_whitelist(test, method, tags):
                    continue

        super().addTest(test)
