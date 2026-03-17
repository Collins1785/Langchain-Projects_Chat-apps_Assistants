import streamlit as st
from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.4
)

# Prompt
prompt = PromptTemplate(
    input_variables=["points"],
    template="""
You are a professional email writing assistant.

The user will provide bullet‑point context.  
Your job is to write a polished, well‑structured email that follows these rules:

1. Include a clear and relevant **Subject line**.
2. Start with a professional **Greeting**.
3. Write a clean, concise **Email Body** that covers all the user's points.
4. Ensure each point is addressed clearly and logically.
5. Maintain a polite, professional tone.
6. End with a proper **Wrap‑up / Closing**.

User's bullet‑points:
{points}

Your output format:
--------------------
### Generated Email

Subject: <subject line>

<greeting>

<body paragraphs>

<professional closing>
--------------------
"""
)

parser = StrOutputParser()
chain = prompt | llm | parser

# Streamlit UI
st.title("Smart Email Writer ✉️")

st.write("Provide the key points for your email below:")

points = st.text_area(
    "Enter bullet‑points or context:",
    placeholder="• Follow up on project status\n• Request updated timeline\n• Ask for next steps"
)

if st.button("Generate Email"):
    if points.strip():
        with st.spinner("Drafting your email..."):
            response = chain.invoke({"points": points})
            st.markdown(response)
    else:
        st.warning("Please enter some context for the email to be generated.")