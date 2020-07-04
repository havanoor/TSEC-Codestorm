from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
def sendmail(name,email,mess):
    msg = MIMEMultipart()
    msg['From'] = "psycho.saiyan20@gmail.com"
    password='mzvmwencqnpmjczv'
    greet = "{} has written to AURA,\n email:  {},".format(name,email)
    msg['To']= 'djsceaura@gmail.com'
    msg['Subject'] = "{} has sent a message!".format(name)
    msg.attach(MIMEText(greet))
    msg.attach(MIMEText("<br><br><b> Message:</b>  <p>{}</p>".format(mess), 'html'))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(msg['From'],password)
    s.sendmail(msg['From'],msg['To'],msg.as_string())
    s.quit()


def repmail(name,email):
    msg = MIMEMultipart()
    msg['From'] = "Noreply.contactaura@gmail.com"
    password='Aurakayamrahe'
    greet = "Dear {},".format(name)
    msg['To']= email
    msg['Subject'] = "Thanks for reaching out!"
    msg.attach(MIMEText(greet))
    msg.attach(MIMEText("<br>Thank you for contacting us!<p>We have received your email. One of our members should get back to you as soon as possible!</p><br><p>Please note that this is a no-reply email, and messages sent here will not be seen. If you would like to contact us again, please use the account <b>djsceaura@gmail.com</b></p><p>Thanking you,<br> Yours sincerely,</p><p>Team AURA</p>", 'html'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(msg['From'],password)
    s.sendmail(msg['From'],msg['To'],msg.as_string())
    s.quit()
