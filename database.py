import sqlite3 as sq
from datetime import date
from datetime import datetime
import json

conn = sq.connect('users.db',check_same_thread=False)
c = conn.cursor()


def create_newuser(USERNAME,USER_DESIGNATION,USER_EMAIL,PASS_WORD,CLUB):
    c.execute('INSERT INTO USERS(USERNAME,USER_DESIGNATION,USER_EMAIL, PASS_WORD,CLUB) VALUES (?,?,?,?,?)',
                   (USERNAME,USER_DESIGNATION,USER_EMAIL, PASS_WORD,CLUB))
    conn.commit()

def view_all_data():
    c.execute('SELECT * FROM USERS ')
    data = c.fetchall()
    return data

def edit_user_data(changing_attribute,att1,att2):
    c.execute(f"UPDATE USERS SET {changing_attribute}=? WHERE USERNAME=?",(att1,att2))
    conn.commit()

def delete_user_data(username):
    c.execute('DELETE FROM USERS WHERE USERNAME="{}" '.format(username))
    conn.commit()

def add_log(username,designation,mailcount=0):
    today = date.today()
    current_date = today.strftime("%B %d, %Y")
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    
    c.execute('SELECT USERNAME FROM LOGS WHERE DATE=?',(current_date,))
    data = c.fetchall()
    USER_LOGS_LS = data; USER_LOGS_LS = [item for t in data for item in t] ; 
    
    if username in USER_LOGS_LS:
        c.execute('SELECT MAILL_COUNT FROM LOGS WHERE DATE=? and USERNAME=?',(current_date,username,))
        present_mail_count = c.fetchall(); 
        if len(present_mail_count)>0:
            present_mail_count = present_mail_count[0][0]
        else:
            present_mail_count = 0 
        c.execute(f"UPDATE LOGS SET MAILL_COUNT=? WHERE DATE=? and USERNAME=?",(int(present_mail_count)+mailcount,current_date,username,))
        conn.commit()
    else:
        c.execute('INSERT INTO LOGS(DATE,TIME,USERNAME,DESIGNATION,MAILL_COUNT) VALUES (?,?,?,?,?)',
                   (current_date,current_time,username,designation,mailcount))
        conn.commit()
        
def get_logs():
    c.execute('SELECT * FROM LOGS ')
    logs = c.fetchall()
    return logs
            
def load_json(new_data):
    with open('email_data.json','w') as file:
        json.dump(new_data,file,indent = 4)
        
def get_owasp():
    c.execute('SELECT USERNAME,USER_DESIGNATION FROM USERS WHERE CLUB=?',('OWASP',))
    owaspians = c.fetchall()
    return owaspians

def get_igniters():
    c.execute('SELECT USERNAME,USER_DESIGNATION  FROM USERS WHERE CLUB=?',('IGNITERS',))
    vigniters = c.fetchall()
    return vigniters