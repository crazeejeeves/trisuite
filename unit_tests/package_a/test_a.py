from unittest import TestCase

from basic_math.accumulate import add
from framework.tags import tag


class TestUnitA(TestCase):

    def test_one_param(self):
        self.assertRaises(TypeError, lambda: add(1))

    @tag("Nightly", priority=10)
    def test_two_params(self):
        self.assertEquals(3, add(1, 2), "Add result did not produce 3")

    @tag("Weekly")
    def test_three_params(self):
            self.assertEquals(6, add(1, 2, 3), "Add result did not produce 6")

