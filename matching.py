import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from sklearn.cluster import KMeans
from firebase_admin import auth, credentials, initialize_app
import firebase_admin

# Initialize Firebase
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(".gitignore/serviceAccountKey.json")
        initialize_app(cred)
# Firebase Authentication functions
def sign_up(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return {"success": True, "message": "User created successfully!", "user": user}
    except Exception as e:  # Define 'e' here to catch the exception
        return {"success": False, "message": f"Error creating user: {e}"}


def login(email, password):
    try:
        user = auth.get_user_by_email(email)
        return {"success": True, "message": f"Welcome back, {user.email}!", "user": user}
    except Exception as e:
        return {"success": False, "message": f"Login failed: {e}"}

# Load and process user data
def load_user_data(file):
    df_original = pd.read_csv(file)
    
    if df_original.empty:
        st.warning("No user data found in the CSV.")
        return None
    
    df_n = df_original.drop(columns=['first_name', 'last_name', 'pronouns', 'gender'])

    if df_n.empty:
        st.warning("No numeric data for clustering.")
        return None

    n_clusters = max(1, len(df_original) // 2)  # At least 1 cluster for every two users
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df_n['Cluster'] = kmeans.fit_predict(df_n)

    df_clustered = df_n.join(df_original[['first_name', 'last_name']], how='inner')

    return df_clustered

# Create pairs based on clustering
def create_pairs(df_clustered):
    final_pairs = []
    existing_pairs = set()

    for cluster in df_clustered['Cluster'].unique():
        users_in_cluster = df_clustered[df_clustered['Cluster'] == cluster]
        names = users_in_cluster[['first_name', 'last_name']].values.tolist()
        np.random.shuffle(names)

        for i in range(0, len(names) - 1, 2):
            user1 = names[i]
            user2 = names[i + 1]

            if user1 != user2:
                pair = (tuple(user1), tuple(user2))
                if pair not in existing_pairs and (pair[1], pair[0]) not in existing_pairs:
                    final_pairs.append(pair)
                    existing_pairs.add(pair)

        if len(names) % 2 == 1:
            final_pairs.append((tuple(names[-1]), ("No Pair", "No Pair")))

    return final_pairs

# Store pairs in SQLite database
def store_pairs_in_db(pairs):
    conn = sqlite3.connect('user_pairs.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_pairs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user1_first TEXT NOT NULL,
        user1_last TEXT NOT NULL,
        user2_first TEXT NOT NULL,
        user2_last TEXT NOT NULL
    )
    ''')

    for pair in pairs:
        user1 = pair[0]
        user2 = pair[1]
        
        cursor.execute('''
        INSERT INTO user_pairs (user1_first, user1_last, user2_first, user2_last)
        VALUES (?, ?, ?, ?)
        ''', (user1[0], user1[1], user2[0], user2[1]))

    conn.commit()
    conn.close()

# Login and Sign up form
def login_form():
    st.header("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        response = login(email, password)
        if response and response["success"]:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success(response["message"])
        else:
            st.error(response["message"])

def signup_form():
    st.header("Sign Up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        response = sign_up(email, password)
        if response and response["success"]:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success(response["message"])
        else:
            st.error(response["message"])

# Dashboard after login
def dashboard():
    st.header("Dashboard")
    st.write(f"Welcome, {st.session_state.user_email}!")
    
    # CSV file uploader for user matching
    uploaded_file = st.file_uploader("Upload CSV file with survey responses", type=["csv"])
    if uploaded_file:
        st.success("File uploaded successfully!")
        df_clustered = load_user_data(uploaded_file)
        
        if df_clustered is not None:
            final_pairs = create_pairs(df_clustered)
            st.subheader("Generated Pairs:")
            for pair in final_pairs:
                st.write(f"{pair[0][0]} {pair[0][1]} paired with {pair[1][0]} {pair[1][1]}")
            store_pairs_in_db(final_pairs)
            st.success("Pairs stored in the database successfully!")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.success("You have been logged out.")

# Streamlit app
def main():
    initialize_firebase()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        dashboard()
    else:
        login_form()
        signup_form()

if __name__ == "__main__":
    main()
