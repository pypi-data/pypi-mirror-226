def find_user_by_id(id, user_list):
    return next((user for user in user_list if user['id'] == id), None)

if __name__ == '__main__':
    users = [
        {
            'id': 101,
            'name': 'Aa'
        },
        {
            'id': 100,
            'name': 'Bb'
        },
        {
            'id': 102,
            'name': 'Cc'
        },
        {
            'id': 1,
            'name': 'A'
        },
        {
            'id': 2,
            'name': 'B'
        },
        {
            'id': 3,
            'name': 'C'
        },
        {
            'id': 4,
            'name': 'D'
        },
    ]

    user = find_user_by_id(2, users)
    if user:
        print(user['id'], user['name'])
    user = find_user_by_id(100, users)
    if user:
        print(user['id'], user['name'])
    user = find_user_by_id(1000, users)
    if user:
        print(user['id'], user['name'])