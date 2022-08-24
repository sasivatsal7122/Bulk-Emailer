import streamlit as st
import streamlit_authenticator as stauth
import pickle
from pathlib import Path

# local imports
import dashboard
import database as db

def run_login():
    st.set_page_config(page_title="Bulk Club Mailer",page_icon="📨")

    names = [];usernames=[];hashed_passwords = []
    login_details = db.view_all_data()
    for i in login_details:
        names.append(i[0])
        usernames.append(i[2])
        hashed_passwords.append(i[3])
    
    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,cookie_name='s',key='j',cookie_expiry_days=1)
    name,authentication_status,username=authenticator.login("Login","main")

    if authentication_status:
        authenticator.logout('Logout', 'sidebar')
        dashboard.main(name)
        
    elif authentication_status == False:
        st.error('Username/password is incorrect')
        

    elif authentication_status == None:
        st.warning('Please enter your username and password')