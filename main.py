from chapters import chapters_by_grade_subject
from openai_api import generate_content

# Function to retrieve chapters based on grade and subject
def get_chapters_for_grade_subject(grade, subject):
    return chapters_by_grade_subject.get(grade, {}).get(subject, [])

# Function to create prompt for OpenAI API
# main.py

# main.py

def create_prompt(selected_grade, selected_subject, selected_chapter, request_type):
    base_prompt = f"Create a {request_type} for a {selected_grade} {selected_subject} lesson on '{selected_chapter}'. "
    
    if request_type == "overview and syllabus":
        return base_prompt + "Include objectives, lesson breakdowns, and estimated times, aligned with Common Core State Standards."
    elif request_type == "video script":
        return base_prompt + (
            "You are the teacher. Provide a detailed video script for teaching the topic. "
            "Only include what the teacher would say, without any scene descriptions, shots, or stage directions."
        )
    elif request_type == "practice questions":
        return base_prompt + "Create 5 practice questions with varying difficulty levels."
    elif request_type == "group activity":
        return base_prompt + "Describe a group activity that encourages collaboration and concept application."
    elif request_type == "quiz":
        return base_prompt + "Create a 5-question quiz covering fundamental concepts."
    elif request_type == "project instructions":
        return base_prompt + "Provide detailed instructions for a project-based activity."
    elif request_type == "exam questions":
        return base_prompt + "Generate a set of 5 exam-level questions."
    
    return base_prompt
