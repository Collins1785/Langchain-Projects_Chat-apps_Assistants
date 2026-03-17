import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.output_parsers import StrOutputParser
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import os
load_dotenv()

#Initialize LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.3
)

#Prompt for summarization
summary_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""
You are a expert summarizer
Here is the video transcript:

{transcript}
Please genearet a clear, concise summary of the main points and topics.
"""
)

# 3. Output parser
parser = StrOutputParser()
# 4. Build chain using LCEL (new LangChain syntax)
chain = summary_prompt | llm | parser

#Stremlit UI
st.title("You Tube Video Summarizer")
video_url = st.text_input("Enter the Youtube Video Url:")

def get_video_id(url):
    """
    Extract video ID from youtube Url
    """
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'Youtu.be':
        return parsed_url.path[1:]
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    return None
if st.button("Summarize"):
    if not video_url:
        st.warning("Please enetr a video url")
    else:
        video_id = get_video_id(video_url)
        print (video_id)
        '''
        if not video_id:
            st.error("Invalid Url entered")
        else:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                full_text = " ".join([t['text'] for t in transcript])

                summary = chain.run ({"transcript": full_text})

                st.subheader("Video Summary")
                st.write(summary)

            except Exception as e:
                st.error(f"Error:{str(e)}")
'''
