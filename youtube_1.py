import os
import re
import requests
import streamlit as st
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

import yt_dlp

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ----------------- Setup -----------------
load_dotenv()

st.set_page_config(page_title="YouTube Transcript Summarizer", page_icon="📺")
st.title("📺 YouTube Transcript Summarizer (yt-dlp powered)")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY missing. Add it to your .env file.")
    st.stop()

# ----------------- LLM -----------------
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.3
)

summary_prompt = PromptTemplate(
    input_variables=["transcript"],
    template="""
You are an expert summarizer.

Here is the transcript:

{transcript}

Write a clear, concise summary of the main ideas and key points.
"""
)

parser = StrOutputParser()
chain = summary_prompt | llm | parser

# ----------------- Helpers -----------------
def get_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname in ("youtu.be", "www.youtu.be"):
        return parsed.path.lstrip("/")
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed.query).get("v", [None])[0]
    return None


def extract_subtitles(video_url):
    """
    Uses yt-dlp to fetch subtitles (auto or manual).
    Works even when YouTube transcript API is blocked.
    """
    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)

        subtitles = info.get("subtitles") or info.get("automatic_captions")

        if not subtitles:
            raise Exception("No subtitles available for this video.")

        # Prefer English
        for lang in ["en", "en-US", "en-GB"]:
            if lang in subtitles:
                url = subtitles[lang][0]["url"]
                return requests.get(url).text

        # Fallback: first available language
        first_lang = list(subtitles.keys())[0]
        url = subtitles[first_lang][0]["url"]
        return requests.get(url).text


def vtt_to_text(vtt_data):
    """
    Converts VTT subtitle format to plain text.
    """
    lines = vtt_data.split("\n")
    text_lines = []

    for line in lines:
        # Skip timestamps
        if re.match(r"\d{2}:\d{2}:\d{2}\.\d{3}", line):
            continue
        # Skip metadata
        if line.strip().isdigit() or line.strip() == "WEBVTT":
            continue
        if line.strip():
            text_lines.append(line.strip())

    return " ".join(text_lines)


# ----------------- UI -----------------
video_url = st.text_input("Enter the YouTube video URL:")

if st.button("Summarize"):
    if not video_url:
        st.warning("Please enter a YouTube URL.")
    else:
        try:
            with st.spinner("Extracting subtitles..."):
                vtt_data = extract_subtitles(video_url)
                transcript_text = vtt_to_text(vtt_data)

            if not transcript_text.strip():
                st.error("Transcript extraction failed or returned empty text.")
            else:
                with st.spinner("Generating summary..."):
                    summary = chain.invoke({"transcript": transcript_text})

                st.subheader("Video Summary")
                st.write(summary)

        except Exception as e:
            st.error(f"Error: {str(e)}")