import smtplib, ssl
from pprint import pprint

def sendmails(message):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "itaivincent321@gmail.com"
    receiver_email = "vincentmhokore@gmail.com"
    password = "Tinasheitaianesu321"

    context = ssl.create_default_context()
    # pprint(sender_email, receiver_email, message)
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        try:
            server.login(sender_email,password)
            res = server.sendmail(sender_email, receiver_email, message)
            print('email sent!')
        except:
            print('email failed to send for some reason')


