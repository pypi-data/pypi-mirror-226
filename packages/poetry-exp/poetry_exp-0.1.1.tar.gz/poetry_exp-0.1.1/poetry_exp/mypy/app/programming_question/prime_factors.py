
def find_prime_factors(num):
    prime_factor = []
    i = 2
    while i <= num:
        if num % i == 0:
            if i not in prime_factor:
                prime_factor.append(i)
            num = num/i
            i -= 1
        i += 1
    return prime_factor


if __name__ == '__main__':
    print find_prime_factors(35)  # 5, 7
    print find_prime_factors(72)  # [2, 3]
    print find_prime_factors(12)  # [2,3]
    print find_prime_factors(189)  # [3, 7]


