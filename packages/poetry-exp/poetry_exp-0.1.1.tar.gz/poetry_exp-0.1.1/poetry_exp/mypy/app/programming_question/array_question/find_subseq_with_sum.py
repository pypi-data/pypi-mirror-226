

def find_sub_seq_with_sum(arr, sums):

    s = 0
    indexes = []
    i = 0
    while i < len(arr):
        print 'i: ', i
        indexes.append(i)
        s += arr[i]

        print '....s: ', s
        if s > sums:
            print 's: ', s
            print 'indexes', indexes
            if len(indexes)>=2:
               i = indexes[1]
            indexes = []
        elif s == sums:
            for j in indexes:
                print arr[j]
            s = 0
            i = indexes[-1]
            indexes = []
            print '..................'

        else:
           i = i+1


if __name__ == '__main__':
    a = [1,2,3,4,1,5,6,1, 2,3,4]
    s = 5
    find_sub_seq_with_sum(a, s)
