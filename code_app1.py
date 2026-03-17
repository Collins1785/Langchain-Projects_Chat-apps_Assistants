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
    temperature=0.3
)

# Prompt
prompt = PromptTemplate(
    input_variables=["task"],
    template="""
You are an expert Python coding assistant.

Your job:
1. Read the user's task.
2. Generate clean, correct Python code that solves it.
3. Provide a clear line-by-line explanation of the important parts.

User task:
{task}

Your output format:
--------------------
### Python Code
<put the code here>

### Explanation
<explain the key lines here>
--------------------
"""
)

parser = StrOutputParser()
chain = prompt | llm | parser

# Streamlit UI
st.title("Python Coding Assistant")

task = st.text_area("Describe the Python task you want to generate code for:")

if st.button("Generate Code"):
    if task.strip():
        with st.spinner("Generating code..."):
            response = chain.invoke({"task": task})
            st.markdown(response)
    else:
        st.warning("Please enter a task.")