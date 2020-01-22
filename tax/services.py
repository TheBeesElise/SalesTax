from sys import stdout

from SalesTax.tax.models import Product


def read_line(input_string):
    """takes a line item string and turns it into a Product object"""
    data = input_string.split(' ')
    count, keywords, base_cost = int(data[0]), data[1:-2], int(data[-1].replace('.', ''))
    return Product(count, keywords, base_cost)


def read_receipt(filepath):
    """reads line items from a given file"""
    line_items = []
    with open(filepath, 'r') as ifile:
        lines = ifile.readlines()
    for line in lines:
        item = read_line(line)
        line_items.append(item)
    return line_items


def write_receipt(data_list, filepath):
    """writes a receipt of a given list of Products to a file at the given path"""
    outstring = ''
    for item in data_list:
        outstring += f"{item.count} {' '.join(item.keywords)}: {as_usd(item.cost)}\n"
    total, total_tax = sum(item.cost for item in data_list), sum(item.count * item.tax for item in data_list)
    outstring += f"Sales Taxes: {as_usd(total_tax)}\nTotal: {as_usd(total)}\n"
    stdout.write(outstring)
    opath = filepath.split('.')[0] + '_out.txt'
    with open(opath, 'w') as ofile:
        ofile.write(outstring)
    return opath


def as_usd(val):
    """converts the integer price of an number to USD"""
    return f'${(val / 100):.2f}'
