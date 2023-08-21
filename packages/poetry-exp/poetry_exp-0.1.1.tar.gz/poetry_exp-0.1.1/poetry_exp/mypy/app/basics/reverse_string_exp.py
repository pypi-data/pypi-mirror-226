

def revers_str(s):
    if len(s) == 1:
        return s
    return revers_str(s[1:]) + s[0]

print revers_str("abcdef")

# In-place reverse not possible in string, because it is immutable

str = "Python"
rev_str = "".join([str[i] for i in range(len(str)-1, -1, -1)])
print rev_str # nohtyP
print str

str = "hello"
reverse = str[::-1]
print reverse
print str

