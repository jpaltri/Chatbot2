from langchain.chains import LLMChain
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
import boto3
import os
import streamlit as st
import PyPDF2
import io

# Setup AWS and environment variables securely
os.environ["AWS_PROFILE"] = "Julien"

# Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

model_id = "anthropic.claude-v2"

llm = Bedrock(
    model_id=model_id,
    client=bedrock_client,
    model_kwargs={"max_tokens_to_sample": 2000, "temperature": 0.9}
)

def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() if page.extract_text() else ''
    return text

def my_chatbot(language, freeform_text, pdf_content):
    # Modifying the prompt to use PDF content as a knowledge base
    prompt = PromptTemplate(
        input_variables=["language", "freeform_text", "pdf_content"],
        template="You are a chatbot. You have read the following document: {pdf_content}\n\nUser Question in {language}: {freeform_text}\nAnswer:"
    )
    bedrock_chain = LLMChain(llm=llm, prompt=prompt)
    try:
        response = bedrock_chain({'language': language, 'freeform_text': freeform_text, 'pdf_content': pdf_content})
        return response
    except Exception as e:
        st.error(f"Failed to fetch response: {str(e)}")
        return None

st.title("Bedrock Chatbot")

# Automatically load a PDF from the file system
pdf_path = "Notes Cindy.pdf"  # Update this to the path of your PDF
pdf_content = extract_text_from_pdf(pdf_path)

# Display the PDF content
st.text_area("PDF Content (Knowledge Base)", value=pdf_content, height=300, disabled=True)

language = st.sidebar.selectbox("Language", ["english", "spanish"])
freeform_text = st.sidebar.text_area("What is your question based on the document?", max_chars=100)

if st.sidebar.button("Submit"):
    if freeform_text:
        with st.spinner('Fetching response...'):
            response = my_chatbot(language, freeform_text, pdf_content)
            if response:
                st.write(response['text'])
            else:
                st.write("Please try again.")
