from smtplib import SMTP_SSL as SMTP_SSL       # this invokes the secure SMTP protocol (port 465, uses SSL)
from smtplib import SMTP                       # use this for standard SMTP protocol   (port 25, no encryption)


to='aafak-mohammad@hpe.com'
fromname='Nithin Karthik'
fromemail='no-reply@hpe.com'
subject='Hello1233333'
body='Good Evening !!'

message=''
message+= "To: " + to + "\n"
message+= "From: \"" + fromname + "\" <" + fromemail + ">\n"
message+= "Subject: " + subject + "\n"
message+= "\n"
message+= body

print('Creating mail server.......')
#mailserver = SMTP('smtp3.hpe.com')
mailserver = SMTP('16.208.49.245')

mailserver.set_debuglevel(1)
print(f'mailserver: {mailserver}')

mailserver.ehlo()
print(f'Sending mail@@@@@@....')

mailserver.sendmail(fromemail, to, message)
print(f'Sent mail...@@@@@@@@@@@@@@@@@.')

mailserver.quit()