import streamlit as st
from firebase import initialize_firebase
from firebase.auth import sign_up, login

initialize_firebase()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_form():
    st.header("Login")
    email = st.text_input("Email", key="login_email")  # Unique key
    password = st.text_input("Password", type="password", key="login_password")  # Unique key
    
    if st.button("Login"):
        response = login(email, password)
        if response is not None:
            if response["success"]:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(response["message"])
            else:
                st.error(response["message"])

def signup_form():
    st.header("Sign Up")
    email = st.text_input("Email", key="signup_email")  # Unique key
    password = st.text_input("Password", type="password", key="signup_password")  # Unique key
    
    if st.button("Sign Up"):
        response = sign_up(email, password)
        if response is not None:
            if response["success"]:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success(response["message"])
            else:
                st.error(response["message"])

def dashboard():
    st.header("Dashboard")
    st.write(f"Welcome, {st.session_state.user_email}!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.success("You have been logged out.")
        st.experimental_rerun()

if st.session_state.logged_in:
    dashboard()  
else:
    login_form() 
    signup_form() 
