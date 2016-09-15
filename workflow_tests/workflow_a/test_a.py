from unittest import TestCase

from basic_math.accumulate import add


class TestWorkflowA(TestCase):

    def test_one_param(self):
        self.assertRaises(TypeError, lambda: add(1))

    def test_two_params(self):
        self.assertEquals(3, add(1, 2), "Add result did not produce 3")

    def test_three_params(self):
            self.assertEquals(6, add(1, 2, 3), "Add result did not produce 6")

