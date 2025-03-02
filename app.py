import streamlit as st
import sqlite3
import bcrypt

# Helper functions for database operations
def create_connection():
    db_path = st.secrets["database"]["name"]
    return sqlite3.connect(db_path)

def register_user(username, name, password):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    try:
        cursor.execute('INSERT INTO users (username, name, password_hash) VALUES (?, ?, ?);',
                       (username, name, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def verify_login(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    data = cursor.fetchone()
    conn.close()
    if data:
        password_hash = data[0]
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    return False

def get_user_name(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM users WHERE username = ?', (username,))
    data = cursor.fetchone()
    conn.close()
    return data[0] if data else None

def reset_password(username, new_password):
    conn = create_connection()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    cursor.execute('UPDATE users SET password_hash = ? WHERE username = ?', (hashed_password, username))
    conn.commit()
    conn.close()

# Streamlit UI
st.title('User Authentication System')

menu = st.sidebar.selectbox('Menu', ['Login', 'Register', 'Reset Password'])

if menu == 'Register':
    st.subheader('Register New User')
    new_username = st.text_input("Choose a username", key="new_user")
    new_name = st.text_input("Enter your name", key="new_name")
    new_password = st.text_input("Choose a password", type='password', key="new_password")
    if st.button('Register'):
        if register_user(new_username, new_name, new_password):
            st.success('You are successfully registered!')
        else:
            st.error('Registration failed (username may already exist)')

elif menu == 'Login':
    st.subheader('Login')
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button('Login'):
        if verify_login(username, password):
            user_name = get_user_name(username)
            st.success(f'Welcome {user_name}!')
        else:
            st.error('Incorrect username or password')

elif menu == 'Reset Password':
    st.subheader('Reset Password')
    reset_username = st.text_input("Your Username", key="reset_user")
    new_password = st.text_input("Your New Password", type='password', key="reset_pass")
    if st.button('Reset Password'):
        reset_password(reset_username, new_password)
        st.success('Password has been reset successfully')

