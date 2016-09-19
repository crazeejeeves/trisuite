import unittest
import os
import sys

import framework
from framework.config import CommandLineConfiguration as Configuration
from framework.filters import FilterSystem
from framework.controller import TestController

# TODO: Remove this or replace with a check to enforce a consistent working folder
# Workaround to force the working folder to default to the location of the script
# file. Specific for the current
os.chdir(sys.path[0])

framework.init_logging()

config = Configuration()
filters = FilterSystem(config)

controller = TestController(config, filters)
controller.setup()

for i, suite in enumerate(controller.get_suites()):
    unittest.TextTestRunner(verbosity=2).run(suite)



