from fastapi import FastAPI
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Initialize the Groq LLM for sentiment analysis
llm = ChatGroq(model_name="mixtral-8x7b-32768", temperature=0, api_key=os.environ.get("GROQ_API_KEY"))

# Define the prompt template for sentiment analysis
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sentiment analysis assistant. Analyze the sentiment of the following text and respond with 'Positive', 'Negative', or 'Neutral'."),
    ("human", "{text}")
])

class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze_sentiment(request: TextRequest):
    chain = prompt | llm
    response = chain.invoke({"text": request.text})
    sentiment = response.content.strip()
    return sentiment