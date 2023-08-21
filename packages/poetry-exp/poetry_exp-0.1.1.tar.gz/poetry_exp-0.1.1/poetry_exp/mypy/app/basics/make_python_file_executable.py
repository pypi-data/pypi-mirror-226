"""
The script files mode must be executable and the first line must begin with #! followed by
the path of the Python interpreter. The first is done by executing chmod +x scriptfile or perhaps chmod 755 script file.
The second can be done in a number of ways.
The most straightforward way is to write:
#!/usr/local/bin/python
As the very first line of your file, using the pathname for where the Python interpreter is installed on your platform.
If you would like the script to be independent of where the Python interpreter lives, you can use the env program.
Almost all UNIX variants support the following, assuming the python interpreter is in a directory on the users $PATH:
#! /usr/bin/env python

"""