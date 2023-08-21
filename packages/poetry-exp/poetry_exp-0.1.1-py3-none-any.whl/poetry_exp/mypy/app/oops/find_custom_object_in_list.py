"""
list.sort(key=lambda x: x.prop)
The key parameter is used to identify the items to sort the objects on

"""


class Emp(object):

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    # def __hash__(self):   # to work is operator
    #     return hash(self.name)

    def __eq__(self, other):
        # Will called when == use to compare
        return self.__class__ == other.__class__ and self.name == other.name

    def __ne__(self, other):
        #print 'Will called while != to compare'
        return self.__class__ != other.__class__ or self.name != other.name

    def __str__(self):
        return "Name: {0}, Salary: {1}".format(self.name, self.salary)


def display_list(items):
    for items in items:
        print items


if __name__ == '__main__':
    e1 = Emp("Ajay", 10)
    e2 = Emp("Aafak", 5)
    e3 = Emp("Chandan", 2)
    l1 = [e1, e2, e3]

    e4 = Emp("Ajay", 10)

    print e4 == e1  # True
    print e4 in l1  # True
    print l1.index(e4)  # 0

