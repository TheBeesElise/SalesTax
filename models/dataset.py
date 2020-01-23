from pydoc import locate

from SalesTax.services.dataset import get_class_name


class DataSet:
    """Stores and handles the searching of a collection of data objects"""
    class DataObj:
        """Wraps a class object and associates it with a pk for indexing in a DataSet"""
        __slots__ = ['pk', 'obj']

        def __init__(self, obj, pk):
            self.pk = pk
            self.obj = obj

        def __setattr__(self, key, value):
            if key in self.__slots__:
                object.__setattr__(self, key, value)
            else:
                object.__setattr__(self.obj, key, value)

        def __getattr__(self, key):
            if key in self.__slots__:
                return object.__getattribute__(self, key) or None
            else:
                return getattr(self.obj, key)

        def __str__(self):
            return f'{self.pk}) {self.obj}'

        def __repr__(self):
            return str(self)

        def __gt__(self, other):
            return self.pk > other.pk

        def __lt__(self, other):
            return self.pk < other.pk

    __slots__ = ['cls', 'dset', 'pk_gen']

    def __init__(self, obj_cls_str):

        self.cls = locate(obj_cls_str)
        self.dset = set()
        self.pk_gen = self.next_pk()

    def next_pk(self):
        """Generates the next logical pk based on the current contents of the DataSet"""
        pk = 0
        while True:
            while pk in [obj.pk for obj in self.dset]:
                pk += 1
            yield pk

    def __str__(self):
        return '\n'.join(str(dobj) for dobj in sorted(self.dset))

    def __repr__(self):
        return str(self)

    def create(self, pk=None, **kwargs):
        """Adds a new DataObj to a DataSet. To use, pass each attribute and its desired value as kwargs"""
        pk = pk or next(self.pk_gen)
        obj = self.cls(**kwargs)
        dobj = self.DataObj(obj, pk)
        self.dset.add(dobj)

    def delete(self, pk):
        """Removes an entry from the DataSet"""
        for obj in self.dset:
            if obj.pk == pk:
                self.dset.remove(obj)

    def serialize(self):
        """Generates a JSON-compatible dictionary based on the contents of a DataSet"""
        cls_name = get_class_name(self.cls)
        return {
            cls_name: {
                dobj.pk: {
                    key: value for item in self.dset for key, value in vars(item.obj)
                } for dobj in self.dset}
        }

    def all(self):
        """gets a list of all elements in the DataSet"""
        return [dobj for dobj in self.dset]


    def filter(self, **kwargs):
        """Finds all elements in a DataSet that match a given kwarg condition"""
        out = []
        for dobj in self.dset:
            if all(getattr(dobj, key) == value for key, value in kwargs.items()):
                out.append(dobj)
        return out
