import unittest

from src.utilities import bytes2human


class TestBytes(unittest.TestCase):
    def test_documentation_examples(self):
        first_val = bytes2human(10_000)
        second_val = bytes2human(100_001_221)
        self.assertEqual(first_val, '9.8 KiB')
        self.assertEqual(second_val, '95.4 MiB')

    def test_bytes_only(self):
        val = bytes2human(100)
        self.assertEqual(val, '100.0 B')

    def test_neg_bytes(self):
        val = bytes2human(-1)
        self.assertEqual(val, "0.0 B")

    def test_KB(self):
        val = bytes2human(1_024)
        self.assertEqual(val, "1.0 KiB")

    def test_MB(self):
        val = bytes2human(1_048_576)
        self.assertEqual(val, "1.0 MiB")

    def test_GB(self):
        val = bytes2human(1_073_741_824)
        self.assertEqual(val, "1.0 GiB")

    def test_TB(self):
        val = bytes2human(1_099_511_627_776)
        self.assertEqual(val, "1.0 TiB")

    def test_PB(self):
        val = bytes2human(1_125_899_906_842_624)
        self.assertEqual(val, "1.0 PiB")

    def test_EB(self):
        val = bytes2human(1_152_921_504_606_846_976)
        self.assertEqual(val, "1.0 EiB")

    def test_ZB(self):
        val = bytes2human(1_180_591_620_717_411_303_424)
        self.assertEqual(val, "1.0 ZiB")

    def test_YB(self):
        val = bytes2human(1_208_925_819_614_629_174_706_176)
        self.assertEqual(val, "1.0 YiB")


if __name__ == '__main__':
    unittest.main()
