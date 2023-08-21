#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# import Datetime for the document's timestamp
from datetime import datetime

# import glob and os
import os, glob

# use the elasticsearch client's helpers class for _bulk API
from elasticsearch import Elasticsearch, helpers

# declare a client instance of the Python Elasticsearch library
client = Elasticsearch("http://localhost:9200")

# posix uses "/", and Windows uses ""
if os.name == 'posix':
    slash = "/" # for Linux and macOS
else:
    slash = chr(92) # '\' for Windows

def current_path():
    return os.path.dirname(os.path.realpath( __file__ ))

# default path is the script's current dir
def get_files_in_dir(self=current_path()):

    # declare empty list for files
    file_list = []

    # put a slash in dir name if needed
    if self[-1] != slash:
        self = self + slash

    # iterate the files in dir using glob
    for filename in glob.glob(self + '*.*'):

        # add each file to the list
        file_list += [filename]

    # return the list of filenames
    return file_list

def get_data_from_text_file(file):

    # declare an empty list for the data
    data = []

    # get the data line-by-line using os.open()
    for line in open(file, encoding="utf8", errors='ignore'):

        # append each line of data to the list
        data += [ str(line) ]

    # return the list of data
    return data

# pass a directory (relative path) to function call
all_files = get_files_in_dir("C:\\Users\\aafakmoh\\OneDrive - Hewlett Packard Enterprise\\root")

# total number of files to index
print ("TOTAL FILES:", len( all_files ))

"""
PART 2 STARTS HERE
"""
# define a function that yields an Elasticsearch document from file data
def yield_docs(all_files):

    # iterate over the list of files
    for _id, _file in enumerate(all_files):

        # use 'rfind()' to get last occurence of slash
        file_name = _file[ _file.rfind(slash)+1:]

        # get the file's statistics
        stats = os.stat( _file )

        # timestamps for the file
        create_time = datetime.fromtimestamp( stats.st_ctime )
        modify_time = datetime.fromtimestamp( stats.st_mtime )

        # get the data inside the file
        data = get_data_from_text_file( _file )

        # join the list of data into one string using return
        data = "".join( data )

        # create the _source data for the Elasticsearch doc
        doc_source = {
            "file_name": file_name,
            "create_time": create_time,
            "modify_time": modify_time,
            "data": data
        }

        # use a yield generator so that the doc data isn't loaded into memory
        yield {
            "_index": "my_files",
            "_type": "some_type",
            "_id": _id + 1, # number _id for each iteration
            "_source": doc_source
        }

try:
    # make the bulk call using 'actions' and get a response
    resp = helpers.bulk(
        client,
        yield_docs( all_files )
    )
    print ("\nhelpers.bulk() RESPONSE:", resp)
    print ("RESPONSE TYPE:", type(resp))
except Exception as err:
    print("\nhelpers.bulk() ERROR:", err)