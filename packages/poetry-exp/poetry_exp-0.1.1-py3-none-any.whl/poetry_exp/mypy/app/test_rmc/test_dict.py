snap_config = {}


def add_details(id, details):
    snap_config[id] = details

def get_details(id):
    return snap_config[id]


if __name__ == '__main__':
    details = {"a":1, "b":2}
    details2 = {"c": 3, "d": 4}
    add_details("ab", details)
    print(get_details("ab"))
    add_details("cd", details)
    print(get_details("cd"))

    print(snap_config)
