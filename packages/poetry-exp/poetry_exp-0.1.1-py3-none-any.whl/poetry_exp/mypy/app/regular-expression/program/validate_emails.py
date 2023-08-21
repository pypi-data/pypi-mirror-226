import re

PATTERN =  "^[\w\._-]+@[\w]+\.{1}[a-zA-Z]+$"
PATTERN =  "^([\w\._-]+)@([\w]+\.{1}[a-zA-Z]+)$"  # grouping
#PATTERN =  "^[\w\._-]+@[\w\.]+\.[\D]{1}$" will make shan.mohammad.rath@gmail.com.in invalid

def validate_email(email):
   match = re.match(PATTERN, email)
   if match:
       print match.groups()
       print email, ": is valid"
       return True
   else:
       print email, ": is not valid"
       return False


"((25[0-5]| 1[0-9][0-9]| [0-1][0-9][0-9] |2[o-4][0-9]) \.){3}()"

if __name__=='__main__':
    email_list = [
        'aafak.mohammad@emc.com',
        'aafak.mohammad@emc..com',
        'aafak.mitsmca09@gmail.com',
        'shan.mohammad.rath@gmail.com',
        'shan.mohammad.rath@gmail.com.in',
        'invalid@com',
        'invalid.invalid@com',
        'invalid.gmail.com',
        'shan.mohammad.rath@gmail.com2',


    ]

    for email in email_list:
        validate_email(email)