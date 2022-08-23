import sqlite3 as sq


def create_newuser(USERNAME,USER_DESIGNATION,USER_EMAIL,PASS_WORD):
    conn = sq.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO USERS(USERNAME,USER_DESIGNATION,USER_EMAIL, PASS_WORD) VALUES (?,?,?,?)',
                   (USERNAME,USER_DESIGNATION,USER_EMAIL, PASS_WORD))
    conn.commit()
    conn.close()


def view_all_data():
    conn = sq.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('SELECT * FROM USERS ')
    data = c.fetchall()
    return data


def edit_user_data(changing_attribute,att1,att2):
    conn = sq.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute(f"UPDATE USERS SET {changing_attribute}=? WHERE USERNAME=?",(att1,att2))
    conn.commit()

def delete_user_data(username):
    conn = sq.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('DELETE FROM USERS WHERE USERNAME="{}" '.format(username))
    conn.commit()
