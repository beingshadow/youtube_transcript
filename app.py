import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

from youtube_transcript_api import YouTubeTranscriptApi

# load all the environment variables
load_dotenv()

# Configure API key for the project
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Generate the content using Google Gemini API
prompt = ''' You are YouTube Video summarizer You will be taking the transcript text and summarize 
the entire video and provide the important summary in details within 700-800 words The transcript will be appended here:'''

# Getting the transcript from YouTube videos
def extract_transcript(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " "
        for i in transcript_text:
            transcript += " " + i['text']
        return transcript

    except Exception as e:
        raise e

# Getting the summary based on Prompt from Google Gemini
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title("Youtube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter your YouTube link")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("# Detailed Notes")
        st.write(summary)