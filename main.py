from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from helper_functions import create_db_from_github_file, get_google_api_key, DB
import re





app = FastAPI()

google_api_key = get_google_api_key()
MODEL_NAME = "gemini-2.0-flash-exp"
llm = ChatGoogleGenerativeAI(model=f"models/{MODEL_NAME}", google_api_key=google_api_key)

db = DB()

def get_product_ids():
    pass

class QueryRequest(BaseModel):
    question: str

def generate_code(question: str):
    prompt_template = PromptTemplate(
        input_variables=["question"],
        template="""
        You are an AI assistant that generates Firebase Firestore queries to only retrieve product IDs based on a user's query.
        The products are stored in a Firestore collection named "products", and you must generate a query that fetches 
        relevant product IDs based on attributes like name, brand, price etc. And never update or delete any data.
        
        Respond **only** with a Python function if the query follows the rule.

        **Limit** the data to **20** documents.
        
        ```python
        def get_product_ids():
            products_ref = db.collection("products")
            query_ref = products_ref.where("Product Name", "==", based on user query)
            results = query_ref.stream()
            
            product_ids = [doc.id for doc in results]
            return product_ids
        ```
        
        Answer the following question: {question} Based on this context: {context}\n\n
        The rule:
        If the user asks to **update or delete**, respond with:
        **"I can only retrieve data, updating or deleting is not allowed."**
        """,
    )

    retriever = create_db_from_github_file("https://raw.githubusercontent.com/abdullah0150/Images/refs/heads/main/products_and_db_metadata")
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )
    
    response = rag_chain.invoke(question)
    return response

@app.post("/generate-code")
def generate_code_endpoint(request: QueryRequest):
    response = generate_code(request.question)
    
    if "```python" in response and "def get_product_ids" in response:
        # Extract only the Python code
        code_match = re.search(r"```python\n(.*?)```", response, re.DOTALL)
        if code_match:
            clean_code = code_match.group(1)
        else:
            clean_code = response  # If there's an issue, use raw response

        try:
            # I know this is not secure, but it's just a demo and you can apply more security measures or run the code on a separate server
            # and return the result
            exec(clean_code, globals())
            product_ids = get_product_ids()
            return {"product_ids": product_ids}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")
    else:
        return {"message": response}
