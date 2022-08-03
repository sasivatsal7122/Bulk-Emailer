import streamlit as st
from PIL import Image
import smtplib
from email.message import EmailMessage
import pandas as pd
from dotenv import load_dotenv
import os
import time
from stqdm import stqdm

def main(username, user_name,designation):
    st.title('#')
    
    club = st.sidebar.selectbox(
        "Choose Club", ['OWASP-VIIT', 'Vigniters Club'])
    if club == 'OWASP-VIIT':
        owasp_header = Image.open('header.png')
        st.image(owasp_header)
        st.title(f"Hello {user_name}")
        st.text(f"{designation}, OWASP-VIIT")
        st.write("")
        st.write("")
        data_type = st.selectbox(
            "Choose Options", ['Local Excel', 'Google Sheets'])

        emails = [];names = []

        if data_type == 'Google Sheets':
            st.write("")
            st.write("")
            excel_url = st.text_input("Enter Google Sheets URL")
            if excel_url:
                excel = excel_url.replace('/edit#gid=', '/export?format=csv&gid=')
                df=pd.read_csv(excel)
                
                names = df['Name'].to_list()
                emails = df['Email'].to_list()
                try:
                    with st.expander("Show Emails"):
                        st.json(emails)
                    with st.expander("Show Names"):
                        st.json(names)
                except:
                    pass
                
            
        else:
            st.write("")
            st.write("")
            excel = st.file_uploader("Drop The Excel File")
            #try:
            df = pd.read_excel(excel, engine='openpyxl')
            names = df['Name'].to_list()
            emails = df['Email'].to_list()
            with st.expander("Show Emails"):
                st.json(emails)
            with st.expander("Show Names"):
                st.json(names)
            #except:
                #pass
        
        st.write("")
        st.write("")
        st.header("Email Subject & Body")
        col1, col2 = st.columns(2)
        with col1:
            st.write("")
            st.write("")
            email_subject = st.text_input("Enter Email Subject")

        with col2:
            st.write("")
            st.write("")
            email_body = st.file_uploader("Drop The Email Body")
            if email_body:
                with open(os.path.join("email_body",email_body.name),"wb") as f:
                    f.write((email_body).getbuffer())
                with open(os.path.join("email_body",email_body.name),'r+') as f:
                    body = f.readlines()

        load_dotenv()
        email_sender = 'owaspviit@gmail.com'
        email_password = os.getenv("PASSWORD")

        email_receiver = emails
        send_emails = st.button("Send All The emails")
        
        if send_emails:
            print(emails)
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login(email_sender, email_password)
            email_receiver = stqdm(email_receiver)
            for email,name in zip(email_receiver,names):

                Reciever_Email = email

                newMessage = EmailMessage()

                subject = email_subject.format(Name=name)
                
                with open(os.path.join("email_body",email_body.name),'r+') as f:
                    body = f.readlines()
                
                body = ' '.join([str(char) for char in body])
                body = body.format(Name=name)

                newMessage['Subject'] = subject
                newMessage['From'] = email_sender
                newMessage['To'] = Reciever_Email
                newMessage.set_content(body)

                smtp.sendmail(from_addr=email_sender,
                                to_addrs=Reciever_Email, msg=newMessage.as_string())
                time.sleep(0.5)
            smtp.quit()
