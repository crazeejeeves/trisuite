import logging
import os
import unittest

from framework.config import BaseConfiguration
from framework.filters import FilterSystem
from framework.suite import FilterableTestSuite


class TestController:
    """Controls top-level suite processing and filtering
    """

    _SUITE_FOLDER_SUFFIX = '_tests'
    _TESTCASE_PATTERN = 'test_*.py'

    def __init__(self, config: BaseConfiguration, filters: FilterSystem):
        self._logger = logging.getLogger(__name__)

        self._config = config
        self._filters = filters
        self._suites = []

    def _build_suites(self):
        requested_suites = self._config.get_suites()
        suffix_len = len(self._config.SUITE_FOLDER_SUFFIX)
        data_sources = [(item[:-suffix_len], item) for item in os.listdir()
                        if os.path.isdir(item) and item.endswith(self._config.SUITE_FOLDER_SUFFIX)]

        self._logger.info('Found {} candidate test folders'.format(len(data_sources)))

        names = [name for name, folder in data_sources]
        self._logger.debug('Suite(s) requested: ' + str(requested_suites))
        self._logger.debug('Folder(s) found: ' + str(names))
        self._logger.warn('Requested suite(s) not found: {}'.format(requested_suites.difference(names)))

        # Inject test loader to use our custom suite class that processes the tags
        # The suite instances are created by the loader and prevents us from injecting
        # the configuration hence we inject the global config via the class itself
        FilterableTestSuite.set_filters(self._filters)
        unittest.TestLoader.suiteClass = FilterableTestSuite

        for name, folder in data_sources:
            if name in requested_suites:
                self._logger.info('Suite "{}" loading from "{}"...'.format(name, folder))
                suite = unittest.TestLoader().discover(folder, pattern=self._config.TESTCASE_PATTERN)
                self._suites.append(suite)
                self._logger.info('Suite "{}" loaded with {} test(s)!'.format(name, suite.countTestCases()))
                continue

            self._logger.info('Suite "{}" skipped'.format(name))

    def setup(self):
        self._build_suites()
        pass

    def get_suites(self):
        for suite in self._suites:
            yield suite
