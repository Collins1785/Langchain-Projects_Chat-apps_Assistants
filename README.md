
**Week 4 – LangChain Projects with Groq LLM**

This week, I built several chat applications and GenAI‑powered assistants using **Streamlit** for the UI and **Groq LLM** for fast, high‑quality responses. These projects helped me understand how chatbots actually work behind the scenes and how different prompting techniques influence the quality of the output.

One of the most challenging tasks was creating a **YouTube video summarizer**. Even after following the instructions from the recordings, the transcript extraction kept failing with the error:

```
no element found: line 1, column 0
```

After digging deeper, I discovered that YouTube was blocking the transcript endpoint for my IP, which meant the standard transcript API wouldn’t work. With the help of Copilot, I switched to using:

```
import yt_dlp
```

This approach uses YouTube’s internal subtitle API, which isn’t blocked, and finally allowed me to extract subtitles and generate accurate summaries. After several rounds of troubleshooting and refinement, I successfully built a working YouTube transcript summarizer.

---
