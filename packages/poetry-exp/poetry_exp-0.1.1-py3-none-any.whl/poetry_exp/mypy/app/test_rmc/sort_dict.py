import time
from collections import OrderedDict
cache = {
  "ds": {
        "2": {
          'name': 'd2',
          'id': 2
        },
        "1": {
          'name': 'd1',
          'id': 1
        },
        "3": {
          'name': 'd3',
          'id': 3
        }
  }
}

cache2 = []
for i in range(10000, 0, -1):
    cache2.append({"name": "ds"+str(i), "id": i})

def sort_list_by_dict_key(dict_list, key):
    """
    In-place sort the list containing the dict objects by a given key
    :param dict_list: list containing the dict objects
    :param key: Name of the key by which the list has to be sorted
    """
    try:
        dict_list.sort(key=lambda d: d[key])
    except Exception as e:
        print('Failed to sort objects, error: {0}'.format(e))


def sort_dict(d, key):
    objects = sorted(d.items(), key=lambda d: d[1][key])
    d.clear()
    for key, value in objects:
        d[key] = value



if __name__ == '__main__':
    #sort_dict(cache2['ds'], 'name')
    print(cache2)
    t1 = time.time()
    sort_list_by_dict_key(cache2, 'name')
    t2 = time.time()
    print('sorting time {0}'.format(t2-t1))
    print(cache2)
