def filter_nones(dictionaries):
    if not dictionaries:
        return

    keep_keys = set()

    for dict_ in dictionaries:
        for key, value in dict_.items():
            # print(key, value)
            if value is not None:
                keep_keys.add(key)

    all_keys = set(dictionaries[0])
    remove_keys = all_keys - keep_keys

    print(remove_keys)
    for dict_ in dictionaries:
        for key in remove_keys:
            del dict_[key]


if __name__ == '__main__':
    dicts = [
            {'a': 1, 'b': None, 'c': 4},
            {'a': 2, 'b': None, 'c': 3},
            {'a': None, 'b': None, 'c': 3},
    ]
    expected = [
            {'a': 1, 'c': 4},
            {'a': 2, 'c': 3},
            {'a': None, 'c': 3},
    ]

    filter_nones(dicts)
    print (dicts == expected)
