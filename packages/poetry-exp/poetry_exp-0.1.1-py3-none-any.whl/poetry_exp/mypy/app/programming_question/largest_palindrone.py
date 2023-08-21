
def is_palindrone(num):
    s = str(num)
    return s==s[-1::-1]


def largest_palindrone():
    max = 0
    for i in range(10, 100):
        for j in range(10, 100):
            p = i*j
            if is_palindrone(p):
                if p > max:
                    max = p
    return max


def largest_palindrone_three_digit():
    max = 0
    for i in range(10, 1000):
        for j in range(10, 1000):
            p = i*j
            if is_palindrone(p):
                if p > max:
                    max = p
    return max


if __name__ == '__main__':
    print is_palindrone(9009)

    print largest_palindrone()  # 9009
    print largest_palindrone_three_digit() # 906609