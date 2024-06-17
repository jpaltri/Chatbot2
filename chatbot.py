from langchain.chains import LLMChain
from langchain.llms.bedrock import Bedrock
from langchain.prompts import PromptTemplate
import boto3
import os
import streamlit as st
import PyPDF2
import io
import chainlit as cl

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
        template="You are a friendly and intelligent chatbot. You will give simple, accurate and brief explanations or instructions. If you do not know how to respond, simply state that you do not know, never make up an answer. You have read the following document: {pdf_content}\n\nUser Question in {language}: {freeform_text}\nAnswer:"
    )
    bedrock_chain = LLMChain(llm=llm, prompt=prompt)
    try:
        response = bedrock_chain({'language': language, 'freeform_text': freeform_text, 'pdf_content': pdf_content})
        return response
    except Exception as e:
       return f"Failed to fetch response: {str(e)}"

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label = "Summarize air import",
            message = "Can you summarize the air import process into brief and well defines steps",
            icon = "https://static.vecteezy.com/system/resources/previews/014/237/107/non_2x/intelligent-system-idea-software-development-gradient-icon-vector.jpg"
        ),
        cl.Starter(
            label = "Explain a concept",
            message = "Can you explain the concept of Incoterms",
            icon = "https://www.creativefabrica.com/wp-content/uploads/2022/07/25/Html-File-Line-Gradient-Icon-Graphics-34809782-1-1-580x387.jpg"
        ),
        cl.Starter(
            label = "Define a terminology",
            message = "Can you define and explain in layman terms \"PTT\"",
            icon = "https://png.pngtree.com/png-clipart/20230920/original/pngtree-book-pixel-perfect-gradient-linear-ui-icon-red-color-illustration-vector-png-image_12806820.png"
        ),
        cl.Starter(
            label = "Help me use CargoWise",
            message = "How do I open a file on CargoWise?",
            icon = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfpV1cOOZDFNr2atjHgVNWedyrzJCQ1q2AUw&s"
        ),
    ]

@cl.on_chat_start
async def on_chat_start():
    pdf_path = "C:/Users/pcset/OneDrive/Documents/Notes Cindy.pdf"
    pdf_content = extract_text_from_pdf(pdf_path)

    cl.user_session.set("pdf_content", pdf_content)

"""     languages = ["English", "Spanish", "Italian", "Mandarin"]
    language_selection = await cl.Select(
        id = "language_select",
        label = "Select_Language",
        values = languages,
        initial_value = "english"
    ).send()

    cl.user_session_set("selected_language", language_selection("selected")) """

@cl.on_message
async def on_message(message:str):
    pdf_content= cl.user_session.get("pdf_content")
    language = cl.user_session.get("selected_language")
    
    response = my_chatbot(language, message, pdf_content)

    await cl.message(content=response.get('text', 'Please try again.')).send()


""" st.title("Air Import Chatbot") """

""" # Automatically load a PDF from the file system
pdf_path = "C:/Users/pcset/OneDrive/Documents/Notes Cindy.pdf"  # Update this to the path of your PDF
pdf_content = extract_text_from_pdf(pdf_path)

# Display the PDF content
st.text_area("PDF Content (Knowledge Base)", value=pdf_content, height=300, disabled=True)

language = st.sidebar.selectbox("Language", ["english", "spanish"])
freeform_text = st.sidebar.text_area("What is your question?", max_chars=300)

if st.sidebar.button("Submit"):
    if freeform_text:
        with st.spinner('Fetching response...'):
            response = my_chatbot(language, freeform_text, pdf_content)
            if response:
                st.write(response['text'])
            else:
                st.write("Please try again.")
 """
