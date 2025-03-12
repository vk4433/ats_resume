import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("gemini"))

model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")

def resume_generation (resume_text, job_desc_text):
    prompt = f"""
    You are a professional resume editor. Given the following original resume and job description, update the resume to be more ATS-friendly.
    
    Tasks:
    1. Reformat the resume so that each section (Contact Information, Education, Skills, Projects, Work Experience) is clearly separated with headers.
    2. Incorporate relevant keywords from the job description (e.g., "NLP", "Machine Learning", "Data Engineering") naturally into the resume.
    3. Ensure the resume is clearly spaced and easy to read.
    
    Original Resume:
    {resume_text}
    
    Job Description:
    {job_desc_text}
    
    Please provide the updated, well-formatted resume.
    """
    response =model.generate_content(prompt)
    return response.text

 

