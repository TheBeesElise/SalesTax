class Tax():
    __slots__ = ['title', '_rate']

    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self._rate = kwargs['_rate']

    def __repr__(self):
        return f"title: {self.title}, rate: {self.rate * 100}%"

    @property
    def rate(self):
        return self._rate / 100


class Keyword():
    __slots__ = ['word', '_taxes']

    def __init__(self, **kwargs):
        self.word = kwargs['word']
        self._taxes = kwargs['taxes']

    @property
    def total_tax_amount(self):
        return sum(tax.rate for tax in self.taxes)

    def __repr__(self):
        tab = '\t'
        return f"\nword: {self.word},\ntaxes:\n{''.join(f'{tab}{repr(tax.obj)}' for tax in self.taxes)}\n"

    @property
    def taxes(self):
        from SalesTax.db import Taxes
        result = []
        for tax in self._taxes:
            result += Taxes.find_all(title=tax)
        return result

class Product():
    __slots__ = ['keywords', 'count', 'base_cost']

    def __init__(self, count, keywords, base_cost):
        self.keywords = keywords
        self.count = count
        self.base_cost = base_cost

    def __repr__(self):
        return str(vars(self))

    @property
    def tax(self):
        """
        calculates the absolute amount added to the cost by taxes. It does this by checking each keyword for its
        collection of taxes, then testing if each root tax has been applied to prevent double-taxing, then returns
        the total
        Returns
        -------

        """
        _keywords = [kw for kw in Keyword.objects.filter(word__in=self.keywords)]
        keywords = []
        taxes = []
        for keyword in _keywords:
            tax_types = [t.title for t in keyword.taxes.all()]
            if tax_types not in taxes:
                taxes.append(tax_types)
                keywords.append(keyword)
        return round(self.base_cost * sum(kw.total_tax_amount for kw in keywords))

    @property
    def unit_cost(self):
        return self.base_cost + self.tax

    @property
    def cost(self):
        def to_nearest_5(val):
            return 5 * round(val / 5)

        return self.count * to_nearest_5(self.base_cost + self.tax)
