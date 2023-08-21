"""
list.sort(key=lambda x: x.prop)
The key parameter is used to identify the items to sort the objects on

"""


class Emp(object):

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    # def __cmp__(self, other):
    #     print 'called...'
    #     return cmp(self.salary, other.salary)

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
    print '..............before sort'
    display_list(l1)
    print '..............after sort by name'
    l1.sort(key=lambda x: x.name)
    display_list(l1)

    print '...............after sort by salary'
    l1.sort(key=lambda x: x.salary)
    display_list(l1)

    print '...............after sort by name and salary'
    e4 = Emp("Aafak", 3)
    l1.append(e4)

    l1.sort(key=lambda x: (x.name, x.salary))
    display_list(l1)

"""
..............before sort
Name: Ajay, Salary: 10
Name: Aafak, Salary: 5
Name: Chandan, Salary: 2
..............after sort by name
Name: Aafak, Salary: 5
Name: Ajay, Salary: 10
Name: Chandan, Salary: 2
...............after sort by salary
Name: Chandan, Salary: 2
Name: Aafak, Salary: 5
Name: Ajay, Salary: 10

...............after sort by name and salary
Name: Aafak, Salary: 3
Name: Aafak, Salary: 5
Name: Ajay, Salary: 10
Name: Chandan, Salary: 2

"""
