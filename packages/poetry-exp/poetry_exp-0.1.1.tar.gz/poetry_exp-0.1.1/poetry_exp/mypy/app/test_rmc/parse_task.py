import json


def get_task_error(task):
    if task['taskStatus'] == 'Error' or task['taskState'] == 'Failed':
        return task['taskErrors']

    if task.get('subTasks'):
        for sub_task in task.get('subTasks')['tasks']:
            errors = get_task_error(sub_task)
            if errors:
                return errors

def get_error_details(task_response):
    if task_response.get('task'):
        return get_task_error(task_response.get('task'))


if __name__ == '__main__':
    with open('task_response.json') as f:
        task_response = json.load(f)
        errors = get_error_details(task_response)
        print errors

    with open('task_response_with_no_error.json') as f:
        task_response = json.load(f)
        errors = get_error_details(task_response)
        print errors

    with open('task_response_sub_task_error.json') as f:
        task_response = json.load(f)
        errors = get_error_details(task_response)
        print errors

    with open('task_response_big_with_error.json') as f:
        task_response = json.load(f)
        errors = get_error_details(task_response)
        print errors