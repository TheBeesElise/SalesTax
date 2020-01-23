from SalesTax.models.product import Product


def read_line(input_string):
    """takes a line item string and turns it into a Product object"""
    data = input_string.split(' ')
    count, keywords, base_cost = int(data[0]), data[1:-2], int(data[-1].replace('.', ''))
    return Product(count, keywords, base_cost)


def as_usd(val):
    """converts the integer price of an number to USD"""
    return f'${(val / 100):.2f}'
