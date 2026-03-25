import unittest

from src.utilities import compute_percentage_color


class TestPercentColor(unittest.TestCase):
    def test_percent_green(self):
        _, color = compute_percentage_color(1)
        self.assertEqual(color, "green")

    def test_percent_yellow(self):
        _, color = compute_percentage_color(80)
        self.assertEqual(color, "yellow")

    def test_percent_red(self):
        _, color = compute_percentage_color(95)
        self.assertEqual(color, "red")

    def test_too_low(self):
        _, color = compute_percentage_color(-100)
        self.assertEqual(color, "green")

    def test_too_high(self):
        _, color = compute_percentage_color(200)
        self.assertEqual(color, "red")

if __name__ == '__main__':
    unittest.main()
