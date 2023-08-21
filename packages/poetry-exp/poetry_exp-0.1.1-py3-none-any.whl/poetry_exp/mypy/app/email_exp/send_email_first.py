import smtplib

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("aafak.mitsmca09@gmail.com", "behonest@CB1989")
server.sendmail(
  "aafak.mitsmca09@gmail.com",
  "aafak.mitsmca09@gmail.com",
  "this message is from python")
server.quit()