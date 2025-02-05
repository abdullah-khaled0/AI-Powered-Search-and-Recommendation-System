import os
import textwrap
import json

import firebase_admin # type: ignore
from firebase_admin import credentials, firestore # type: ignore

from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import requests


from dotenv import load_dotenv
load_dotenv()




def get_google_api_key():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set. Please set it as an environment variable.")
    
    return GOOGLE_API_KEY
    

def to_markdown(text):
    text = text.replace('•', '  *')
    return "> " + textwrap.indent(text, '> ', predicate=lambda _: True).replace('\n', '\n> ')


def DB():
    # Load Firebase credentials from environment variable
    firebase_json = os.getenv("FIREBASE_CREDENTIALS")
    
    if not firebase_json:
        raise ValueError("FIREBASE_CREDENTIALS environment variable is missing!")
    
    # Convert JSON string back to a dictionary
    firebase_credentials = json.loads(firebase_json)
    
    # Initialize Firebase
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)
    
    # Firestore client
    db = firestore.client()

    return db






def create_db_from_github_file(file_url: str, file_type: str = "text") -> FAISS:
    """
    Create a FAISS database from a file hosted on GitHub.

    Args:
        file_url (str): URL of the file on GitHub.
        file_type (str): Type of the file ('text' or 'pdf'). Default is 'text'.

    Returns:
        FAISS: A FAISS vector store database built from the file's content.
    """

    google_api_key = get_google_api_key()
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=google_api_key)


    # Fetch the file from GitHub
    response = requests.get(file_url)
    response.raise_for_status()  # Raise an error if the request fails
    file_content = response.content

    # Load the document based on file type
    if file_type == "text":
        # Directly create a document for plain text
        text = file_content.decode("utf-8")
        documents = [Document(page_content=text, metadata={"source": file_url})]
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # Create the FAISS vector store
    db = FAISS.from_documents(docs, embeddings)

    retriever = db.as_retriever()
    return retriever
