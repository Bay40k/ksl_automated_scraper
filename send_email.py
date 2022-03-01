import smtplib


async def send_email(
    mail_server: str,
    mail_port: int,
    email_from: str,
    email_password: str,
    email_to: str,
    subject: str,
    body: str,
):
    server = smtplib.SMTP_SSL(mail_server, mail_port)

    # Next, log in to the server
    server.login(email_from, email_password)

    # Send the email
    msg = f"Subject: {subject}\n\n{body}".encode(
        "UTF-8"
    )  # The newlines separate the message from the headers
    server.sendmail(email_from, email_to, msg)
