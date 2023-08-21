"""
__init__: is called immediately Whenever an instance of a class is created. You can
also pass arguments to the class during its initialization.

__getitem__: Implementing getitem in a class allows its instances to use the [] (indexer) operator.
"""


class GetTest(object):
    def __init__(self):
        self.info = {
            'name': 'Yasoob',
            'country': 'Pakistan',
            'number': 12345812
        }

    def __getitem__(self, i):
        return self.info[i]


gt = GetTest()
print gt["name"] # Yasoob