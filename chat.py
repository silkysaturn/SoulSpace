import streamlit as st

def chat_interface():

    if "user_name" not in st.session_state:
        st.session_state["user_name"] = "User A"
    # Chat interface
    
    st.title("Chat Interface")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input, allowing for single user input
    if prompt := st.chat_input("Type your message (just use 'User A'):"):
        # Add message to chat history with the fixed user identifier
        user_message = f"{st.session_state.user_name}: {prompt}"
        st.session_state.messages.append({"role": st.session_state.user_name, "content": user_message})
        
        # Display user message in chat message container
        with st.chat_message(st.session_state.user_name):
            st.markdown(user_message)


if __name__ == "__main__":
    chat_interface()

