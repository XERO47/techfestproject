import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to, subject, body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'themaker1602@gmail.com'
    smtp_password = 'hzcg uwdl kycs tvej'
    from_email = smtp_username
    to_email = to
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body))
    smtp_server = smtplib.SMTP(smtp_server, smtp_port)
    smtp_server.starttls()
    smtp_server.login(smtp_username, smtp_password)
    try:
      smtp_server.sendmail(from_email, to_email, message.as_string())
      print("Alert sent successfully")
    except:
       print("Email was not sent")
    
    smtp_server.quit()
