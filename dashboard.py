import streamlit as st

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
