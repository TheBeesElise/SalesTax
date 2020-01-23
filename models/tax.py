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
