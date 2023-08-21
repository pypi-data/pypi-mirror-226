import glob
import os
# def find_files(root_dir):
#     files = []
#     for filename in glob.iglob(root_dir, '**/*', recursive=True):
#         print filename
#         files.append(filename)
#     return files


"""
root, sub_dir, files in os.walk(dir_path)
root: Current path which is "walked through"
subdirs: Files in root of type directory
files: Files in root (not in subdirs) of type other than directory
"""

def find_files_in_sorted_order(dir_path):
    file_list = []
    for root, sub_dir, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            # os.path.getsize give the size in bytes
            file_list.append({'name': file, 'file_path': file_path, 'size': os.path.getsize(file_path)})

    file_list.sort(key=lambda d: d['size'])
    return file_list


if __name__ == '__main__':
    #fl = find_files_in_sorted_order('C:\\Users\\mohama30\\Documents\\EMC\\repository\\personal\\cb-python\\cb-python\\python-demo\\python-program\\file_handling')
    #fl = find_files_in_sorted_order('.')
    print os.path.abspath(__file__) # current file absolute path C:\Users\mohama30\Documents\EMC\repository\personal\cb-python\cb-python\python-demo\python-program\file_handling\sort_files_by_size.py
    print os.getcwd() # C:\Users\mohama30\Documents\EMC\repository\personal\cb-python\cb-python\python-demo\python-program\file_handling

    fl = find_files_in_sorted_order(os.path.dirname(os.path.abspath(__file__)))
    print fl

    for f in fl:
        print f


"""
{'size': 38L, 'name': 'test1', 'file_path': 'C:\\Users\\mohama30\\Documents\\EMC\\repository\\personal\\cb-python\\cb-python\\python-demo\\python-program\\file_handling\\files\\test1'}
{'size': 46L, 'name': 'test2', 'file_path': 'C:\\Users\\mohama30\\Documents\\EMC\\repository\\personal\\cb-python\\cb-python\\python-demo\\python-program\\file_handling\\files\\test2'}
{'size': 135L, 'name': 'capatalize_every_word.py', 'file_path': 'C:\\Users\\mohama30\\Documents\\EMC\\repository\\personal\\cb-python\\cb-python\\python-demo\\python-program\\file_handling\\capatalize_every_word.py'}
{'size': 231L, 'name': 'find_no_of_lines.py', 'file_path': 'C:\\Users\\mohama30\\Documents\\EMC\\repository\\personal\\cb-python\\cb-python\\python-demo\\python-program\\file_handling\\find_no_of_lines.py'}
{'size': 278L, 'name': 'find_all_num.py', 'file_path': 'C:\\Users\\mohama30\\Documents\\EMC\\repository\\personal\\cb-python\\cb-python\\python-demo\\python-program\\file_handling\\find_all_num.py'}
{'size': 579L, 'name': 'find_word_count.py', 'file_path': 'C:\\Users\\mohama30\\Documents\\EMC\\repository\\personal\\cb-python\\cb-python\\python-demo\\python-program\\file_handling\\find_word_count.py'}
{'size': 655L, 'name': 'count_no_of_spaces.py', 'file_path': 'C:\\Users\\mohama30\\Documents\\EMC\\repository\\personal\\cb-python\\cb-python\\python-demo\\python-program\\file_handling\\count_no_of_spaces.py'}
{'size': 1123L, 'name': 'sort_files_by_size.py', 'file_path': 'C:\\Users\\mohama30\\Documents\\EMC\\repository\\personal\\cb-python\\cb-python\\python-demo\\python-program\\file_handling\\sort_files_by_size.py'}

"""