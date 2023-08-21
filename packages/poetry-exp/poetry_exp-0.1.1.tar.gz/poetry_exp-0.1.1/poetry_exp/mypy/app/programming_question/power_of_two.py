
def is_power_of_two(num):
    square = 1
    while num >= square:
        if num == square:
            return True
        square = square*2
    return False


if __name__ == '__main__':
    numbers = range(33)
    for num in numbers:
        print num, 'is power of 2: ', is_power_of_two(num)