from sys import stdout

from SalesTax.services.product import read_line, as_usd


def read_receipt(filepath):
    """reads line items from a given file"""
    line_items = []
    with open(filepath, 'r') as ifile:
        lines = ifile.readlines()
    for line in lines:
        try:
            item = read_line(line)
        except Exception as e:
            print(e.args[0])
            raise Exception
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
    with open(filepath, 'w') as ofile:
        ofile.write(outstring)
    return filepath
