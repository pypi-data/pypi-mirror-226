import re


def remove_special_char(string):
    return re.sub("\s|-|@|!|%|&|\*|\(|\)|\+|=|\?|<|>|!|\^|#|\$", "", string)



def remove_special_char2(string):
    return re.sub("[^a-zA-Z0-9]", "", string)

if __name__ == '__main__':
    print remove_special_char("abc SG-1 ksj!@#$%^&*()hdkj@") # abcSG1ksjhdkj

    print remove_special_char2("abc SG-1 ksj!@#$%^&*()hdkj@") # abcSG1ksjhdkj