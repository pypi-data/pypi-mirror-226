"""

The code in the else block is executed after the for loop completes,
If a break is encountered in the for loop execution, else block will not executed.
"""

if __name__ == '__main__':

    for i in range(5):
        if i==3:
            break
        print i
    else:
        print 'Loop Executed successfully'  # will not execute because there is a break statement in loop

    for i in range(5):
       print i
    else:
        print 'Loop Executed successfully' # wiil print this because there is no break
