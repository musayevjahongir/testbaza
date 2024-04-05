import sqlite3
def get_admins():
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute("SELECT username FROM Admins")
    chat_ids = cursor.fetchall()
    cnt.close()
    return chat_ids
def add_admin(username:str):
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""INSERT INTO Admins (username) VALUES ("{username}")""")
    cnt.commit()
    cnt.close()
    return True
def del_admin(username:str):
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""DELETE FROM Admins WHERE username = ("{username}")""")
    cnt.commit()
    cnt.close()
    return True
def del_user(chat_id:str):
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""DELETE FROM Users WHERE chat_id = ("{chat_id}")""")
    cnt.commit()
    cnt.close()
    return True

def get_channel():
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute("SELECT name FROM Obuna")
    channels = cursor.fetchall()
    cnt.close()
    return channels

def check_chennel(chat_id: str)->list:
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""SELECT * FROM Obuna WHERE name = ("{chat_id}")""")
    a=cursor.fetchall()
    cnt.close()
    return a

def get_users():
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute("SELECT chat_id FROM Users")
    chat_ids = cursor.fetchall()
    cnt.close()
    return chat_ids
def add_channel(name:str):
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""INSERT INTO Obuna (name) VALUES ("{name}")""")
    cnt.commit()
    chat_ids = cursor.fetchall()
    cnt.close()
    return chat_ids

def del_obuna(name:str):
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""DELETE FROM Obuna WHERE name = ("{name}")""")
    cnt.commit()
    chat_ids = cursor.fetchall()
    cnt.close()
    return chat_ids

def add_user(chat_id: str)->bool:
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""INSERT INTO Users (chat_id) VALUES ("{chat_id}")""")
    cnt.commit()
    cnt.close()
    return True
def check_admin(username: str)->list:
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f'SELECT * FROM Admins WHERE username = "{username}"')
    a=cursor.fetchall()
    print(username)
    cnt.close()
    return a
def check_user(chat_id: str)->list:
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f'SELECT * FROM Users WHERE chat_id = "{chat_id}"')
    a=cursor.fetchall()
    cnt.close()
    return a
# print(type((get_channel())[0]))