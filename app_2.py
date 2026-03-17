#Chat app
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

# 1. LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.3
)

# 2. Prompt
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
You are a helpful AI assistant.
User says: {user_input}
Your response:
"""
)

# 3. Output parser
parser = StrOutputParser()

# 4. Build chain using LCEL (new LangChain syntax)
chain = prompt | llm | parser

# 5. Run chatbot
if __name__ == "__main__":
    user_input = input("Ask me anything: ")
    response = chain.invoke({"user_input": user_input})
    print("AI says:", response)
