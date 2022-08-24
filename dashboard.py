import streamlit as st
from PIL import Image
import smtplib
from email.message import EmailMessage
import pandas as pd
from dotenv import load_dotenv
import os
import time
from stqdm import stqdm
import mimetypes
from string import Template
import json


import admindashboard
import database as db


def mailer_util(user_name, designation, club_name, club_email):
    st.title('#')
    header_img = Image.open(F'headers/{club_name}-header.png')
    st.image(header_img)
    st.title(f"Welcome {user_name}")
    st.text(f"{designation}, {club_name}")
    st.write("")
    st.write("")
    data_type = st.selectbox(
        "Choose Options", ['Local Excel', 'Google Sheets'])

    emails = []
    names = []

    if data_type == 'Google Sheets':
        st.write("")
        st.write("")
        excel_url = st.text_input("Enter Google Sheets URL")
        if excel_url:
            excel = excel_url.replace('/edit#gid=', '/export?format=csv&gid=')
            df = pd.read_csv(excel)

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
        try:
            df = pd.read_excel(excel, engine='openpyxl')
            names = df['Name'].to_list()
            emails = df['Email'].to_list()
            with st.expander("Show Emails"):
                st.json(emails)
            with st.expander("Show Names"):
                st.json(names)
        except:
            pass

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
            with open(os.path.join("email_body", 'body.txt'), "wb") as f:
                f.write((email_body).getbuffer())
            with open(os.path.join("email_body", 'body.txt'), 'r+') as f:
                body = f.readlines()
            exp_body =' '.join([str(char) for char in body])
            with st.expander('Show Email Body'):
                st.write(exp_body)
        
    def attach_file_to_email(newMessage, file_name, file_extension):
        with open(os.path.join("attachments", f'attachment.{file_extension}'), "rb") as fp:
            file_data = fp.read()
            maintype, _, subtype = (mimetypes.guess_type(file_name)[
                                    0] or 'application/octet-stream').partition("/")
            newMessage.add_attachment(
                file_data, maintype=maintype, subtype=subtype, filename=file_name)

    file_attachment = st.file_uploader("Drop the Attachment Here")
    if file_attachment:
        file_name = file_attachment.name
        file_extension = file_name.split('.')[1]
        with open(os.path.join("attachments", f'attachment.{file_extension}'), "wb") as f:
            f.write(file_attachment.getbuffer())

    load_dotenv()
    email_sender = club_email
    email_password = os.getenv(f"{club_name}-PASSWORD")

    email_receiver = emails ; not_sent_emails_ls = []
    f = open('email_data.json')
    data = json.load(f)
    new_dict = dict(data)
    send_emails = st.button("Send Emails")

    if send_emails:
        db.add_log(user_name,designation,len(email_receiver))
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(email_sender, email_password)
        email_receiver = stqdm(email_receiver)
        for email, name in zip(email_receiver, names):
            
            new_dict.update({email:name})
            newMessage = EmailMessage()
            Reciever_Email = email
            subject = email_subject.format(Name=name)
            
            with open(os.path.join("email_body", 'body.txt'), 'r+') as f:
                body = f.readlines()
            try:
                with open(F'{club_name}-html_body.html','r+',encoding='utf-8') as f:
                    html_body = f.readlines()
            except:
                st.error("NO HTML TEMPLATE FOUND")
                
            body=list(map(lambda x: x.replace('\n','<br>'),body))
            body = ' '.join([str(char) for char in body])
            
            
            html_body = ' '.join([str(char) for char in html_body])
            html_body = Template(html_body)
            html_body = html_body.substitute(Name=name,Body=body)
                

            newMessage['Subject'] = subject
            newMessage['From'] = email_sender
            newMessage['To'] = Reciever_Email
            newMessage.set_content(html_body,subtype='html')
            
            if file_attachment:
                attach_file_to_email(newMessage, file_name, file_extension)
            try:
                smtp.sendmail(from_addr=email_sender,
                            to_addrs=Reciever_Email, msg=newMessage.as_string())
            except:
                not_sent_emails_ls.append(Reciever_Email)
            time.sleep(0.01)
        smtp.quit()
        if len(not_sent_emails_ls)>0:
            st.subheader("Error Sending Emails To:")
            with st.expander('Show Not Sent Emails'):
                st.json(not_sent_emails_ls)
        db.load_json(new_dict)

def main(user_name):
    
    club_ls = ['OWASP-VIIT', 'Vigniters Club']
    
    owasp_designation = dict();vigniters_designation = dict()
    owasp_designation_ls = db.get_owasp()
    vigniters_designation_ls = db.get_igniters()
    
    for i in owasp_designation_ls:
        owasp_designation.update({i[0]:i[1]})
    for j in vigniters_designation_ls:
        vigniters_designation.update({j[0]:j[1]})
    
    if user_name in vigniters_designation.keys():
            auth_token = 'VIGNITERS'; club_n = 0
    if user_name in owasp_designation.keys():
        auth_token = 'OWASP-VIIT';club_n = 1
    if (user_name in owasp_designation.keys()) and (user_name in vigniters_designation.keys()):
        auth_token = 'OWASP-VIIT&VIGNITERS'; club =1
    administrators = ['Chief Secretary','Vice Secretary','Associate Secretary']
    try:
        if owasp_designation[user_name] in administrators:
            club = st.sidebar.selectbox(
            "Choose Club", [club_ls[abs(1-club_n)], club_ls[club_n],"Admin Dashboard"])
        else: 
            club = st.sidebar.selectbox(
                "Choose Club", [club_ls[abs(1-club_n)], club_ls[club_n]])
    except:
        club = st.sidebar.selectbox(
                "Choose Club", [club_ls[abs(1-club_n)], club_ls[club_n]])
        
    if club:

        if club == 'OWASP-VIIT' and (auth_token == 'OWASP-VIIT' or auth_token == 'OWASP-VIIT&VIGNITERS'):
            db.add_log(user_name,owasp_designation[user_name],0)
            mailer_util(
                user_name, owasp_designation[user_name], 'OWASP-VIIT', 'owaspviit@gmail.com')

        elif club == 'Vigniters Club' and (auth_token == 'VIGNITERS' or auth_token == 'OWASP-VIIT&VIGNITERS'):
            db.add_log(user_name,vigniters_designation[user_name],0)
            mailer_util(
                user_name, vigniters_designation[user_name], 'VIGNITERS', 'vignansiit.d2cigniters@gmail.com')
        elif club == 'Admin Dashboard':
            admindashboard.dashboard(user_name)
        else:
            st.error(
                "You Are Not Authorised to view this section, contact the owner for support")
    else:
        pass
