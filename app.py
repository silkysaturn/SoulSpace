import streamlit as st
from firebase import initialize_firebase
from firebase.auth import sign_up, login
from mt import mood_tracker  
from survey import survey_form

# Initialize Firebase
initialize_firebase()

# Custom CSS to change font family
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;  /* Change to your preferred font */
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login" 

if "user_email" not in st.session_state:
    st.session_state.user_email = None 

# Login form
def login_form():
    st.header("Login")
    email = st.text_input("Email", key="login_email")  # Unique key for email input
    password = st.text_input("Password", type="password", key="login_password")  # Unique key for password input
    
    if st.button("Login"):
        response = login(email, password)
        if response is not None:
            if response["success"]:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.page = "dashboard"  # Navigate to dashboard
                st.success(response["message"])
            else:
                st.error(response["message"])
    
    # Button to switch to sign-up
    if st.button("Don't have an account? Sign Up"):
        st.session_state.page = "signup"  # Switch to signup page

# Signup form
def signup_form():
    st.header("Sign Up")
    email = st.text_input("Email", key="signup_email")  # Unique key for email input
    password = st.text_input("Password", type="password", key="signup_password")  # Unique key for password input
    
    if st.button("Sign Up"):
        response = sign_up(email, password)
        if response is not None:
            if response["success"]:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.page = "dashboard"  # Navigate to dashboard
                st.success(response["message"])
            else:
                st.error(response["message"])

    # Button to switch back to login
    if st.button("Already have an account? Log In"):
        st.session_state.page = "login"  # Switch to login page

# Dashboard
def dashboard():
    st.markdown("<h1 style='text-align: center;'>Welcome to SoulSpace🚀</h1>", unsafe_allow_html=True)

    # Alert for the survey
    st.warning("Please complete the survey before you can chat with anybody.")
    
    # Centered content
    st.write(f"You are worthy of happiness and peace of mind.")

    # Create two columns for navigation buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Go to Mood Tracker"):
            st.session_state.page = "mood_tracker"  # Navigate to Mood Tracker

    with col2:
        if st.button("Complete Survey"):
            st.session_state.page = "survey"  # Navigate to Survey

    # Resources section
    st.subheader("Resources")
    st.write("- **[Crisis Text Line](https://www.crisistextline.org/)**")
    st.write("- **[Veterans Crisis Line](https://www.veteranscrisisline.net/)**")
    st.write("- **[Child Abuse Hotline](https://www.childhelp.org/hotline/)**")
    st.write("- **[National Sexual Assault Hotline](https://rainn.org/)**")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.session_state.page = "login"  # Reset to login page
        st.success("You have been logged out.")

# Main logic to handle navigation and page rendering
if st.session_state.logged_in:
    if st.session_state.page == "dashboard":
        dashboard()  # Call the dashboard function
    elif st.session_state.page == "mood_tracker":
        mood_tracker()  # Call the mood tracker function
    elif st.session_state.page == "survey":
        survey_form()  # Call the survey form function
else:
    if st.session_state.page == "login":
        login_form()  # Show the login form
    else:
        signup_form()  # Show the signup form
