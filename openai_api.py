# openai_api.py

import openai
import streamlit as st  # Import Streamlit to use secrets

# Set up OpenAI API key using Streamlit secrets
client = openai.Client(api_key=st.secrets["OPENAI_API_KEY"])

# Function to make API calls using the new method
def generate_content(prompt):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Specify your desired model
        prompt=prompt,
        max_tokens=2000
    )
    return response.choices[0].text.strip()
