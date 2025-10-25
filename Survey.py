# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="👩‍💻",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Screen Time Survey")
st.write("Track your daily phone usage and how it affects your focus and mood!")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    name_input = st.text_input("Enter your name:")
    screen_time = st.number_input("How many hours did you spend on your phone today?", min_value=0.0, step=0.5)
    focus_level = st.slider("How focused did you feel today? (1 = not focused, 10 = very focused)", 1, 10, 5)
    mood_input = st.selectbox("How was your mood today?", ["Tired", "Okay", "Happy", "Sad", "Angry"])
    productivity = st.slider("How productive did you feel today? (1–10)", 1, 10, 5)

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # Create a new row of data from the form inputs
        new_row = {
            "Name": name_input,
            "ScreenTimeHours": screen_time,
            "FocusLevel": focus_level,
            "Mood": mood_input,
            "ProductivityLevel": productivity
        }

        import csv
        import os
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data.csv")
        with open(csv_path, "a", newline="") as f:

            writer = csv.DictWriter(f, fieldnames=new_row.keys())
            if f.tell() == 0:         
                writer.writeheader()
            writer.writerow(new_row)

    st.success("Your data has been saved!")
    st.write(f"****{name_input}** spent **{screen_time} hours** on their phone, felt **{focus_level}/10 focused**, rated their productivity **{productivity}/10**, and was **{mood_input}** today.")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
