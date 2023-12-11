import streamlit as st
import pdfplumber
import docx
import requests

import os

# Set the HUGGINGFACE_API_TOKEN in your environment before running.
api_token = os.getenv('HUGGINGFACE_API_TOKEN')


def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages)
    return text


def extract_text_from_word(doc_file):
    doc = docx.Document(doc_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Cache the model loading functions
@st.cache_data()
def summarize_text(text, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    API_URL = "https://api-inference.huggingface.co/models/slauw87/bart_summarisation"
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    print(response.json())
    summary = response.json()[0]['summary_text']
    sentences = summary.split('. ') # This splits the summary at each period followed by a space
    summary = '\n'.join(f"- {sentence.strip()}" for sentence in sentences if sentence) # Converts sentences into bullet points
    return summary

@st.cache_data()
def answer_question(context, question, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    API_URL = "https://api-inference.huggingface.co/models/rsvp-ai/bertserini-bert-base-squad"
    response = requests.post(API_URL, headers=headers, json={"inputs": {"question": question, "context": context}})
    print(response.json()) 
    answer = response.json()['answer']
    return answer

def main():
    # Initialize session state
    if 'retry' not in st.session_state:
        st.session_state.retry = False

    st.title("Insurance Document Summarizer and QA")

    uploaded_file = st.file_uploader("Upload an insurance claim document", type=["pdf", "docx"])

    # Only process the file if it's uploaded and the model is not in a retry state
    if uploaded_file is not None and not st.session_state.retry:
        try:
            # Depending on the file type, call the appropriate text extraction function
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = extract_text_from_word(uploaded_file)

            # If text is extracted, summarize and answer questions
            if text:
                try:
                    with st.spinner('Summarizing the document...'):
                        summary = summarize_text(text, api_token)
                    st.markdown("**Summary:**")
                    st.markdown(f'<p style="white-space: pre-wrap;">{summary}</p>', unsafe_allow_html=True)
                    
                    question = st.text_input("Ask a question about the claim:")
                    if question:
                        with st.spinner('Looking for an answer...'):
                            answer = answer_question(text, question, api_token)
                        st.markdown("**Answer:**")
                        st.markdown(f'<p style="white-space: pre-wrap;">{answer}</p>', unsafe_allow_html=True)

                except Exception as e:
                    st.error("An error occurred while processing the document. This usually means that model is still loading. Please hit the retry button and try again.")
                    st.session_state.retry = True
                    if st.button('Retry', key='retry_button'):
                        st.session_state.retry = False
                        st.experimental_rerun()

        except Exception as e:
            st.error("Failed to load the document. Please try again.")
            #st.session_state.retry = True
            # if st.button('Retry', key='retry_doc_failure'):
            #     st.session_state.retry = False
            #     st.experimental_rerun()

    # If the retry button has been clicked, display the message
    if st.session_state.retry:
        st.warning("Please wait for the model to load and then try uploading your document again.")
        if st.button('Retry', key='retry_warning'):
            st.session_state.retry = False
            st.experimental_rerun()


# Check if this script is the main program
if __name__ == '__main__':
    main()