import re
str ="help not help1count in help"
match = re.findall("\\bhelp\\b", str)
if match:
    print(match)
    print("word#",len(match))
else:
    print ("Not match")


f = open('email.txt','r')
match = re.findall("\\baafak.mohammad@cloudbyte.com\\b", f.read())
if match:
    print(match)
    print("word#",len(match))
else:
    print ("Not match")
