import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("gemini"))

model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")

def percentage_match(resume_text, job_dis):
    prompt = f"""
    You are an expert in resume analysis. Compare the given resume with the job description and provide a percentage match based on skills and experience (total 100%).
    - give the percentage of match
    - If the candidate is from a completely different background, say: **"You are not eligible for this role."**
    - If the skills perfectly match, say: **"Perfect match! Your skills align exactly with the job requirements (100%)."**
    - If there is a moderate match, say: **"Moderate match (X%). The job requires some advanced skills beyond your experience."**

    **Job Description:**
    {job_dis}

    **Resume:**
    {resume_text}

    Answer in **four lines only**.
    """

    response = model.generate_content(prompt)
    return response.text
