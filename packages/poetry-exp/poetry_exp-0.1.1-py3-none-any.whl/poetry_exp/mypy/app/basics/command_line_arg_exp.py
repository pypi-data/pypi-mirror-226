import sys

cmd_args = sys.argv
print cmd_args

"""
$ chmod +x demo.py
$ ./demo.py input.txt output.txt

['demo.py', 'input.txt', 'output.txt'] 



['C:/Users/mohama30/Documents/EMC/repository/personal/cb-python/cb-python/python-demo/python-program/basics/command_line_arg_exp.py']

"""


total = len(sys.argv)
cmdargs = str(sys.argv)
print ("The total numbers of args passed to the script: %d " % total)
print ("Args list: %s " % cmdargs)
print ("Script name: %s" % str(sys.argv[0]))
for i in xrange(total):
    print ("Argument # %d : %s" % (i, str(sys.argv[i])))


"""
$ ./demo.py -i input.txt -o output.txt
The total numbers of args passed to the script: 5 
Args list: ['./demo.py', '-i', 'input.txt', '-o', 'output.txt'] 
Script name: ./demo.py
Argument # 0 : ./demo.py
Argument # 1 : -i
Argument # 2 : input.txt
Argument # 3 : -o
Argument # 4 : output.txt

"""