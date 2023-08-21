with open('find_tripplet.py') as f:
    # f.readline() Only one line
    # f.xreadline(), It iterates over the lines in a file, yielding each one to let us process it before reading the next line

    # for line in f.xreadlines():
    #     #print line
    #     pass

    print 'comes..'
    # If we use our file object in an iterator, it starts yielding us lines, just like xreadlines()!
    for line in f:
        print line

    for line in f.readlines():  # load all the lines from file
        #print line
        pass


count = 0
with open('find_tripplet.py') as f:
    for w in f.read():
        if w.isupper():
            print 'Found Capital Latter: ', w
            count += 1

print count


# one line solution
with open('find_tripplet.py') as fh:
    count = sum(ch.isupper() for line in fh for ch in line)
    print count



