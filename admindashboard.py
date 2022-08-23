import streamlit as st
import database as db
import pandas as pd
import streamlit_authenticator as stauth

def dashboard(name):
    st.title(f"Admin Dashboard")
    crud = st.selectbox("",('Read','Create','Update','Delete'))
    
    if crud=='Read':
        st.subheader("List of all Users with Login Access")
        result=db.view_all_data()
        new_df=pd.DataFrame(result,columns=["USERNAME","USER-DESIGNATION","USER-EMAIL","PASSWORD"])
        new_df.index += 1 
        st.dataframe(new_df)
    elif crud=='Create':
        st.subheader("Want To Create a New User?")
        col1,col2 = st.columns(2)
        name = col1.text_input("Enter Name :")
        designation = col2.text_input("Enter Designation :")
        email = col1.text_input("Enter Email :")
        password = col2.text_input("Enter password :"); tls = []; tls.append(password)  
        hashed_password = stauth.Hasher(tls).generate()
        confirm_bt = st.button("Add New User")      
        if confirm_bt:
            db.create_newuser(name,designation,email,hashed_password[0])
            st.success("Added ::{} ::To User Record".format(name))
        
    elif crud=='Update':
        st.subheader("Edit USer Record")
        with st.expander("Current Data"):
            result= db.view_all_data()
            new_df=pd.DataFrame(result,columns=["USERNAME","USER-DESIGNATION","USER-EMAIL","PASSWORD"])
            new_df.index += 1 
            st.dataframe(new_df)
        list_of_names = [i[0] for i in db.view_all_data()]
        selected_name =st.selectbox("Select User to be Updated",list_of_names)
        if selected_name:
            select_attribute = st.selectbox("Select Attribute to be Updated",("USERNAME","USER_DESIGNATION","USER-EMAIL","PASS_WORD"))
            if select_attribute:
                new_val = st.text_input("Enter New Value: ")
                update_btn = st.button("Update the Value")
                if update_btn:
                    db.edit_user_data(select_attribute,new_val,selected_name)
                    tdict = dict(zip(["USERNAME","USER_DESIGNATION","USER-EMAIL","PASS_WORD"],result[0]))
                    print(tdict)
                    st.success(f"Updated ::{tdict[select_attribute]} ::To {new_val}")
       
    elif crud=='Delete':
        st.subheader("Delete User Record")
        with st.expander("Current Data"):
            result= db.view_all_data()
            new_df=pd.DataFrame(result,columns=["USERNAME","USER-DESIGNATION","USER-EMAIL","PASSWORD"])
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
                    new_df=pd.DataFrame(result,columns=["USERNAME","USER-DESIGNATION","USER-EMAIL","PASSWORD"])
                    new_df.index += 1 
                    st.dataframe(new_df)
    