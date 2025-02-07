FROM python:3.9-slim

WORKDIR /app

COPY ./server.py /app/

RUN pip install --no-cache-dir fastapi uvicorn requests langchain-groq

EXPOSE 80

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
