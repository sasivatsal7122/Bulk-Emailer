import pickle
from pathlib import Path
import streamlit_authenticator as stauth



def auth_driver(club,names_ls,usernames_ls,passwords_ls,designation_ls):
    hashed_passwords=stauth.Hasher(passwords_ls).generate()
    file_path=Path(__file__).parent/f"pkl_creds/{club}_pw.pkl"
    with file_path.open("wb")as file:
        pickle.dump(hashed_passwords,file)
        
    file_path=Path(__file__).parent/f"pkl_creds/{club}_usernames.pkl"
    with file_path.open("wb")as file:
        pickle.dump(usernames_ls,file)
        
    file_path=Path(__file__).parent/f"pkl_creds/{club}_names.pkl"
    with file_path.open("wb")as file:
        pickle.dump(names_ls,file)
        
    designation_ls = dict(zip(names_ls,designation_ls))
    
    file_path=Path(__file__).parent/f"pkl_creds/{club}_designation.pkl"
    with file_path.open("wb")as file:
        pickle.dump(designation_ls,file)


owasp_names=["Sasi Vatsal","Likhith","Lokesh"]
owasp_usernames = ["sasivatsal7122@gmail.com","likhithbavisetti@gmail.com",'lokeshwarlakhi@gmail.com']
owasp_passwords=["7382117167","9391377120",'7989104871']
owasp_designation = ['Chief Secretary','Vice Secretary','Associate Secretary']

vigniters_names=["Sasi Vatsal"]
vigniters_usernames = ["sasivatsal7122@gmail.com"]
vigniters_passwords=["7382117167"]
vigniters_designation = ['Chief Igniter']

if __name__=='__main__':
    auth_driver(club='OWASP_VIIT',names_ls=owasp_names,usernames_ls=owasp_usernames,passwords_ls=owasp_passwords,designation_ls=owasp_designation)
    auth_driver(club='VIGNITERS',names_ls=vigniters_names,usernames_ls=vigniters_usernames,passwords_ls=vigniters_passwords,designation_ls=vigniters_designation)
