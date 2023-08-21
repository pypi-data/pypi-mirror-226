
def find_k_numbers_with_most_occurance():
    pass



import re
with open('find_possible_triangles.py', 'r') as fh:

    ch = re.findall(r'\S', fh.read())
    if ch:
        print len(ch)