import streamlit as st
import requests
import json

st.title("AI Orchestrator")

user_request = st.text_area("Enter your request")

if st.button("Submit"):
    if user_request:
        try:
            api_url = (
                "http://fastapi:8000/orchestrate"  # Important: FastAPI container name
            )
            response = requests.post(api_url, json={"request": user_request})
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            results = response.json()
            st.write("Results:")
            st.write(results)
        except requests.exceptions.RequestException as e:
            st.error(f"Error communicating with the backend: {e}")
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON response from backend: {e}")
    else:
        st.warning("Please enter a request.")
