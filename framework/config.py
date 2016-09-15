import argparse


class SuiteConfig:

    def __init__(self):
        self._parser = None
        self._args = None
        self._categories = []
        self._priorities = []

        self._configure_parser()

    def _configure_parser(self):
        if self._parser is not None:
            return

        self._parser = argparse.ArgumentParser(epilog='Note: --query overrides all other flags and returns without executing tests')
        self._parser.add_argument('--suite',
                                  default='unit',
                                  metavar='SuiteName',
                                  nargs='+',
                                  help='Suite(s) to execute')
        self._parser.add_argument('--priority',
                                  metavar='PriorityTag',
                                  type=int,
                                  nargs='+',
                                  help='Priority of test cases to execute')
        self._parser.add_argument('--category',
                                  metavar='CategoryTag',
                                  nargs='+',
                                  help='Additional filter(s) for test cases')
        self._parser.add_argument('--product',
                                  type=str,
                                  choices=['ACE', 'BME', 'STL'],
                                  help='Define the product to test')
        self._parser.add_argument('--skip-shared',
                                  action='store_true',
                                  help='Skips shared functionality tests')

        self._parser.add_argument('--query',
                                  type=str,
                                  choices=['suite', 'priority', 'category'],
                                  default='suite',
                                  help='Extract the required meta information from the test collection'
                                  )

    def _check_parse_state(self):
        if self._args is None:
            raise ValueError("Commandline arguments have not been initialized correctly")

    def _nargs_to_readonly_container(self, input):
        if isinstance(input, str):
            return input,
        elif isinstance(input, list):
            return tuple(input)
        else:
            assert isinstance(input, type(None))
            return None

    def parse(self):
        self._args = self._parser.parse_args()

    def get_suites(self):
        self._check_parse_state()
        return self._nargs_to_readonly_container(self._args.suite)

    def get_categories(self):
        self._check_parse_state()
        return self._nargs_to_readonly_container(self._args.category)

    def get_priorities(self):
        self._check_parse_state()
        return self._nargs_to_readonly_container(self._args.priority)

    def get_product(self):
        self._check_parse_state()
        return self._args.product

    def is_shared_skipped(self):
        self._check_parse_state()
        return self._args.skip_shared
