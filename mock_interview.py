import streamlit as st
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# -----------------------------
# 🔹 Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# 🔹 Prompt Template
# -----------------------------

INTERVIEW_PROMPT = """
You are an expert interviewer and career coach.

Based on the job role and job description below, generate 5 highly relevant interview questions along with strong, well-structured sample answers.

Guidelines:
- Questions should be realistic and commonly asked in interviews
- Answers should be clear, professional, and impactful
- Include a mix of:
  - Technical questions
  - Behavioral questions
  - Scenario-based questions
- Keep answers concise but meaningful (4–6 lines each)
- Make it useful for interview preparation

Job Role:
{job_role}

Job Description:
{job_description}

Output Format:

1. Question:
Answer:

2. Question:
Answer:

... and so on up to 5.
"""

prompt_template = PromptTemplate.from_template(INTERVIEW_PROMPT)

# -----------------------------
# 🔹 Initialize LLM
# -----------------------------

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        st.error("❌ GROQ_API_KEY not found. Please check your .env file.")
        st.stop()

    return ChatGroq(
        groq_api_key=api_key,
        model="llama-3.1-8b-instant",
        temperature=0.7
    )

# -----------------------------
# 🔹 Streamlit UI
# -----------------------------

st.set_page_config(page_title="Mock Interview Assistant", layout="wide")

st.title("🎯 AI Mock Interview Assistant")
st.write("Prepare for your interviews with AI-generated questions and answers.")

# Inputs
job_role = st.text_input("💼 Enter Job Role (e.g., Software Engineer)")

job_description = st.text_area(
    "📄 Enter Job Description",
    height=200,
    placeholder="Paste the job description here..."
)

generate_button = st.button("🚀 Generate Interview Questions")

# -----------------------------
# 🔹 Main Logic
# -----------------------------

if generate_button:

    if not job_role or not job_description:
        st.warning("⚠️ Please provide both Job Role and Job Description.")
    else:
        with st.spinner("Generating interview questions..."):

            llm = get_llm()

            # LCEL chain
            chain = prompt_template | llm

            response = chain.invoke({
                "job_role": job_role,
                "job_description": job_description
            })

            output = response.content

            st.success("✅ Interview Questions Generated!")

            st.subheader("📌 Questions & Answers:")
            st.text_area("", output, height=400)

            # Download button
            st.download_button(
                label="📥 Download Q&A",
                data=output,
                file_name="mock_interview.txt",
                mime="text/plain"
            )