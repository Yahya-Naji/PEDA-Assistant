import streamlit as st
from gtts import gTTS
import os
from io import BytesIO
from main import get_chapters_for_grade_subject, create_prompt
from openai_api import generate_content

# Set Streamlit page configuration
st.set_page_config(page_title="PEDAssistant: Empowering Education Excellence", layout="wide")

# Custom CSS for theme styling with improved mobile responsiveness
st.markdown("""
    <style>
    /* General background color */
    .stApp {
        background-color: white;
    }

    /* Header Styling */
    h1, h2, h3, h4, h5, h6 {
        color: #8C001A;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 8px 0;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #F4B400;
    }

    /* Button styling */
    div.stButton > button {
        background-color: #8C001A;
        color: white;
        border: none;
        padding: 12px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        width: 100%;
        margin: 10px 0;
    }
    div.stButton > button:hover {
        background-color: #AA1E2D;
        color: white;
    }

    /* Radio button styling */
    .stRadio > label {
        font-weight: bold;
        color: #8C001A;
    }

    /* Footer styling */
    hr {
        border: 1px solid #8C001A;
    }

    .footer {
        color: #8C001A;
        font-size: 14px;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Mobile-specific styles */
    @media only screen and (max-width: 600px) {
        h1 { font-size: 22px !important; }
        h2 { font-size: 20px !important; }
        h3 { font-size: 18px !important; }
        div.stButton > button {
            padding: 10px 12px;
            font-size: 14px;
            border-radius: 6px;
        }
        .stRadio > label { font-size: 14px; }
        .css-18e3th9 {
            padding: 1rem 0.5rem 2rem 0.5rem !important;
        }
        .block-container { margin: auto; padding: 0 1rem; }
        [data-testid="stSidebar"] { padding: 1rem; }
        .footer { font-size: 12px; }
        .stRadio { margin-bottom: 1rem; }
        .stTextInput > div > input { padding: 10px; font-size: 14px; }
    }
    @media only screen and (min-width: 600px) {
        .block-container { padding-left: 2rem; padding-right: 2rem; }
    }
    </style>
""", unsafe_allow_html=True)

# Function to convert text to speech and return the audio file
def text_to_speech(text):
    tts = gTTS(text)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

# App title
st.title("PEDAssistant: Empowering Education Excellence")

# Sidebar for grade and subject selection
st.sidebar.header("Grade and Subject Selection")
selected_grade = st.sidebar.selectbox("Choose a Grade", ["Grade 7", "Grade 8", "Grade 9"], key="selected_grade")
selected_subject = st.sidebar.selectbox("Choose a Subject", ["Math", "Physics", "Chemistry", "Biology"], key="selected_subject")

# Retrieve chapters based on grade and subject
chapters = get_chapters_for_grade_subject(selected_grade, selected_subject)
selected_chapter = st.sidebar.selectbox("Choose a Chapter", chapters, key="selected_chapter")

# Clear the session state messages if grade, subject, or chapter changes
if "last_selection" not in st.session_state:
    st.session_state.last_selection = {"grade": selected_grade, "subject": selected_subject, "chapter": selected_chapter}

if (selected_grade != st.session_state.last_selection["grade"] or 
    selected_subject != st.session_state.last_selection["subject"] or 
    selected_chapter != st.session_state.last_selection["chapter"]):
    
    # Reset chat history when any selection changes
    st.session_state.messages = []
    st.session_state.show_chat = False
    st.session_state.last_selection = {"grade": selected_grade, "subject": selected_subject, "chapter": selected_chapter}

# Content generation section
st.header(f"Content Generation for {selected_chapter} ({selected_subject} - {selected_grade})")

# Radio button for selecting the type of content to generate
request_type = st.radio("Select Content Type", [
    "overview and syllabus", "video script", "practice questions", 
    "group activity", "quiz", "project instructions", "exam questions"
])

# Initialize session state to keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

# Button to generate the initial content
if st.button(f"Generate {request_type.title()} for {selected_chapter}"):
    prompt = create_prompt(selected_grade, selected_subject, selected_chapter, request_type)
    response = generate_content(prompt)
    
    # Add the generated response to the chat history if not already added
    if not any(msg["content"] == response for msg in st.session_state.messages):
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Convert response to audio
    audio_file = text_to_speech(response)
    
    # Activate the chat interface
    st.session_state.show_chat = True

# Display the chat interface only if the user has generated a response
if st.session_state.show_chat:
    st.subheader(f"Interactive Chat for {selected_chapter} ({selected_subject} - {selected_grade})")

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**AI (Teacher):** {message['content']}")
            st.audio(audio_file)

    # Input area for additional user prompts
    user_input = st.text_input("Enter your request or refinement here:")

    # Process user input and generate refined response
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate a response based on user input
        refined_prompt = create_prompt(selected_grade, selected_subject, selected_chapter, request_type)
        refined_response = generate_content(refined_prompt)
        
        # Store and display the refined response if it's not a duplicate
        if not any(msg["content"] == refined_response for msg in st.session_state.messages):
            st.session_state.messages.append({"role": "assistant", "content": refined_response})
            st.markdown(f"**AI (Teacher):** {refined_response}")
            
            # Convert refined response to audio
            refined_audio_file = text_to_speech(refined_response)
            st.audio(refined_audio_file)

    # Button to clear chat history
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.show_chat = False

# Footer
st.markdown(
    """
    <hr>
    <div class="footer">
    Lesson Plan Generator aligned with Common Core State Standards | Powered by OpenAI
    </div>
    """,
    unsafe_allow_html=True
)
