import unittest

from src.utilities import compute_percentage_color


class TestPercentColor(unittest.TestCase):
    def test_percent_green(self):
        string = compute_percentage_color(1)
        self.assertIn('[#70f97E]', string)
        self.assertIn('[/]', string)

    def test_percent_yellow(self):
        string = compute_percentage_color(80)
        self.assertIn('[#F9F070]', string)
        self.assertIn('[/]', string)

    def test_percent_red(self):
        string = compute_percentage_color(95)
        self.assertIn('[#F76A5D]', string)
        self.assertIn('[/]', string)

    def test_too_low(self):
        string = compute_percentage_color(-100)
        self.assertIn('[#70f97E]', string)
        self.assertIn('[/]', string)

    def test_too_high(self):
        string = compute_percentage_color(200)
        self.assertIn('[#F76A5D]', string)
        self.assertIn('[/]', string)


if __name__ == '__main__':
    unittest.main()
