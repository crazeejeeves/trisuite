import unittest

import framework
from framework.config import CommandLineConfiguration as Configuration
from framework.filters import FilterSystem
from framework.controller import TestController

framework.init_logging()

config = Configuration()
filters = FilterSystem(config)

controller = TestController(config, filters)
controller.setup()

for suite in controller.get_suites():
    unittest.TextTestRunner(verbosity=2).run(suite)


