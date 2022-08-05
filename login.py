import streamlit as st
import streamlit_authenticator as stauth
import pickle
from pathlib import Path

# local imports
import dashboard

def run_login():
    st.set_page_config(page_title="Bulk Club Mailer",page_icon="📨")
    file_path = Path(__file__).parent/"pkl_creds/pw.pkl"
    with file_path.open("rb")as file:
        hashed_passwords=pickle.load(file)
        
    file_path = Path(__file__).parent/"pkl_creds/usernames.pkl"
    with file_path.open("rb")as file:
        usernames=pickle.load(file)
        
    file_path = Path(__file__).parent/"pkl_creds/names.pkl"
    with file_path.open("rb")as file:
        names=pickle.load(file)
    
    authenticator = stauth.Authenticate(names,usernames,hashed_passwords,cookie_name='s',key='j')
    name,authentication_status,username=authenticator.login("Login","main")

    if authentication_status:
        authenticator.logout('Logout', 'sidebar')
        dashboard.main(name)
        
    elif authentication_status == False:
        st.error('Username/password is incorrect')
        

    elif authentication_status == None:
        st.warning('Please enter your username and password')