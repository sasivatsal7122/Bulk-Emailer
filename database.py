import sqlite3 as sq
from datetime import date
from datetime import datetime


conn = sq.connect('users.db',check_same_thread=False)
c = conn.cursor()


def create_newuser(USERNAME,USER_DESIGNATION,USER_EMAIL,PASS_WORD):
    c.execute('INSERT INTO USERS(USERNAME,USER_DESIGNATION,USER_EMAIL, PASS_WORD) VALUES (?,?,?,?)',
                   (USERNAME,USER_DESIGNATION,USER_EMAIL, PASS_WORD))
    conn.commit()
    conn.close()


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
    
    c.execute('SELECT DATE FROM LOGS')
    data = c.fetchall()
    DATE_LOGS_LS = [data[0] for i in data];datelogs=[]
    for i in DATE_LOGS_LS:
        datelogs.append(i[0])
    if current_date in datelogs:
        c.execute('SELECT MAILL_COUNT FROM LOGS WHERE DATE=?',(current_date,))
        present_mail_count = c.fetchall(); present_mail_count = present_mail_count[0][0]
        c.execute(f"UPDATE LOGS SET MAILL_COUNT=? WHERE DATE=?",(int(present_mail_count)+mailcount,current_date))
        conn.commit()
    else:
        c.execute('INSERT INTO LOGS(DATE,TIME,USERNAME,DESIGNATION,MAILL_COUNT) VALUES (?,?,?,?,?)',
                   (current_date,current_time,username,designation,mailcount))
        conn.commit()
            