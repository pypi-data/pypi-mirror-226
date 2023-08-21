

if __name__ == '__main__':

    for i in range(10):
        print 'i: ', i
        for j in range(5):
            print 'j: ', j
            if j == 2:
                break  # will break only inner not outer
