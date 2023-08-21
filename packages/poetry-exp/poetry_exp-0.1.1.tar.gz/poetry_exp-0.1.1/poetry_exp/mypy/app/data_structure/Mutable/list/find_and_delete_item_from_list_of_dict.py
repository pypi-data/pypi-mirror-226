

# in place delete
def delete_item(list_of_dicts, item_key, item_value):
    for i in range(len(list_of_dicts)):
        if list_of_dicts[i].get(item_key) == item_value:
            del list_of_dicts[i]
            break
    else:
        print("Item for key: '{0}' with value: '{1}' not found".format(item_key, item_value))


if __name__ == '__main__':
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
    delete_item(new_list1, 'id', 3) # [{'id': 1, 'name': 'AAA'}, {'id': 5, 'name': 'D'}]
    print(new_list1)

    # -ve case
    delete_item(new_list1, 'id1', 3)
    delete_item(new_list1, 'id', 2)
