import streamlit as st
import pandas as pd
import datetime
import os

# File path for the CSV file
csv_file = 'mood_history.csv'

# Function to load the data
def load_data(): 
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame(columns=['date', 'mood', 'note'])

# Function to save the data
def save_data(mood_df):
    mood_df.to_csv(csv_file, index=False)

# Mood Tracker Function
def mood_tracker():
    # Load existing data
    mood_df = load_data()

    # Title
    st.title('Mood Tracker')

    # Mood Input
    st.subheader('How are you feeling today?')

    # User selects their mood
    mood = st.selectbox('Select your mood:', ['Happy', 'Sad', 'Anxious', 'Excited', 'Neutral'])

    # Optionally add a note
    note = st.text_area('Add a note (optional):')

    # Record the mood with date and time
    if st.button('Submit'):
        new_entry = {
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'mood': mood,
            'note': note
        }

        # Create a DataFrame for the new entry
        new_entry_df = pd.DataFrame([new_entry])

        # Concatenate the new entry to the existing DataFrame
        mood_df = pd.concat([mood_df, new_entry_df], ignore_index=True)
        
        st.success('Mood logged!')

    # Display past moods
    st.subheader('Mood History')
    st.dataframe(mood_df)

    # Line Graph Section
    st.subheader('Mood Over Time')

    # Convert 'date' column to datetime
    mood_df['date'] = pd.to_datetime(mood_df['date'])

    # Plot line graph of mood trends
    if not mood_df.empty:
        # Map moods to numbers for graphing
        mood_mapping = {'Happy': 5, 'Excited': 4, 'Neutral': 3, 'Anxious': 2, 'Sad': 1}
        mood_df['mood_score'] = mood_df['mood'].map(mood_mapping)

        # Plot the mood over time using Streamlit's line chart
        st.line_chart(mood_df.set_index('date')['mood_score'])

    # Download data as CSV
    if st.button('Download History as CSV'):
        st.download_button(
            label="Download mood history as CSV",
            data=mood_df.to_csv(index=False).encode('utf-8'),
            file_name='mood_history.csv',
            mime='text/csv',
        )
