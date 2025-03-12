import streamlit as st
from extract.text import text_extract
from agents.workflow import setup_workflow
from IPython.display import Image
import tempfile

st.set_page_config(page_title="AI Resume Assistant", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2c3e50;'>AI Resume Assistant</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])  

with col1:
    st.markdown("### Workflow Diagram")
    
    try:
         
        graph = setup_workflow()
        workflow_diagram = graph.get_graph().draw_mermaid_png()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(workflow_diagram)
            temp_file_path = temp_file.name

        st.image(temp_file_path, caption="AI Resume Workflow", use_container_width=True)

    except Exception as e:
        st.error(f"Error generating workflow diagram: {e}")

# Right Column: Inputs and Processing
with col2:
    st.markdown("**Upload Resume (PDF)**")
    resume_file = st.file_uploader("", type=["pdf"], key="resume_uploader")

    st.markdown("**Enter Job Description**")
    job_desc_text = st.text_area("Paste the job description here:", "", height=200, key="job_desc_textarea")

    if resume_file and job_desc_text:
        if st.button("Process Resume"):
            try:
                resume_text = text_extract(resume_file)

                initial_state = {
                    "resume_text": resume_text,
                    "job_description": job_desc_text,
                    "eligibility_result": "",
                    "generated_email": ""
                }

                final_state = graph.invoke(initial_state)

                st.session_state.resume_text = final_state.get("resume_text", "No updated resume available")
                st.session_state.eligibility_result = final_state.get("eligibility_result", "No eligibility result available")
                st.session_state.generated_email = final_state.get("generated_email", "No email generated")

                st.success("Processing completed! Use the buttons below to view results.")

            except Exception as e:
                st.error(f"Error: {e}")

    if "resume_text" in st.session_state:
        if st.button("View ATS-Friendly_updated_Resume"):
            st.text_area("ATS-Friendly Resume", st.session_state.resume_text, height=300, label_visibility="collapsed")

    if "eligibility_result" in st.session_state:
        if st.button("View Eligibility Check Result"):
            st.text_area("Eligibility Check Result", st.session_state.eligibility_result, height=100, label_visibility="collapsed")

    if "generated_email" in st.session_state:
        if st.button("View Generated Recruiter Email"):
            st.text_area("Generated Recruiter Email", st.session_state.generated_email, height=200, label_visibility="collapsed")
