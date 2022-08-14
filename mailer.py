import smtplib
from email.message import EmailMessage
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from time import sleep
import os
from string import Template


def read_info():
    df = pd.read_excel("test_xl.xlsx")
    print(df)
    names = df['Name'].to_list()
    emails = df['Email'].to_list()
    rolls = df['Roll'].to_list()
    print(names)
    print(emails)
    print(rolls)
    return emails, names, rolls


def send_mail():
    load_dotenv()

    email_sender = 'owaspviit@gmail.com'
    email_password = os.getenv("OWASP-VIIT-PASSWORD")
    print(email_sender, email_password)
    #email_receiver = ['sasivatsal7122@gmail.com','likhithbavisetti@gmail.com','mallaharsha66@gmail.com','lokeshwarlakhi@gmail.com']
    email_receiver = ['sasivatsal7122@gmail.com','vatsal7122@gmail.com']
    email_receiver = tqdm(email_receiver)
    names = ['Satya Sasi Vatsal','Allu Arjun']

    for email,name in zip(email_receiver,names):
        Reciever_Email = email

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()

        smtp.login(email_sender, email_password)

        newMessage = EmailMessage()
        
        with open('email_body/body.txt','r+') as f:
            body = f.readlines()
            
        with open('html_body.html','r+',encoding='utf-8') as f:
            html_body = f.readlines()
        
            
        subject = 'Hey dfgdgh {Name}'
        subject = subject.format(Name=name)
        
        body=list(map(lambda x: x.replace('\n','<br>'),body))
        body = ' '.join([str(char) for char in body])
                
        html_body = ' '.join([str(char) for char in html_body])
        html_body = Template(html_body)
        html_body = html_body.substitute(Name=name,Body=body)
                
        newMessage['Subject'] = subject
        newMessage['From'] = email_sender
        newMessage['To'] = Reciever_Email
        newMessage.set_content(html_body,subtype='html')

        smtp.sendmail(from_addr=email_sender, to_addrs=Reciever_Email, msg=newMessage.as_string())
        sleep(.01)

    smtp.quit()


if __name__ == '__main__':  
   # emails, names, rolls = read_info()
    send_mail()