import re


def count_char(file_path='email.txt'):
    with open(file_path, 'r') as file_obj:
        return len(re.findall(r'\S', file_obj.read()))


def count_word(file_path='email.txt'):
    with open(file_path, 'r') as file_obj:
        #return len(re.findall(r'[\w@\.]+', file_obj.read()))
        return len(re.findall(r'\b[\w@\.:]+\b', file_obj.read()))
if __name__ == '__main__':
    print count_char()
    print count_word()