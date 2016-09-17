import unittest

import framework
from framework.config import CommandLineConfiguration as Configuration
from framework.controller import SuiteController

framework.init_logging()

config = Configuration()

controller = SuiteController()
for suite in controller.get_suites():
    unittest.TextTestRunner(verbosity=2).run(suite)


