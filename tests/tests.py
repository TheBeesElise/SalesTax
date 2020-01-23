from os import walk
from filecmp import cmp as compare
from re import search
import unittest

from SalesTax.services.json import write_receipt, read_receipt

TEST_DIR = '/Users/ryanchilds/Practice/CodeClub/SalesTax/tests/files'


class FileTests(unittest.TestCase):
    def test_files(self):
        files = {}
        for directory in ['input', 'expected']:
            _, _, filenames = next(walk(f'{TEST_DIR}/{directory}'))
            files[directory] = [f'{TEST_DIR}/{directory}/{file}' for file in filenames if search(r'([0-9])', file)]
        actuals = []
        files['output'] = []
        for index, filepath in enumerate(files['input']):
            files['output'].append(write_receipt(read_receipt(filepath), filepath.replace('input', 'output')))
            self.assertTrue(compare(files['output'][index], files['expected'][index]))


class ServiceTests(unittest.TestCase):
    def test_bad_line_items(self):
        from SalesTax.services.product import read_line

        def read_receipt_test(filepath):
            exceptions = []
            with open(filepath, 'r') as ifile:
                lines = ifile.readlines()
            for line in lines:
                try:
                    item = read_line(line.strip('\n'))
                except Exception as e:
                    print(e.args[0])
                    exceptions.append(e)
            return exceptions

        receipt = read_receipt_test(f'{TEST_DIR}/input/test_bad_line_items.txt')
        for error in receipt:
            self.assertIsInstance(error, ValueError)


class TestDataSet(unittest.TestCase):
    pass
