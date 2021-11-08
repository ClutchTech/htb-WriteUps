import smtplib
host = '127.0.0.1'
port = 25

sender_email = "kyle@writer.htb"
receiver_email = "kyle@writer.htb"

with open('evil_disclaimer', 'r') as f:
    message = f.read()

try:
    server = smtplib.SMTP(host,port)
    server.ehlo()
    server.sendmail(sender_email,receiver_email,message)
except Exception as e:
    print(e)
