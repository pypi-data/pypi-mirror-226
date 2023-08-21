

if __name__ == '__main__':
    import copy
    l = [
        {
            "name": 'rice',
            "price": 90
        },
        {
            "name": 'tea',
            "price": 10
        },
        {
            "name": 'ice',
            "price": 10
        },
        {
            "name": 'sugar',
            "price": 60
        }
    ]
    l2 = copy.copy(l)
    l3 = copy.deepcopy(l)
    l.sort(key=lambda d: d['price'])
    print (l)
    print (l2)
    """
    [{'price': 10, 'name': 'tea'}, {'price': 10, 'name': 'ice'}, {'price': 60, 'name': 'sugar'}, {'price': 90, 'name': 'rice'}]

    [{'price': 90, 'name': 'rice'}, {'price': 10, 'name': 'tea'}, {'price': 10, 'name': 'ice'}, {'price': 60, 'name': 'sugar'}]

    """
    l2.sort(key=lambda d: (d['price'], d['name']))
    print l2
    """
    [{'price': 10, 'name': 'ice'}, {'price': 10, 'name': 'tea'}, {'price': 60, 'name': 'sugar'}, {'price': 90, 'name': 'rice'}]

    """

    l[0]['price'] = 10000 # because of shallow copy will change in both list l, l2 but not l3

    print l
    print l2
    print l3

    """
    [{'price': 10000, 'name': 'tea'}, {'price': 10, 'name': 'ice'}, {'price': 60, 'name': 'sugar'}, {'price': 90, 'name': 'rice'}]
    [{'price': 10, 'name': 'ice'}, {'price': 10000, 'name': 'tea'}, {'price': 60, 'name': 'sugar'}, {'price': 90, 'name': 'rice'}]
    
    [{'price': 90, 'name': 'rice'}, {'price': 10, 'name': 'tea'}, {'price': 10, 'name': 'ice'}, {'price': 60, 'name': 'sugar'}]

    """

"""

or use following
>>> from operator import itemgetter
>>> mylist=[{"name":"a", "age":2}]
>>> mylist = sorted(mylist, key=itemgetter('name', 'age'))
>>>

"""