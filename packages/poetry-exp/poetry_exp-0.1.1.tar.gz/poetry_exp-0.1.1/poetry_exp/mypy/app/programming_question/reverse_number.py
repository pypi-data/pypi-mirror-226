
def reverse_number(num):
    reverse = 0
    while num > 0:
        reminder = num % 10
        reverse = reverse * 10 + reminder
        num = num/10
    return reverse


if __name__ == '__main__':
    print reverse_number(123)  # 321
    print reverse_number(12345) # 54321
