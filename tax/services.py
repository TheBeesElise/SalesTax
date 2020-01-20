from .models import Product


def process_line(input_string):
    data = input_string.split(' ')
    count, keywords, base_cost = int(data[0]), data[1:-2], int(data[-1].replace('.', ''))
    return Product(count, keywords, base_cost)

# def report