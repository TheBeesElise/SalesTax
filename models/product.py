class Product():
    """an object that stores the quantity, base cost, and possible keywords of a line item"""
    __slots__ = ['keywords', 'count', 'base_cost']

    def __init__(self, count, keywords, base_cost):
        self.keywords = keywords
        self.count = count
        self.base_cost = base_cost

    def __repr__(self):
        return str(self)

    @property
    def tax(self):
        """
        calculates the absolute amount added to the cost by taxes. It does this by checking each keyword for its
        collection of taxes, then testing if each root tax has been applied to prevent double-taxing, then returns
        the total
        Returns
        -------

        """
        from SalesTax.database.db import Keywords

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

    def __str__(self):
        return f'{self.count} {" ".join(self.keywords)}: {self.cost}'