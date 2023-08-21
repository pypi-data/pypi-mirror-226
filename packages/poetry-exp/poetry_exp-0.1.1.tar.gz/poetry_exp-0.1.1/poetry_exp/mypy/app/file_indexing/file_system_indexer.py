import os
import uuid
from file_indexing.es_bulk_api import ESBulkApiHelper
from datetime import datetime

"""
def all_files(directory):
    for path, dirs, files in os.walk(directory):
        for f in files:
            yield os.path.join(path, f)

r3d_files = [f for f in all_files(your_directory)
               if f.endswith('.R3D')]
"""

def get_all_file_path(folder='.'):
    filepaths = [os.path.join(folder, f) for f in os.listdir(folder)]
    return filepaths


def get_all_files(root_dir):
    file_objects = []
    for path, subdirs, files in os.walk(root_dir):
        file_obj = {
            'path': path,
            'subDirs': [],
            'size': os.path.getsize(path)
        }
        file_details = []

        for file in files:
            file_full_path = os.path.join(path, file)
            stats = os.stat(path)
            file_details.append({
                'name': file,
                'size': os.path.getsize(file_full_path),
                'createdAt': str(datetime.fromtimestamp(stats.st_ctime)),
                'updatedAt':  str(datetime.fromtimestamp(stats.st_mtime))
            })
        file_obj['files'] = file_details

        sub_file_objects = []
        if subdirs:
            for dir in subdirs:
                sub_file_objects.extend(get_all_files(os.path.join(root_dir, dir)))
        file_obj['subDirs'] = sub_file_objects
        file_objects.append(file_obj)

        return file_objects


class ESFileIndexer:
    def __init__(self, files):
        self.bulk_api = ESBulkApiHelper()
        self.files = files

    def build_docs(self, files):
        # files = get_all_files('C:\\Users\\aafakmoh\\Desktop')
        for file in files:
            sub_dirs = file.pop('subDirs', [])
            if sub_dirs:
                self.build_docs(sub_dirs)
            file_path = file['path']
            file['name'] = file_path[file_path.rindex('\\')+1:]
            self.bulk_api.add_document('files', str(uuid.uuid4()), file)

    def index_files(self):
        self.build_docs(self.files)
        self.bulk_api.bulk_update()




if __name__ == '__main__':
    #print(get_all_file_path('C:\\Users\\aafakmoh\\Desktop'))
    #print(get_all_files('C:\\Users\\aafakmoh\\Desktop'))

    files = get_all_files('C:\\Users\\aafakmoh\\Downloads')

    fi = ESFileIndexer(files)
    fi.index_files()