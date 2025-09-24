import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
import openai
from dotenv import load_dotenv

load_dotenv()

## Langsmith tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot With OpenAI"

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user's question as best as you can."),
    ("user", "Question: {input}"),
])

def generate_response(question, api_key, engine, temperature, max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(
        model=engine
    )
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"input": question})
    return answer

## Title of the app
st.title("Q&A Chatbot")

## Sidebar for user inputs
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

## Dropdown to select various Open AI models
engine = st.sidebar.selectbox("Select the Open AI model", ["gpt-4-turbo", "gpt-4", "gpt-5"])

## Adjust response parameters
temperature = st.sidebar.slider("Select the temperature", 0.0, 1.0, 0.5)
max_tokens = st.sidebar.slider("Select the max tokens", 1, 300, 150)

## Main Interface
st.write("Ask any question and get an answer!")
user_input = st.text_input("Enter your question here:")

if user_input:
    response = generate_response(user_input, api_key, engine, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please enter a question to get started.")