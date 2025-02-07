# Internship-Assignment

This project implements a microservices-based text analysis system with sentiment analysis and text summarization capabilities using Groq LLM.

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Groq API key

## Setup

1. Clone the repository

2. Create a `.env` file in the root directory with your Groq API key:
```sh
GROQ_API_KEY=your_api_key_here
```

3. Build and start the Docker containers:

```
docker-compose up --build
```

4. Run the Streamlit frontend:

```
pip install streamlit requests
streamlit run app.py
```

5. Run the server.py

```
python server.py
```

## Services
The system consists of three main components:

***Frontend:*** Streamlit application running on port 8501
***Containerized Tasks:***
Sentiment Analysis (port 8001)
Text Summarization (port 8002)
***Backend:*** FastAPI server running on port 8005

## Usage

1. Open the Streamlit UI at http://localhost:8501
2. Enter text in the input area
3. Click "Submit" to analyze
4. Based on your input, the system will:
 - Analyze sentiment based on request
 - Generate a summary

## Architecture Diagram

![Architecture Diagram](https://github.com/user-attachments/assets/ec5a9c4c-334b-41c9-a041-53d8ca89e11c)
