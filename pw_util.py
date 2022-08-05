import pickle
from pathlib import Path
import streamlit_authenticator as stauth



def auth_driver(names_ls,usernames_ls,passwords_ls):
    hashed_passwords=stauth.Hasher(passwords_ls).generate()
    file_path=Path(__file__).parent/f"pkl_creds/pw.pkl"
    with file_path.open("wb")as file:
        pickle.dump(hashed_passwords,file)
        
    file_path=Path(__file__).parent/f"pkl_creds/usernames.pkl"
    with file_path.open("wb")as file:
        pickle.dump(usernames_ls,file)
        
    file_path=Path(__file__).parent/f"pkl_creds/names.pkl"
    with file_path.open("wb")as file:
        pickle.dump(names_ls,file)
        

if __name__=='__main__':
    owasp_names=["Sasi Vatsal","Likhith","Lokesh"]
    owasp_usernames = ["sasivatsal7122@gmail.com","likhithbavisetti@gmail.com",'lokeshwarlakhi@gmail.com']
    owasp_passwords=["7382117167","9391377120",'7989104871']
    owasp_designation = ['Chief Secretary','Vice Secretary','Associate Secretary']

    vigniters_names=["Sasi Vatsal"]
    vigniters_usernames = ["sasivatsal7122@gmail.com"]
    vigniters_passwords=["7382117167"]
    vigniters_designation = ['Chief Igniter']
    
    c_names = owasp_names+vigniters_names
    c_usernames = owasp_usernames+vigniters_usernames
    c_passwords = owasp_passwords+vigniters_passwords
    
    auth_driver(names_ls=c_names,usernames_ls=c_usernames,passwords_ls=c_passwords)
    
    owasp_designation_ls = dict(zip(owasp_names,owasp_designation))
    
    file_path=Path(__file__).parent/f"pkl_creds/OWASP_VIIT_designation.pkl"
    with file_path.open("wb")as file:
        pickle.dump(owasp_designation_ls,file)
        
    vigniters_designation_ls = dict(zip(vigniters_names,vigniters_designation))
    
    file_path=Path(__file__).parent/f"pkl_creds/VIGNITERS_designation.pkl"
    with file_path.open("wb")as file:
        pickle.dump(vigniters_designation_ls,file)