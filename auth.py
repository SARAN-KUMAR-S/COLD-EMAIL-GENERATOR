import sqlite3
import streamlit as st

# Database Setup
def initialize_db():
    conn = sqlite3.connect('form.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coldmailusers (
            USERNAME TEXT(50) UNIQUE,
            PASSWORD TEXT(50)
        )
    """)
    conn.commit()
    return conn, cursor

def authentication_page(cursor, conn):
    st.title("User Authentication")
    tabs = st.tabs([":rainbow[Login]", ":rainbow[New User]"])

    # Login tab
    with tabs[0]:
        st.header("Login")
        with st.form(key="login_form"):
            username = st.text_input("Enter Username")
            password = st.text_input("Enter Password", type="password")
            login = st.form_submit_button("LOGIN")

            if login:
                cursor.execute("SELECT * FROM coldmailusers WHERE USERNAME=? AND PASSWORD=?", (username, password))
                user = cursor.fetchone()
                if user:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success(f"Welcome back, {username}!")
                else:
                    st.error("Invalid username or password.")

    # New User Registration tab
    with tabs[1]:
        st.header("New User Registration")
        with st.form(key="register_form"):
            username = st.text_input("Choose a Username")
            password = st.text_input("Choose a Password", type="password")
            register = st.form_submit_button("REGISTER")

            if register:
                try:
                    cursor.execute("INSERT INTO coldmailusers (USERNAME, PASSWORD) VALUES (?, ?)", (username, password))
                    conn.commit()
                    st.success("Registration successful! You can now log in.")
                except sqlite3.IntegrityError:
                    st.error("Username already exists. Please choose a different one.")
