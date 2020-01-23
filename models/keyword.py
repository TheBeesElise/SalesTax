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
        from SalesTax.database.db import Taxes
        result = []
        for tax in self._taxes:
            result += Taxes.filter(title=tax)
        return result
