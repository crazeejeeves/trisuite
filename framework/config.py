import argparse
import logging

from framework.tags import ProductTag


class BaseConfiguration:
    """Base class for defining framework configuration. Provides standard interface to obtain
    all supported, configurable parameters

    Note to inheritors: Ensure the data types are respected when assigning the values to the
    internal variables
    """

    SUITE_FOLDER_SUFFIX = '_tests'
    TESTCASE_PATTERN = 'test_*.py'

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._suites = set()
        self._categories = set()
        self._is_category_excluded = True
        self._priority = -1
        self._product = None
        self._skip_shared = False

    def __repr__(self):
        repr_str = 'suites = {}\ncategories = {}\nis_excluded = {}\npriority = {}\nproduct = {}\nskip_shared = {}'.format(
            self._suites,
            (len(self._categories) > 0) and self._categories or 'unspecified',
            self._is_category_excluded,
            self._priority,
            self._product,
            self._skip_shared
        )
        return repr_str

    @staticmethod
    def _args_to_tuple(param):
        if isinstance(param, str):
            return param,
        elif isinstance(param, list):
            return tuple(param)
        else:
            assert isinstance(param, type(None))
            return ()

    @staticmethod
    def _args_to_set(param):
        if isinstance(param, str):
            return set([param])
        elif isinstance(param, list):
            return set(param)
        else:
            assert isinstance(param, type(None))
            return set()

    def get_suites(self):
        return self._suites

    def get_categories(self):
        return self._categories

    @property
    def is_excluded(self):
        return self._is_category_excluded

    def get_priority(self):
        return self._priority

    def get_product(self):
        if self._product:
            return ProductTag(self._product)
        else:
            return None

    def is_shared_skipped(self):
        return self._skip_shared


class CommandLineConfiguration(BaseConfiguration):
    """Configuration based on command line parameter parsing
    """

    def __init__(self):
        super().__init__()

        self._parser = None
        self._args = None

        if self._configure_parser():
            self._parse()

    def _configure_parser(self):
        if self._parser is not None:
            return

        try:
            self._parser = argparse.ArgumentParser(epilog='Note: --query overrides all other flags and returns without executing tests')
        except AttributeError as e:
            self._logger.exception('Failed to parse command-line arguments')
            self._logger.warn('Using default parameters (unit test only)')
            self._suites = set(['unit'])
            return False
            
        self._parser.add_argument('--suite',
                                  default='unit',
                                  metavar='SuiteName',
                                  nargs='+',
                                  help='Suite(s) to execute')
        self._parser.add_argument('--product',
                                  type=str,
                                  choices=['ACE', 'BME', 'STL'],
                                  help='Filter specific product to test')
        self._parser.add_argument('--skip-shared',
                                  action='store_true',
                                  help='Skips shared functionality tests')
        self._parser.add_argument('--priority',
                                  default=-1,
                                  metavar='PriorityID',
                                  type=int,
                                  help='Lowest priority of test cases to execute (inclusive)')

        category = self._parser.add_mutually_exclusive_group()
        category.add_argument('--include',
                              metavar='category',
                              nargs='+',
                              help='Filter(s) for test case categories to include for execution')
        category.add_argument('--exclude',
                              metavar='category',
                              nargs='+',
                              help='Filter(s) for test case categories to exclude from execution')

        self._parser.add_argument('--query',
                                  type=str,
                                  choices=['suite', 'priority', 'category'],
                                  default='suite',
                                  help='Extract the required meta information from the test collection. NOTIMPLEMENTED'
                                  )
        return True

    def _parse(self):
        self._logger.info('Parsing command-line arguments...')

        self._args = self._parser.parse_args()

        self._suites = self._args_to_set(self._args.suite)
        self._priority = self._args.priority
        self._product = self._args.product
        self._skip_shared = self._args.skip_shared

        if self._args.exclude:
            self._categories = self._args_to_set(self._args.exclude)
            self._is_category_excluded = True
        elif self._args.include:
            self._categories = self._args_to_set(self._args.include)
            self._is_category_excluded = False

        self._logger.info('Parse results:\n\n' + str(self) + '\n')
        self._logger.info('Completed command-line parsing')
