from SalesTax.start_session import start_session
start_session()

import os
from filecmp import cmp as compare
from re import search

from django import setup
import unittest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "orm.settings")
setup()

from SalesTax.tax.services import read_receipt, write_receipt

TEST_DIR = '/Users/ryanchilds/Practice/CodeClub/SalesTax/tests'


def find_test_files():
    pattern = r'(test[0-9]).txt'
    return [file for _, _, files in os.walk(TEST_DIR) for file in files if search(pattern, file)]


def parse_list(test_list):
    output = []
    expected = []
    for file in test_list:
        if 'out' in file:
            output.append(file)
        elif 'expected' in file:
            expected.append(file)
        else:
            pass


def find_out_files(file_list):
    return [file for file in file_list if search(r'out', file)]


def find_expected_files(file_list):
    return [file for file in file_list if search(r'expected', file)]


class FileTests(unittest.TestCase):
    def test_files(self):
        _, _, files = next(os.walk(TEST_DIR))
        input_files = find_test_files()
        actuals = []
        for filepath in input_files:
            actuals.append(write_receipt(read_receipt(filepath), filepath))

        expecteds = find_expected_files(files)
        for index in range(len(actuals)):
            if index == 4:
                with self.assertRaises(TypeError):
                    self.assertFalse(compare(actuals[index], expecteds[index]))
            else:
                self.assertTrue(compare(actuals[index], expecteds[index]))
