

def update_current_list_with_new_list(current_list, new_list):
    ids_to_remove = [item['id'] for item in current_list]
    for new_item in new_list:
        for i, item in enumerate(current_list):
            if item['id'] == new_item['id']:
                print('Item :{0} found, Updating it'.format(new_item['id']))
                current_list[i] = new_item
                ids_to_remove.remove(item['id']) # not to remove this id
                break
        else:
            print('New Item :{0} not found, Adding it'.format(new_item['id']))
            current_list.append(new_item) # appending will not change the index of existing items
            # but removing it will change the index of items

    for item in current_list[::]:
        if item['id'] in ids_to_remove:
            current_list.remove(item)


if __name__ == '__main__':
    current_list1 = [
        {
            "id": 1,
            "name": "A"
        },
        {
            "id": 2,
            "name": "B"
        },
        {
            "id": 3,
            "name": "C"
        },
        {
            "id": 4,
            "name": "D"
        },
    ]

    new_list1 = [
        {
            "id": 1,
            "name": "AAA"
        },
        {
            "id": 3,
            "name": "CCCC"
        },
        {
            "id": 5,
            "name": "D"
        },
    ]
    update_current_list_with_new_list(current_list1, new_list1)
    print(current_list1)  # [{'id': 1, 'name': 'AAA'}, {'id': 3, 'name': 'CCCC'}, {'id': 5, 'name': 'D'}]
