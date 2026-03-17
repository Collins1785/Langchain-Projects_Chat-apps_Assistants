import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
# File readers
from pypdf import PdfReader
import docx
load_dotenv()
# -----------------------------
# 🔹 Helper Functions
# -----------------------------

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


def read_txt(file):
    return file.read().decode("utf-8")


def extract_text(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "pdf":
        return read_pdf(uploaded_file)
    elif file_type == "docx":
        return read_docx(uploaded_file)
    elif file_type == "txt":
        return read_txt(uploaded_file)
    else:
        return None


# -----------------------------
# 🔹 Prompt Template
# -----------------------------

COVER_LETTER_PROMPT = """
You are an expert career coach and professional cover letter writer.

Using the resume details below, generate a compelling, professional, and personalized cover letter.

Guidelines:
- Keep it concise (300–400 words)
- Use a strong opening and impactful closing
- Highlight key skills and achievements
- Maintain a confident and professional tone
- Make it suitable for ANY job application
- Do NOT add information not present in the resume

Resume:
{resume_text}

Cover Letter:
"""

prompt_template = PromptTemplate.from_template(COVER_LETTER_PROMPT)

# -----------------------------
# 🔹 Initialize LLM
# -----------------------------

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")

    # Debug (optional – remove later)
    # st.write("DEBUG API KEY:", api_key)

    if not api_key:
        st.error("❌ GROQ_API_KEY is not set or not accessible to Streamlit.")
        st.info("👉 Restart terminal or run: setx GROQ_API_KEY 'your_key'")
        st.stop()

    return ChatGroq(
        groq_api_key=api_key,
        model="llama-3.1-8b-instant",
        temperature=0.7
    )


# -----------------------------
# 🔹 Streamlit UI
# -----------------------------

st.set_page_config(page_title="AI Cover Letter Generator", layout="wide")

st.title("📝 AI-Powered Cover Letter Generator")
st.write("Upload your resume and generate a compelling cover letter instantly.")

uploaded_file = st.file_uploader(
    "Upload your Resume (.pdf, .docx, .txt)",
    type=["pdf", "docx", "txt"]
)

generate_button = st.button("🚀 Generate Cover Letter")

# -----------------------------
# 🔹 Main Logic
# -----------------------------

if generate_button:

    if uploaded_file is None:
        st.warning("⚠️ Please upload a resume before generating a cover letter.")
    else:
        with st.spinner("Generating your cover letter..."):

            resume_text = extract_text(uploaded_file)

            if not resume_text or resume_text.strip() == "":
                st.error("❌ Unable to read the file or file is empty.")
            else:
                llm = get_llm()

                # ✅ Modern LangChain (LCEL)
                chain = prompt_template | llm

                response = chain.invoke({
                    "resume_text": resume_text
                })

                cover_letter = response.content

                st.success("✅ Cover Letter Generated!")

                st.subheader("📄 Your Cover Letter:")
                st.text_area("", cover_letter, height=400)

                # ✅ Download button
                st.download_button(
                    label="📥 Download Cover Letter",
                    data=cover_letter,
                    file_name="cover_letter.txt",
                    mime="text/plain"
                )