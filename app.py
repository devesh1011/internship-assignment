import streamlit as st
import requests

st.title("AI Orchestrator UI")
st.write("Enter your high-level request below:")

request_text = st.text_area(label="Write text here")

if st.button("Submit"):
    try:
        response = requests.post(
            "http://0.0.0.0:8005/orchestrate", json={"request_text": request_text}
        )

        response.raise_for_status()
        result = response.json()
        st.write(result)
    except Exception as e:
        st.error(f"Error calling orchestrator: {e}")
