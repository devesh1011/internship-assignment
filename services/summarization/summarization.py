from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Initializing Groq LLM for summarization
llm = ChatGroq(model_name="mixtral-8x7b-32768", temperature=0, api_key=os.environ.get("GROQ_API_KEY"))

# prompt template for summarization
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a text summarization assistant. Summarize the following text in a concise manner."),
    ("human", "{text}")
])

class TextRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize_text(request: TextRequest):
    chain = prompt | llm
    response = chain.invoke({"text": request.text})
    summary = response.content.strip()
    return summary
