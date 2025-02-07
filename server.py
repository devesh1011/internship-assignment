from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import os

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()


class TaskResponse(BaseModel):
    tasks: list[str]


llm = ChatGroq(
    model_name="mixtral-8x7b-32768",
    temperature=0,
    api_key=os.environ.get("GROQ_API_KEY"),
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an assistant responsible for orchestrating containerized tasks based on user requests. Your goal is to parse high-level user requests and determine which containerized tasks should be executed, along with their correct order.

Available Tasks:
1. **Sentiment Analysis**: 
   - Keywords: "sentiment", "analyze", "emotion", "tone"
   - Container Name: "sentiment_analysis"

2. **Text Summarization**: 
   - Keywords: "summarize", "summary", "shorten", "condense"
   - Container Name: "text_summarization"

Instructions:
- Parse the user's request carefully.
- Identify the task(s) that match the request based on keywords and context.
- Return your response in JSON format with the following structure:
  ```json
    "tasks": ["container_name_1", "container_name_2", ...]
""",
        ),
        ("human", "{request_text}"),
    ]
)


def decide_tasks(request_text: str):
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"request_text": request_text})
    json_res = json.loads(response)
    return json_res["tasks"]


class OrchestratorRequest(BaseModel):
    request_text: str


@app.post("/orchestrate")
def orchestrate(req: OrchestratorRequest):
    tasks = decide_tasks(req.request_text)
    results = {}

    if "sentiment_analysis" in tasks:
        try:
            resp = requests.post(
                "http://localhost:8001/analyze", json={"text": req.request_text}
            )
            resp.raise_for_status()
            results["sentiment"] = resp.json()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Sentiment analysis service error: {str(e)}"
            )

    if "text_summarization" in tasks:
        try:
            resp = requests.post(
                "http://localhost:8002/summarize", json={"text": req.request_text}
            )
            resp.raise_for_status()
            results["summary"] = resp.json()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Summarization service error: {str(e)}"
            )

    if not results:
        results["message"] = "No tasks were selected for this request."
    return results


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8005)
