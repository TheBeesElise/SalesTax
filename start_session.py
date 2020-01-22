from json import loads, dumps


def seed():
    defaults = {
        'Tax':{
            0: {
                "title": 'luxury',
                '_rate': 10
            },
            1: {
                "title": 'import',
                '_rate': 5
            }
        },
        'Keyword': {
            0: {
                'word': 'CD',
                '_taxes': ['luxury']
            },
            1: {
                'word': 'music',
                '_taxes': ['luxury']
            },
            2: {
                'word': 'perfume',
                '_taxes': ['luxury']
            },
            3: {
                'word': 'imported',
                '_taxes': ['import']
            }

        }
    }
    with open("json/data.json", 'r') as data_file:
        data_str = data_file.read()
    if not data_str:
        with open("json/data.json", 'w') as data_file:
            data_file.write(dumps(defaults))
            print("database seeded")
    else:
        print("database exists")


def start_session():
    from SalesTax.dataset import DataSet

    MODEL_SCOPE = 'SalesTax.tax.models.'

    seed()
    with open("/Users/ryanchilds/Practice/CodeClub/SalesTax/json/data.json", 'r') as data_file:
        data_str = data_file.read()
    data_dict = loads(data_str)
    out = {}
    for table in data_dict:
        out[table] = DataSet(MODEL_SCOPE + table)
        for row in data_dict[table]:
            out[table].create(pk=row, **dict(data_dict[table][row].items()))

    return out

