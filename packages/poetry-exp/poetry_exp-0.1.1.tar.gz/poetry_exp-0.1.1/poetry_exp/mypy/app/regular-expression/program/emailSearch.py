import re

str = 'purple alice@google.com, blah monkey bob@abc.com blah dishwasher'
tuples = re.findall(r'([\w\.-]+)@([\w\.-]+)', str)
print (tuples)  ## [('alice', 'google.com'), ('bob', 'abc.com')]
for tuple in tuples:
   print (tuple[0])  ## username
   print (tuple[1])  ## host

print('The content of email.txt');
with open('email.txt') as FileObj:
    for line in FileObj:
        print(line) #will read one line at the time to memory, and close the file when done.
        

f = open('email.txt','rU')
for line in f:
    print(line)
f.close()    


f = open('email.txt','r')
emails = re.findall(r'[\w\.-]+@[\w\.-]+',f.read())
for email in emails:
    print(email)
f.close()    


f = open('email.txt','r')
emails = re.findall(r'([\w\.-]+)@([\w\.-]+)',f.read())
for email in emails:
    print("username:",email[0])
    print("host:",email[1])
f.close()
