import os
import unittest

from framework.suite import FilterableTestSuite


class SuiteController:

    def __init__(self):
        self._suites = []
        self._build_suites()

    def _build_suites(self):
        data_sources = [item for item in os.listdir() if os.path.isdir(item) and item.find('_tests') != -1]

        unittest.TestLoader.suiteClass = FilterableTestSuite

        for source in data_sources:
            suite = unittest.TestLoader().discover(source, pattern='test_*.py')
            self._suites.append(suite)
            # TODO: Remove this after testing
            break

    def get_suites(self):
        for suite in self._suites:
            yield suite
