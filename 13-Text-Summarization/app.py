## TODO: Fix error. YouTube code not working

import streamlit as st
import validators
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader, YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.docstore.document import Document

## Streamlit UI
st.set_page_config(page_title="Summarize Text from YouTube or Website", layout="wide", page_icon="📝")
st.title("Summarize Text from YouTube or Website 📝")
st.subheader("Provide a YouTube video link or a website URL to get a concise summary.")

prompt_template = """
Provide a summary of the following content in 300 words:
Content: {text}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

with st.sidebar:
    groq_api_key = st.text_input("Enter your Groq API Key", type="password")

url = st.text_input("URL:", label_visibility="collapsed")

def get_video_id(youtube_url):
    if "youtu.be" in youtube_url:
        return youtube_url.split("/")[-1]
    elif "youtube.com" in youtube_url:
        return youtube_url.split("v=")[-1].split("&")[0]
    return None

if st.button("Summarize"):
    if not groq_api_key:
        st.error("Please enter your Groq API Key.")
    elif not url.strip() or not validators.url(url):
        st.error("Please enter a valid YouTube video link or website URL.")
    else:
        try:
            llm = ChatGroq(groq_api_key=groq_api_key, model="qwen/qwen3-32b", temperature=0)
            with st.spinner("Fetching content and generating summary..."):
                if "youtube.com" in url or "youtu.be" in url:
                    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[url], headers={"User-Agent": "Mozilla/5.0"})
                    # loader = UnstructuredURLLoader(urls=[url], ssl_verify=False, headers={"User-Agent": "Mozilla/5.0"})
                documents = loader.load()
                if not documents:
                    st.error("No content found at the provided URL.")
                else:
                    chain = load_summarize_chain(
                        llm,
                        chain_type="map_reduce",
                        map_prompt=prompt,
                        combine_prompt=prompt
                    )
                    summary = chain.run(documents)
                    st.success(summary)

        except Exception as e:
            st.error(f"An error occurred: {e}")
