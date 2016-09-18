import unittest

import framework
from framework.config import CommandLineConfiguration as Configuration
from framework.filters import FilterSystem
from framework.controller import TestController

#import xmlrunner

framework.init_logging()

config = Configuration()
filters = FilterSystem(config)

controller = TestController(config, filters)
controller.setup()

for i, suite in enumerate(controller.get_suites()):
    unittest.TextTestRunner(verbosity=2).run(suite)
    #report_name = 'test-reports/results-{}.xml'.format(i)
    #with open(report_name, 'wb') as output:
    #    xmlrunner.XMLTestRunner(output=output, verbosity=10).run(suite)



