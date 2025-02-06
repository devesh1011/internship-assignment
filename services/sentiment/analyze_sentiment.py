from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import sys
import json
import os

llm = ChatGroq(api_key=os.environ.get("GROQ_API_KEY"))


def analyze_sentiment(text):
    prompt_template = """
    Analyze the sentiment of the following text:

    {text}

    Return a JSON object with the sentiment label ("positive", "negative", or "neutral") and a confidence score (0.0-1.0).  For example:

    ```json
    {{
      "sentiment": "positive",
      "confidence": 0.85
    }}
    ```
    """
    prompt = PromptTemplate(input_variables=["text"], template=prompt_template)
    llm_input = prompt.format(text=text)
    llm_response = llm(llm_input)
    try:
        sentiment_data = json.loads(llm_response)
        return sentiment_data
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON from LLM: {e}", "llm_response": llm_response}


if __name__ == "__main__":
    text = sys.stdin.read()
    sentiment = analyze_sentiment(text)
    json.dump(sentiment, sys.stdout)
