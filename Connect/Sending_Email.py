import smtplib

def feedback_email_to_team(Name, Email, Feedback_given):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        subject = 'Feedback from ' + Name
        body = 'Name : ' + Name + '\n\n' + 'Email : ' + \
            Email + '\n\n' + 'Feedback : ' + Feedback_given
        msg = f'Subject: {subject}\n\n{body}'
        smtp.login("connect.mtv14@gmail.com", "eqjyisorlqbhczzg")  # Wrong password

        smtp.sendmail("connect.mtv14@gmail.com", "connect.mtv14@gmail.com", msg)
