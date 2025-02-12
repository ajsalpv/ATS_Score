import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
import json

# Function to get response from Gemini API
def get_gemini_response(input_text):
    """Fetch response from Gemini API with proper error handling."""
    genai.configure(api_key='AIzaSyCXpKg4Z5akGd41Fz0d0p00iNOAoTV2Iiw')  # Set API key dynamically
    model = genai.GenerativeModel("gemini-pro")

    try:
        response = model.generate_content(input_text,generation_config={"temperature": 0})
        return response.text.strip() if hasattr(response, "text") else str(response)
    except Exception as e:
        return f"Error: Failed to get response from Gemini. {str(e)}"

# Function to extract text from uploaded PDF resume
def input_pdf_text(uploaded_file):
    """Extract text from PDF resume."""
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""  # Handle NoneType cases
    return text.strip()

# Streamlit UI
st.title("📄 Smart ATS Resume Analyzer")

# Input fields

# api_key = st.text_input("🔑 Enter Your Gemini API Key", type="password")  # Secure API Key Input
jd = st.text_area("📌 Paste the Job Description")
uploaded_file = st.file_uploader("📎 Upload Your Resume", type="pdf", help="Please upload a PDF resume")

# Submit button
submit = st.button("🚀 Analyze Resume")

if submit:
    if uploaded_file and jd:
        # Extract text from PDF
        resume_text = input_pdf_text(uploaded_file)

        # ATS prompt to enforce JSON response
        # input_prompt = f"""
        # You are an advanced ATS (Applicant Tracking System) specialized in UI/UX analysis.
        # Evaluate the resume based on the given job description.

        # 🔹 Assign a **percentage match** based on relevance.
        # 🔹 Identify **missing keywords** from the job description.
        # 🔹 Provide a **concise profile summary** with improvement suggestions.

        # ⚠️ Respond **ONLY** in JSON format without extra explanations:
        # {{
        #     "JD Match": "XX%",
        #     "MissingKeywords": ["keyword1", "keyword2"],
        #     "Profile Summary": "Your feedback here"
        # }}

        # Resume: {resume_text}
        # Job Description: {jd}
        # """

        input_prompt = f"""
            ### **🚀 ATS Resume Screening System**
            You are an **AI-powered Applicant Tracking System (ATS)** that evaluates resumes based on **job descriptions**.  
            Your goal is to **analyze** the resume and **determine the candidate's suitability** for the role using the following structured evaluation:

            ---

            ### **🔹 Step 1: Extract Candidate Name**
            - Identify the **full name** of the candidate from the resume.  
            - If no name is found, return `"Candidate Name": "Not Found"`.

            ---

            ### **🔹 Step 2: Identify Missing Keywords**
            - Extract **all required skills, tools, and technologies** from the job description.  
            - Extract **all mentioned skills, tools, and technologies** from the resume.  
            - Any **skill in the JD but NOT in the resume** must be added to `"MissingKeywords"`.  
            - If **ALL** required skills are present, return `"MissingKeywords": []`.

            ---

            ### **🔹 Final Evaluation Criteria**
            1. **JD Match Score**  
            - Assign a **percentage match** based on relevance.  
            - The score should be realistic and data-driven.  

            2. **Experience Relevance**  
            - Rate experience fit as:  
                - **Highly Relevant** (Strong match, direct experience)  
                - **Moderately Relevant** (Some transferable skills)  
                - **Needs Improvement** (Lacks key experience)  

            3. **Role Fit Recommendation**  
            - Classify the candidate as:  
                - **Strong Fit** (Highly suitable, ideal match)  
                - **Moderate Fit** (Has potential but has gaps)  
                - **Weak Fit** (Lacks critical requirements, not recommended)  

            4. **Profile Summary & Final Verdict**  
            - Provide a **concise summary** highlighting strengths and improvement areas.  
            - Clearly state if the candidate is **Recommended** or **Not Recommended**.  

            ---

            ### **🔹 Strict JSON Output Format**
            {{
                "Candidate Name": "Extracted Name",
                "JD Match": "XX%",
                "MissingKeywords": ["keyword1", "keyword2", "keyword3"],
                "Experience Relevance": "Highly Relevant / Moderately Relevant / Needs Improvement",
                "Role Fit": "Strong Fit / Moderate Fit / Weak Fit",
                "Profile Summary": "Brief feedback including strengths and improvement suggestions",
                "Final Verdict": "Recommended / Not Recommended"
            }}

            ---

            ### **🔹 Input Data**
            - **Job Description:** {jd}
            - **Candidate Resume:** {resume_text}

            🚨 **STRICT RULE**: Output **ONLY JSON**, no explanations.
            """




        # Get response from Gemini
        response_text = get_gemini_response(input_prompt)

        # Display output
        st.write("📊 ATS Evaluation Result")
        try:
            parsed_response = json.loads(response_text)  # Convert string to JSON
            st.json(parsed_response)  # Display formatted JSON
        except json.JSONDecodeError:
            # st.error("⚠️ The response is not valid JSON. Here’s the raw output:")
            st.write(response_text)

    else:
        st.warning("⚠️ Please provide a Job Description, upload a resume, and enter your API key.")
