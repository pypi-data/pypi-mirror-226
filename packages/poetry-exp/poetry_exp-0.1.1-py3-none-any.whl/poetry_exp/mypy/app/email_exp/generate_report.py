
def generate_report(res):
    # Add body to email
    filename = str(res['result']['verificationInfo']['bootVerification']['bootScreenshotPath'])
    filename = 'screenshot.png'
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
    <br>
     <p>Virtual Machine Boot Screenshot:<br>
     <img src='"""+filename+"""'>
      </body>
    </html>
    """

    report = "backup_verification_report.html"
    # Open file in binary mode
    with open(report, "w") as f:
        print(f)
        # Add file as application/octet-stream
        f.write(body)
        print('Report created...')




if __name__ == "__main__":
    generate_report({"status": "success", "result": {"verificationInfo": {"bootVerification": {"state": "Ok", "status": "Ok", "stateReason": "Ok", "verifiedAt": "2021-01-28T09:28:11.509Z", "bootScreenshotPath": "../20nov/screenshot.jpg"}, "mountVerification": {"state": "Ok", "status": "Ok", "stateReason": "Ok", "verifiedAt": "2021-01-28T09:28:11.509Z"}, "dataIntigrity": {"state": "Ok", "status": "Ok", "stateReason": "Ok", "verifiedAt": "2021-01-28T09:28:11.509Z"}}}})
