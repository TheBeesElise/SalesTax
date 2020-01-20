"""
./manage.py run_from_file
"""

from __future__ import absolute_import
from sys import stdout
from django.core.management import BaseCommand

from ...services import process_line


class Command(BaseCommand):
    help = 'Given a collection of filepaths, builds a receipt for each file sends it to <filepath>_out.txt'

    def add_arguments(self, parser):
        parser.add_argument('filepaths', nargs='+', type=str)

    def handle(self, *args, **options):
        filepaths = options['filepaths']
        for filepath in filepaths:
            line_items = []
            outstring = ''
            with open(filepath, 'r') as ifile:
                lines = ifile.readlines()
            for line in lines:
                item = process_line(line)
                line_items.append(item)
                outstring += f"{item.count} {' '.join(item.keywords)}: {as_usd(item.cost)}\n"
            total, total_tax = round(sum(item.cost for item in line_items), 2), \
                               round(sum(item.count * item.tax for item in line_items), 2)
            outstring += f"Sales Taxes: {as_usd(total_tax)}\nTotal: {as_usd(total)}\n"
            stdout.write(outstring)
            with open(filepath.split('.')[0] + '_out.txt', 'w') as ofile:
                ofile.write(outstring)


def as_usd(val):
    return f'{(val / 100):.2f}'
