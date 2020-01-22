from SalesTax.db import *
from os import walk, remove
from filecmp import cmp as compare
from re import search
import unittest
from SalesTax.tax.services import *

TEST_DIR = '/Users/ryanchilds/Practice/CodeClub/SalesTax/tests'


def find_test_files(file_list):
    """finds the files containing line items to test from a list of files"""
    pattern = r'(test[0-9]).txt'
    return [file for file in file_list if search(pattern, file)]


def find_out_files(file_list):
    """searches a list of file paths to identify and return output files"""
    return [file for file in file_list if search(r'out', file)]


def find_expected_files(file_list):
    """searches a list of file paths to identify and return expected output files"""
    return [file for file in file_list if search(r'expected', file)]


class FileTests(unittest.TestCase):
    def test_files(self):
        _, _, files = next(walk(TEST_DIR))
        files = [TEST_DIR + f'/{file}' for file in files]
        input_files = find_test_files(files)
        actuals = []
        for filepath in input_files:
            try:
                actuals.append(write_receipt(read_receipt(filepath), filepath))
            except ValueError:
                self.assertTrue(True)

        expecteds = find_expected_files(files)
        for index in range(len(actuals)):
            if index == 4:
                with self.assertRaises(TypeError):
                    self.assertFalse(compare(actuals[index], expecteds[index]))
            else:
                self.assertTrue(compare(actuals[index], expecteds[index]))
        for file in actuals:
            remove(file)


class TerminalTests(unittest.TestCase):
    def test_from_user(self):
        pass
