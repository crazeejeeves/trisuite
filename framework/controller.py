import logging
import os
import unittest

from framework.config import BaseConfiguration
from framework.suite import FilterableTestSuite


class TestController:
    """Controls top-level suite processing and filtering
    """

    _SUITE_FOLDER_SUFFIX = '_tests'
    _TESTCASE_PATTERN = 'test_*.py'

    def __init__(self, config: BaseConfiguration):
        self._logger = logging.getLogger(__name__)

        self._config = config
        self._suites = []
        self._build_suites()

    def _build_suites(self):
        requested_suites = self._config.get_suites()
        data_sources = [(item[:-6], item) for item in os.listdir()
                        if os.path.isdir(item) and item.endswith(self._config.SUITE_FOLDER_SUFFIX)]

        # Inject test loader to use our custom suite class that processes the tags
        # The suite instances are created by the loader and prevents us from injecting
        # the configuration hence we inject the global config via the class itself
        FilterableTestSuite.set_config(self._config)
        unittest.TestLoader.suiteClass = FilterableTestSuite

        for name, folder in data_sources:
            if name in requested_suites:
                suite = unittest.TestLoader().discover(folder, pattern=self._config.TESTCASE_PATTERN)
                self._suites.append(suite)

    def get_suites(self):
        for suite in self._suites:
            yield suite
