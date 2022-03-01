import smtplib
from config import config_options

server = smtplib.SMTP_SSL(config_options["mail_server"], config_options["mail_port"])

# Next, log in to the server
server.login(config_options["email_from"], config_options["email_password"])

# Send the email
msg = "Subject: test\n\ntest" # The newlines separate the message from the headers
server.sendmail(config_options["email_from"], config_options["email_to"], msg)