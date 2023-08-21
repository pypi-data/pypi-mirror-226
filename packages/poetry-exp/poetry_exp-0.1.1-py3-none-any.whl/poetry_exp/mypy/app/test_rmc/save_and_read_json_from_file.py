import json

def save_json(json_dict, file_path='vvol_snap_config.json'):
    with open(file_path, 'w') as f:
        json.dump(json_dict, f)
        print('Save json obj to file')

def read_json(file_path='vvol_snap_config.json'):
    with open(file_path) as f:
        return json.load(f)

if __name__ == '__main__':
    details = {"ab": {"a":1, "b":2}}
    save_json(details)

    print(type(read_json()))