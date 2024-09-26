# openai_api.py

import openai
import streamlit as st  # Import Streamlit to use secrets

# Set up OpenAI API key using Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to make API calls using the new method
def generate_content(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",  # Specify your desired model
        prompt=prompt,
        max_tokens=2000
    )
    return response.choices[0].text.strip()
