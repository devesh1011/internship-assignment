FROM python:3.9-slim

WORKDIR /app

# Copy the service code into the container.
COPY ./sentiment_analysis.py /app/

# Install dependencies.
RUN pip install --no-cache-dir fastapi uvicorn langchain-groq python-dotenv

EXPOSE 80

# Run the FastAPI app using Uvicorn.
CMD ["uvicorn", "sentiment_analysis:app", "--host", "0.0.0.0", "--port", "80"]
