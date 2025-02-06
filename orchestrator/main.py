from fastapi import FastAPI, HTTPException
from langchain_groq import ChatGroq
import subprocess
import json
import os

app = FastAPI()

llm = ChatGroq(api_key=os.environ.get("GROQ_API_KEY"))


@app.post("/orchestrate")
async def orchestrate(request: dict):
    user_request = request.get("request")
    if not user_request:
        raise HTTPException(status_code=400, detail="Missing 'request' field")

    prompt = f"""
    You are an AI Orchestrator.  The user request is: {user_request}

    Based on the request, choose one or more of the following containerized tasks:
    - sentiment_analysis
    - summarization

    Return a JSON object with the tasks to execute.  For example:
    ```json
    {{
      "tasks": ["summarization", "sentiment_analysis"] 
    }}
    ```
    """

    llm_response = llm(prompt)
    try:
        tasks_to_run = eval(llm_response)["tasks"]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing LLM response: {e}. LLM Response: {llm_response}",
        )

    results = {}
    for task in tasks_to_run:
        try:
            container_name = f"{task}-container"
            # Pass user_request to container's stdin, capture stdout
            process = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",  # Remove container after execution
                    "--name",
                    container_name,
                    task,  # The image name
                ],
                input=user_request.encode(),  # Encode the input string
                capture_output=True,  # Capture stdout and stderr
                text=True,  # Treat output as text
                check=True,  # Raise exception for non-zero exit codes
            )

            # Process the output (JSON expected)
            try:
                container_output = json.loads(process.stdout)
                results[task] = container_output
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Invalid JSON from container {task}: {e}. Output: {process.stdout}",
                )

        except subprocess.CalledProcessError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error running container {task}: {e}. Stderr: {e.stderr}",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

    return results
