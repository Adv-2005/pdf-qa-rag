import streamlit as st

st.title("PDF Q&A App")

pdf = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

question = st.text_input(
    "Ask a question"
)