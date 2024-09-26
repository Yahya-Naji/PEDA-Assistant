# openai_api.py

import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up your OpenAI API key using the latest OpenAI SDK method
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

# Function to make API calls using the new method
def generate_content(prompt):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # Specify your desired model
        prompt=prompt,
        max_tokens=2000
    )
    return response.choices[0].text.strip()
