import pickle
from pathlib import Path
import streamlit_authenticator as stauth



names=["Sasi Vatsal","Likhith","Lokesh"]
usernames = ["sasivatsal7122@gmail.com","likhithbavisetti@gmail.com",'lokeshwarlakhi@gmail.com']
passwords=["7382117167","9391377120",'79891 04871']


hashed_passwords=stauth.Hasher(passwords).generate()

file_path=Path(__file__).parent/"pkl_creds/pw.pkl"
with file_path.open("wb")as file:
    pickle.dump(hashed_passwords,file)
    
file_path=Path(__file__).parent/"pkl_creds/usernames.pkl"
with file_path.open("wb")as file:
    pickle.dump(usernames,file)
    
file_path=Path(__file__).parent/"pkl_creds/names.pkl"
with file_path.open("wb")as file:
    pickle.dump(names,file)