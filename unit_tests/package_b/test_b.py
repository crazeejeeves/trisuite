from unittest import TestCase

from basic_math.accumulate import add
from framework.tags import tag, ProductTag


class TestUnitB(TestCase):

    def test_one_negative_param(self):
        self.assertRaises(TypeError, lambda: add(-1))

    @tag("Nightly", product=ProductTag.BME)
    def test_two_negative_params(self):
        self.assertEquals(-3, add(-1, -2), "Add result did not produce -3")

    @tag("Weekly", product=ProductTag.ACE)
    def test_three_params(self):
            self.assertEquals(-6, add(-1, -2, -3), "Add result did not produce -6")

