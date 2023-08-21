# A string or word is panagram if it is having all the alphabets

def check_pangram(string):
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    for char in alphabets:
        if not char in string:
            print char, ' not found'
            return False
    return True

if __name__ == '__main__':
    s1 = 'quick brown fox jump over the lazy dog hpst'
    print check_pangram(s1) # True

    s2 = 'quick brown fox jump over the lazy dog'
    print check_pangram(s2)  # False
