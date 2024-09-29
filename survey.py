import streamlit as st
import pandas as pd
import os

# File path for storing survey responses
csv_file = 'soulspace_survey_responses.csv'

def create_csv_file():
    # Check if CSV exists, if not, create it with the appropriate columns
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=[
            'first_name', 'last_name', 'age', 'pronouns', 'gender', 'email', 
            'traveling', 'animals', 'reading', 'sports', 'cooking', 'music', 'art', 'gaming', 
            'technology', 'fitness', 'nature', 'mental_health', 
            'ADHD', 'depression', 'anxiety', 'stress', 'PTSD', 
            'self_esteem', 'other_mental_health'
        ])
        df.to_csv(csv_file, index=False)

def boolean_converter(choices, options):
    return {option: (option in choices) for option in options}

def survey_form():
    create_csv_file()

    # Survey form
    st.title("SoulSpace Survey")

    with st.form("survey_form"):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        pronouns = st.selectbox("Pronouns", ["he/him", "she/her", "they/them", "other"])
        gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Other"])
        email = st.text_input("Email")  

        # Interests selection
        interests = st.multiselect(
            "Select your interests (choose many):",
            options=[
                "Traveling", "Animals", "Reading", "Sports", "Cooking", 
                "Music", "Art", "Gaming", "Technology", "Fitness", 
                "Nature", "Mental Health"
            ]
        )

        # Mental health topics selection
        mental_health_topics = st.multiselect(
            "Select mental health topics you want to discuss (choose many):",
            options=[
                "ADHD", "Depression", "Anxiety", "Stress", 
                "PTSD", "Self-Esteem", "Other Mental Health Issues"
            ]
        )

        # Convert selected interests and topics to boolean
        interests_boolean = boolean_converter(interests, [
            "Traveling", "Animals", "Reading", "Sports", "Cooking", 
            "Music", "Art", "Gaming", "Technology", "Fitness", 
            "Nature", "Mental Health"
        ])
        
        topics_boolean = boolean_converter(mental_health_topics, [
            "ADHD", "Depression", "Anxiety", "Stress", 
            "PTSD", "Self-Esteem", "Other Mental Health Issues"
        ])

        # Prepare values for insertion
        values_to_insert = [
            first_name if first_name else None,  # Set None for empty first_name
            last_name if last_name else None,    # Set None for empty last_name
            age if age else None,                # Set None for empty age
            pronouns,                            # Keep pronouns as is
            gender,                              # Keep gender as is
            email if email else None,            # Set None for empty email
            interests_boolean.get("Traveling", False), 
            interests_boolean.get("Animals", False),
            interests_boolean.get("Reading", False), 
            interests_boolean.get("Sports", False),
            interests_boolean.get("Cooking", False), 
            interests_boolean.get("Music", False),
            interests_boolean.get("Art", False), 
            interests_boolean.get("Gaming", False),
            interests_boolean.get("Technology", False), 
            interests_boolean.get("Fitness", False),
            interests_boolean.get("Nature", False), 
            interests_boolean.get("Mental Health", False),
            topics_boolean.get("ADHD", False), 
            topics_boolean.get("Depression", False),
            topics_boolean.get("Anxiety", False), 
            topics_boolean.get("Stress", False),
            topics_boolean.get("PTSD", False), 
            topics_boolean.get("Self-Esteem", False),
            topics_boolean.get("Other Mental Health Issues", False)
        ]

        # Submit button
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Load existing data into a DataFrame
            df = pd.read_csv(csv_file)

            # Create a new DataFrame from the current submission
            new_data = pd.DataFrame([values_to_insert], columns=df.columns)

            # Append the new data to the existing DataFrame
            df = pd.concat([df, new_data], ignore_index=True)

            # Save back to CSV
            df.to_csv(csv_file, index=False)

            st.success("Your response has been recorded!")

if __name__ == "__main__":
    survey_form()
