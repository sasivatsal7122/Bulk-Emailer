import streamlit as st
import database as db
import pandas as pd
import streamlit_authenticator as stauth
import json
from datetime import date
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

def dashboard(name):
    st.markdown("<h1 style='color:#f8c121;text-align:center;text-decoration:underline'><tt>Admin Dashboard</tt><h1><br>",unsafe_allow_html=True)
    st.header("Manage Users")
    crud = st.selectbox("",('Show all Users','Add New User','Update User Details','Delete User')) 
    if crud=='Show all Users':
        st.subheader("List of all Users with Login Access")
        result=db.view_all_data()
        new_df=pd.DataFrame(result,columns=["USERNAME","USER-DESIGNATION","USER-EMAIL","PASSWORD",'CLUB'])
        new_df.drop(['CLUB','PASSWORD'], axis=1,inplace=True)
        new_df.index += 1 
        st.dataframe(new_df)
    elif crud=='Add New User':
        st.subheader("Want To Create a New User?")
        col1,col2 = st.columns(2)
        name = col1.text_input("Enter Name :")
        designation = col2.text_input("Enter Designation :")
        email = col1.text_input("Enter Email :")
        password = col2.text_input("Enter password :"); tls = []; tls.append(password)  
        club = st.radio("Belongs to?",('OWASP','VIGNITERS'))
        hashed_password = stauth.Hasher(tls).generate()
        confirm_bt = st.button("Add New User")      
        if confirm_bt:
            db.create_newuser(name,designation,email,hashed_password[0],club)
            st.success("Added ::{} ::To User Record".format(name))
        
    elif crud=='Update User Details':
        st.subheader("Edit USer Record")
        with st.expander("Current Data"):
            result= db.view_all_data()
            new_df=pd.DataFrame(result,columns=["USERNAME","USER-DESIGNATION","USER-EMAIL","PASSWORD",'CLUB'])
            new_df.index += 1 
            st.dataframe(new_df)
        list_of_names = [i[0] for i in db.view_all_data()]
        selected_name =st.selectbox("Select User to be Updated",list_of_names)
        if selected_name:
            select_attribute = st.selectbox("Select Attribute to be Updated",("USERNAME","USER-DESIGNATION","USER-EMAIL","PASSWORD",'CLUB'))
            if select_attribute:
                new_val = st.text_input(f"Enter New {select_attribute}: ")
                update_btn = st.button(f"Update {select_attribute}")
                if update_btn:
                    db.edit_user_data(select_attribute,new_val,selected_name)
                    tdict = dict(zip(["USERNAME","USER-DESIGNATION","USER-EMAIL","PASSWORD",'CLUB'],result[0]))
                    print(tdict)
                    st.success(f"Updated ::{tdict[select_attribute]} ::To {new_val}")
       
    elif crud=='Delete User':
        st.subheader("Delete User Record")
        with st.expander("Current Data"):
            result= db.view_all_data()
            new_df=pd.DataFrame(result,columns=["USERNAME","USER-DESIGNATION","USER-EMAIL","PASSWORD",'CLUB'])
            new_df.index += 1 
            st.dataframe(new_df)
        list_of_names = [i[0] for i in db.view_all_data()]
        selected_name =st.selectbox("Select User to be Updated",list_of_names)
        if selected_name:
            del_btn = st.button("Delete User")
            if del_btn:
                db.delete_user_data(selected_name)
                if selected_name!=None:
                    st.warning("Deleted: '{}' from the record".format(selected_name))
                else:
                    st.error("There is nothing to delete")
                with st.expander("Updated Data"):
                    result= db.view_all_data()
                    new_df=pd.DataFrame(result,columns=["USERNAME","USER-DESIGNATION","USER-EMAIL","PASSWORD",'CLUB'])
                    new_df.index += 1 
                    st.dataframe(new_df)

    st.subheader("Login History")
    logs = db.get_logs()  
    new_df=pd.DataFrame(logs,columns=["LOGGED ON","LOGGED AT",'LOGGED IN BY',"DESIGNATION",'MAILL_COUNT'])
    new_df.drop(['MAILL_COUNT'], axis=1,inplace=True)
    new_df = new_df.iloc[::-1]
    new_df.index += 1 
    st.dataframe(new_df)  
        
    st.subheader("Mailing History")
    logs = db.get_logs()  
    new_df=pd.DataFrame(logs,columns=["SENT ON","SENT AT",'SENT BY',"DESIGNATION",'NO.OF MAILS SENT'])
    new_df.drop(['SENT AT'], axis=1,inplace=True)
    columns_titles = ['SENT ON',"NO.OF MAILS SENT","SENT BY"]
    new_df=new_df.reindex(columns=columns_titles)
    new_df = new_df.iloc[::-1]
    new_df.index += 1 
    st.dataframe(new_df) 
    
    st.subheader("Collected Emails")
    f = open('email_data.json')
    data = json.load(f)
    new_dict = dict(data);today = date.today();cur_date = today.strftime("%B %d, %Y")
    st.text(f"There are Total of {len(new_dict.keys())} Emails collected as of {cur_date}")
    with st.expander("Show Emails"):
        st.json(new_dict)
    excel = {
                'Email': new_dict.keys(),
                'Name': new_dict.values()
    }
    excel = pd.DataFrame(excel)
    @st.cache
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'}) 
        worksheet.set_column('A:A', None, format1)  
        writer.save()
        processed_data = output.getvalue()
        return processed_data
    
    data = to_excel(excel)
    st.download_button(
     label="Download data as EXCEL",
     data=data,
     file_name='emails.xlsx',
     mime='text/csv',
    )
    