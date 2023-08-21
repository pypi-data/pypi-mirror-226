
class Emp(object):

    def __init__(self, name):
        self.name = name


class ComparableEmp(object):
    def __init__(self, name):
        self.name = name

    # def __hash__(self):
    #     return hash(self.name)

    def __eq__(self, other):
        # Will called when == use to compare
        return self.__class__ == other.__class__ and self.name == other.name

    def __ne__(self, other):
        #print 'Will called while != to compare'
        return self.__class__ != other.__class__ or self.name != other.name


if __name__ == '__main__':
    e1 = Emp("Aman")
    e2 = Emp("Aman")

    print e1 == e2  # False

    e3 = ComparableEmp("Aman")
    e4 = ComparableEmp("Aman")
    print e3 == e4 # True
    print e3 != e4 # false
    print e3 is e4 # False, compare object identity not contents
    print e3 == e1  # False even object have same contents because we use one more condition self.__class__ == other.__class__

s = (e1, e2, [])
print s

l = list()
"""
Why list cannot be added as key in dict:
Only hashable can be added as a key
Since a list is mutable, if you modify it you would modify its hash too,
which ruins the point of having a hash (like in a set or a dict key).


d = {
    e1: "e1",
    []: ""  # Error unhashable type 'list'
}
"""
