import unittest

from src.utilities import bytes2human


class TestBytes(unittest.TestCase):
    def test_documentation_examples(self):
        first_val = bytes2human(10_000)
        second_val = bytes2human(100_001_221)
        self.assertEqual(first_val, '9.8 KB')
        self.assertEqual(second_val, '95.4 MB')

    def test_bytes_only(self):
        val = bytes2human(100)
        self.assertEqual(val, '100.0 B')

    def test_neg_bytes(self):
        val = bytes2human(-1)
        self.assertEqual(val, "0.0 B")

    def test_KB(self):
        val = bytes2human(1_024)
        self.assertEqual(val, "1.0 KB")

    def test_MB(self):
        val = bytes2human(1_048_576)
        self.assertEqual(val, "1.0 MB")

    def test_GB(self):
        val = bytes2human(1_073_741_824)
        self.assertEqual(val, "1.0 GB")

    def test_TB(self):
        val = bytes2human(1_099_511_627_776)
        self.assertEqual(val, "1.0 TB")

    def test_PB(self):
        val = bytes2human(1_125_899_906_842_624)
        self.assertEqual(val, "1.0 PB")

    def test_EB(self):
        val = bytes2human(1_152_921_504_606_846_976)
        self.assertEqual(val, "1.0 EB")

    def test_ZB(self):
        val = bytes2human(1_180_591_620_717_411_303_424)
        self.assertEqual(val, "1.0 ZB")

    def test_YB(self):
        val = bytes2human(1_208_925_819_614_629_174_706_176)
        self.assertEqual(val, "1.0 YB")


if __name__ == '__main__':
    unittest.main()
