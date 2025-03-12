import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("gemini"))

model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")

def job_disc(upload_text, resume_text):
    prompt = f"""
    Analyze the given job description and resume. Compare the required skills and qualifications from the job description with those listed in the resume. Then, provide the following:

    1. Key Matching Skills: List the skills from the resume that match the job description and also give the count.
    2. Missing Skills**: Identify skills required by the job but missing in the resume and also give the count.
    3. analyse the experince from resume and job discription if the person is elgible for the role or not.

    **Job Description:**
    {upload_text}

    **Resume:**
    {resume_text}

    Ensure the response is structured and easy to understand and short .
    """

    response = model.generate_content(prompt)
    return response.text

 
