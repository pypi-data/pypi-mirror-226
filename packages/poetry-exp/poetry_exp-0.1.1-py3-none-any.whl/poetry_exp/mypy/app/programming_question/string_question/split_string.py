

if __name__ == '__main__':
    s = 'abc xyz "pqr mno ijk" def "ghi klm" uvw'
    found_qoutes = False
    quotes_str = []
    for word in s.split():

        if word.startswith('"'):
            found_qoutes = True

        if not found_qoutes:
            print word
        else:
            if word.endswith('"'):
               found_qoutes = False
               quotes_str.append(word)
               print " ".join(quotes_str)
               quotes_str = []
               continue

            quotes_str.append(word)

"""
abc
xyz
"pqr mno ijk"
def
"ghi klm"
uvw
"""