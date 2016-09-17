import unittest

import framework
from framework.config import CommandLineConfiguration as Configuration
from framework.controller import TestController

framework.init_logging()

config = Configuration()

controller = TestController(config)
for suite in controller.get_suites():
    unittest.TextTestRunner(verbosity=2).run(suite)


