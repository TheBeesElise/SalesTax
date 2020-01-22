class Tax():
    """an object that associates a label with a tax rate"""
    __slots__ = ['title', '_rate']

    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self._rate = kwargs['_rate']

    def __repr__(self):
        return f"title: {self.title}, rate: {self.rate * 100}%"

    @property
    def rate(self):
        """gets the decimal representation of the tax's rate"""
        return self._rate / 100


class Keyword():
    """an object that associates a word with a collection of applicable taxes"""
    __slots__ = ['word', '_taxes']

    def __init__(self, **kwargs):
        self.word = kwargs['word']
        self._taxes = kwargs['taxes']

    @property
    def total_tax_amount(self):
        """Sums the tax rates from each associated tax item"""
        return sum(tax.rate for tax in self.taxes)

    def __repr__(self):
        tab = '\t'
        return f"\nword: {self.word},\ntaxes:\n{''.join(f'{tab}{repr(tax.obj)}' for tax in self.taxes)}\n"

    @property
    def taxes(self):
        """checks the db for all tax items that this object is associated with"""
        from SalesTax.db import Taxes
        result = []
        for tax in self._taxes:
            result += Taxes.filter(title=tax)
        return result


class Product():
    """an object that stores the quantity, base cost, and possible keywords of a line item"""
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
        from SalesTax.db import Keywords

        keywords = []
        for keyword in self.keywords:
            keywords += Keywords.filter(word=keyword)
        taxes = {}
        for keyword in keywords:
            for tax in keyword.obj.taxes:
                taxes[tax.title] = tax.rate
        return round(self.base_cost * sum(taxes[tax] for tax in taxes))

    @property
    def unit_cost(self):
        """the cost of a single unit from the line item, including tax"""
        return self.base_cost + self.tax

    @property
    def cost(self):
        """the total cost of a line item"""
        def to_nearest_5(val):
            return 5 * round(val / 5)

        return self.count * to_nearest_5(self.base_cost + self.tax)
