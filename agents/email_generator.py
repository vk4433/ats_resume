import sys
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("gemini"))

model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")

def generate_email(resume_text, job_dis):
    
    prompt = f"""
    Write a professional and concise email to the recruiter using the given job description and resume.
    - Address it to "Dear Hiring Manager".
    - Highlight key skills that match the job description.
    - Keep it short (four to five lines) yet informative.
    - Concentrate mainly on resume skills.

    Job Description:
    {job_dis}

    Resume:
    {resume_text}

    The email should start with "Dear Hiring Manager," and be professional.

    Best regards,
    Name: 
    Mail: 
    Mobile No: 
    LinkedIn: 
    GitHub: [insert GitHub profile]
    """

    response = model.generate_content(prompt)

    return response.text
 


