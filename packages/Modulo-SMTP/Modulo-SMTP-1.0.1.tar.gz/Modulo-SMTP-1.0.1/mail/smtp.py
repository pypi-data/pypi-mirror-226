from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib



def sendMail(to, subject, message):
    msg =MIMEMultipart()    
    #message= "hola como estas"
    # application --> Monitoring
    # password--> fcgbefhoxfldztxf

    password="fcgbefhoxfldztxf"
    msg['From']="rodolfo.herr@yahoo.com.ar"
    #msg['To']="dherr.ar@gmail.com"
    msg['To']=to
    #msg['Subject']='Suscription'
    msg['Subject']=subject

    msg.attach(MIMEText(message,'plain'))

    server=smtplib.SMTP('smtp.mail.yahoo.com.ar',587)
    server.starttls()
    server.login(msg['From'],password)

    server.sendmail(msg['From'],msg['To'],msg.as_string())

    server.quit()

    print ("Succesfully sent email to %s" %(msg['To']))
    return