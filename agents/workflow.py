from typing import TypedDict
from langgraph.graph import StateGraph, END, START
from agents.elgible import percentage_match
from agents.email_generator import generate_email
from agents.job_discription import job_disc
from agents.resume_generator import resume_generation
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("gemini"))

model = genai.GenerativeModel(model_name="gemini-1.5-flash-002")

class workflowstate(TypedDict):
    resume_text: str
    job_description: str
    eligibility_result: str
    generated_email: str


def analyze_job(state: workflowstate) -> workflowstate:
    job_desc = job_disc(state["job_description"], state["resume_text"])
    state["job_description"] = job_desc
    return state


def check_eligibility(state: workflowstate) -> workflowstate:
    eligibility = percentage_match(state["resume_text"], state["job_description"])
    state["eligibility_result"] = eligibility
    return state

def generate_recruiter_email(state: workflowstate) -> workflowstate:
    if "not eligible" in state["eligibility_result"].lower():
        state["generated_email"] = "Candidate is not eligible. No email generated."
    else:
        state["generated_email"] = generate_email(state["resume_text"], state["job_description"])
    return state

def resume_writing(state: workflowstate) -> workflowstate:
    job_desc = state.get("job_description", "")
    resume_text = state.get("resume_text", "")

    if not job_desc:
        state["resume_text"] = "No job description provided. Cannot generate a resume."
        return state

    updated_resume = resume_generation(resume_text, job_desc)
    state["resume_text"] = updated_resume
    return state

def setup_workflow():
    workflow = StateGraph(workflowstate)  

    # Adding Nodes
    workflow.add_node("analyze_job", analyze_job)
    workflow.add_node("check_eligibility", check_eligibility)
    workflow.add_node("generate_recruiter_email", generate_recruiter_email)
    workflow.add_node("resume_writing", resume_writing)

    # Adding Edges
    workflow.add_edge(START, "analyze_job")
    workflow.add_edge("analyze_job", "check_eligibility")
    workflow.add_edge("check_eligibility", "generate_recruiter_email")
    workflow.add_edge("generate_recruiter_email", "resume_writing")
    workflow.add_edge("resume_writing", END)

    return workflow.compile()

