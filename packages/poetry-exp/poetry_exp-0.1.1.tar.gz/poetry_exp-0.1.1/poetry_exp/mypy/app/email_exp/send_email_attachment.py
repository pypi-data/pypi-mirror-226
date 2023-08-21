import smtplib, email, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_email(res):

    to = "aafak-mohammad@hpe.com"
    fromname = "Nithin Karthik"
    fromemail = "no-reply@hpe.com"

    message = MIMEMultipart()
    message["From"] = fromemail
    message["To"] = to
    message["Subject"] = "Verify Status Report"
    body = """\
    <html>
      <head>
            <style>
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 5px;
                    text-align: left;    
                }    
            </style>
      </head>
      <body>
        <p>Verification """+str(res['status'])+"""!!<br>
        </p>
        <table>
        <tr>
            <th>Type</th>
            <th>Status</th>
            <th>Verified At</th>
        </tr>
        <tr>
            <td>Boot Verification</td>
            <td>"""+str(res['result']['verificationInfo']['bootVerification']['status'])+"""</td>
            <td>"""+str(res['result']['verificationInfo']['bootVerification']['verifiedAt'])+"""</td>
        </tr>
        <tr>
            <td>Mount Verification</td>
            <td>"""+str(res['result']['verificationInfo']['mountVerification']['status'])+"""</td>
            <td>"""+str(res['result']['verificationInfo']['mountVerification']['verifiedAt'])+"""</td>
        </tr>
        <tr>
            <td>Data Integrity</td>
            <td>"""+str(res['result']['verificationInfo']['dataIntigrity']['status'])+"""</td>
            <td>"""+str(res['result']['verificationInfo']['dataIntigrity']['verifiedAt'])+"""</td>
        </tr>
    </table>
      </body>
    </html>
    """

    # Add body to email
    message.attach(MIMEText(body, "html"))

    filename = str(res['result']['verificationInfo']['bootVerification']['bootScreenshotPath'])
    filename = 'screenshot.png'
    # Open file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part["Content-Disposition"] = 'attachment; filename="%s"' % filename

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()

    mailserver = smtplib.SMTP("smtp3.hpe.com")
    mailserver.ehlo()
    mailserver.sendmail(fromemail, to, message.as_string())
    mailserver.quit()
    print('Email enst')


if __name__ == "__main__":
    send_email({"status": "success", "result": {"verificationInfo": {"bootVerification": {"state": "Ok", "status": "Ok", "stateReason": "Ok", "verifiedAt": "2021-01-28T09:28:11.509Z", "bootScreenshotPath": "../20nov/screenshot.jpg"}, "mountVerification": {"state": "Ok", "status": "Ok", "stateReason": "Ok", "verifiedAt": "2021-01-28T09:28:11.509Z"}, "dataIntigrity": {"state": "Ok", "status": "Ok", "stateReason": "Ok", "verifiedAt": "2021-01-28T09:28:11.509Z"}}}})
