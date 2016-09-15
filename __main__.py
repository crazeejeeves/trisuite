import unittest

from framework.config import SuiteConfig
from framework.controller import SuiteController

config = SuiteConfig()
config.parse()

controller = SuiteController()
for suite in controller.get_suites():
    unittest.TextTestRunner(verbosity=2).run(suite)


