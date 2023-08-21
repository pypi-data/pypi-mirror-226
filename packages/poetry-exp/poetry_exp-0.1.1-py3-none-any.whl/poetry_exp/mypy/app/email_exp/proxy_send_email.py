import smtplib
import socks

#'proxy_port' should be an integer
#'PROXY_TYPE_SOCKS4' can be replaced to HTTP or PROXY_TYPE_SOCKS5
socks.setdefaultproxy(socks.HTTP, "web-proxy.in.hpecorp.net", 8080)
socks.wrapmodule(smtplib)

to='aafak-mohammad@hpe.com'
fromname='Nithin Karthik'
fromemail='no-reply@hpe.com'
subject='Hello'
body='Good Evening !!'

message=''
message+= "To: " + to + "\n"
message+= "From: \"" + fromname + "\" <" + fromemail + ">\n"
message+= "Subject: " + subject + "\n"
message+= "\n"
message+= body

print('Creating mail server.......')
mailserver = smtplib.SMTP('smtp3.hpe.com')
print(f'mailserver: {mailserver}')

mailserver.ehlo()
print(f'Sending mail....')

mailserver.sendmail(fromemail, to, message)
print(f'Email sent...')

mailserver.quit()