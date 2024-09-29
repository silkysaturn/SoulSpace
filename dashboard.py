import streamlit as st

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
                # Add button to start chat with each pair
                if st.button(f"Chat with {pair[1][0]} {pair[1][1]}"):
                    start_chat(pair)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_email = None
        st.success("You have been logged out.")

def start_chat(pair):
    st.session_state.chat_with = pair  # Store the pair in session state
    st.session_state.page = "chat"  # Navigate to chat page

def chat_page():
    if "chat_with" in st.session_state:
        user1, user2 = st.session_state.chat_with
        st.header(f"Chat with {user2[0]} {user2[1]}")
        
        chat_id = f"{user1[0]}_{user1[1]}_{user2[0]}_{user2[1]}"
        messages_ref = db.collection("chats").document(chat_id).collection("messages")
        
        # Display chat messages
        messages = messages_ref.order_by("timestamp").stream()
        for msg in messages:
            msg_data = msg.to_dict()
            st.write(f"{msg_data['sender']}: {msg_data['text']}")

        # Message input
        message_text = st.text_input("Type your message...")
        if st.button("Send"):
            # Send message to Firestore
            messages_ref.add({
                "sender": user1[0],  # Adjust as per the logged-in user
                "text": message_text,
                "timestamp": firestore.SERVER_TIMESTAMP,
            })
            st.experimental_rerun()  # Refresh the page to see the new message

def main():
    # Create a centered layout
    st.markdown("<h1 style='text-align: center;'>Dashboard</h1>", unsafe_allow_html=True)

    # Alert at the top of the page for the survey
    st.warning("Please complete the survey before you can chat with anybody.")

    # Center the content
    center_column = st.container()
    with center_column:
        st.write("Welcome to SoulSpace!")

        # Create two columns for buttons
        col1, col2 = st.columns(2)

        with col1:
            # Button to navigate to the Mood Tracker
            if st.button("Go to Mood Tracker"):
                st.session_state.page = "mood_tracker"  # Set page to mood tracker

        with col2:
            # Button to navigate to the Survey
            if st.button("Complete Survey"):
                st.session_state.page = "survey"  # Set page to survey


if __name__ == "__main__":
    main()
