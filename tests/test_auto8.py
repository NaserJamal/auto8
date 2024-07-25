import unittest
from auto8 import main

class TestAuto8(unittest.TestCase):
    def test_parse_flake8_output(self):
        sample_output = "test_file.py:30:80: E501 line too long (104 > 79 chara\
cters)"
        issues = main.parse_flake8_output(sample_output)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['file_path'], 'test_file.py')
        self.assertEqual(issues[0]['line_num'], 30)
        self.assertEqual(issues[0]['col_num'], 80)
        self.assertEqual(issues[0]['error_code'], 'E501')

if __name__ == '__main__':
    unittest.main()