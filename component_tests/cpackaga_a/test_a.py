from unittest import TestCase

from ddt import *

from basic_math.accumulate import add
from framework.tags import tag, ProductTag


@ddt
class TestComponentA(TestCase):

    def test_one_param(self):
        self.assertRaises(TypeError, lambda: add(1))

    @tag("Nightly", "Long-running", priority=1)
    def test_two_params(self):
        self.assertEquals(3, add(1, 2), "Add result did not produce 3")

    @tag("Nightly", priority=1, product=ProductTag.BME)
    def test_three_params(self):
            self.assertEquals(6, add(1, 2, 3), "Add result did not produce 6")

    @tag("Nightly", priority=1, product=ProductTag.BME)
    @data(
        (1, 2, 3, 6),
        (2, 4, 6, 12),
    )
    @unpack
    def test_parameterized_params(self, a, b, c, result):
        self.assertEquals(result, add(a, b, c), "Add result did not produce {}".format(result))

