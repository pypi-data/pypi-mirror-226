from math import inf
buckets = (1,2,5,10, inf)


def find_bucket(num):
    # if 0 <= num <= buckets[0]:
    #     return buckets[0]
    for i in range(len(buckets)-1):
        # if i+1 == len(buckets):
        #     return "inf"
        if num == buckets[i]:
            return buckets[i]

        if buckets[i] < num <= buckets[i + 1]:
            return buckets[i + 1]
        else:
            continue

    return "inf"

if __name__ == '__main__':
    for no in range(1, 20):
        print(f' Num: {no}, Bucket: {find_bucket(no)}')