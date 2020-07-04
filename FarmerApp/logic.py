from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
def sendmail(name,email,id,tot):
    msg = MIMEMultipart()
    msg['From'] = "psycho.saiyan20@gmail.com"
    password='mzvmwencqnpmjczv'
    greet = "Hey {}!".format(name)
    msg['To']= email
    msg['Subject'] = "Confirmation of your order (id {})".format(id)
    msg.attach(MIMEText(greet))
    msg.attach(MIMEText('<p align ="center" <br> Thanks for shopping with us! <br>This is to confirm your order worth Rs {} with us!</p><p> Do come by and shop again! '.format(tot), 'html'))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(msg['From'],password)
    s.sendmail(msg['From'],msg['To'],msg.as_string())
    s.quit()
