# from django.test import TestCase
from unittest import TestCase


def sum_ints(a, b):
    return 0


class MySuite(TestCase):
    def test_sum(self):
        self.assertEqual(sum_ints(1, 2), 3)
