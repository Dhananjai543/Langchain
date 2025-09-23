# Deploy Langserve Runnable and Chain as API

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langserve import add_routes

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# 1. Create your prompt template
system_template = "Tramslate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", "{text}")
    ]
)

parser = StrOutputParser()

# 2. Create your chain
chain = prompt_template | model | parser

# 3. App Definition
app = FastAPI(title="Langchain Server",
              version="0.1",
              description="This is a simple Langchain server with Groq Gemma2-9b-It model")

# 4. Add routes
try:
    add_routes(app, chain, path="/chain")
except Exception as e:
    print(f"Error adding routes: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


#pip install pydantic==2.10.6