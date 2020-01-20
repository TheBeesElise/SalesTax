import os
from filecmp import cmp as compare
from re import compile

from django.test import TestCase

from SalesTax.tax.management.commands.run_from_file import Command as file_cmd


def find_test_files():
    pattern = compile(r'(test[0-9]).txt')
    return [file for _, _, files in os.walk('.') for file in files if pattern.match(file)]


def find_out_and_expected_files():
    out = compile(r'out')
    expected = compile(r'expected')
    return [file for _, _, files in os.walk('.') for file in files if out.match(file)],\
           [file for _, _, files in os.walk('.') for file in files if expected.match(file)]


class FileTests(TestCase):
    def test_files(self):
        file_cmd.handle(filepaths=find_test_files())

        files = zip(find_out_and_expected_files())
        for index, actual, expected in enumerate(files):
            if index == 4:
                with self.assertRaises(TypeError):
                    self.assertFalse(compare(actual, expected))
            else:
                self.assertTrue(compare(actual, expected))