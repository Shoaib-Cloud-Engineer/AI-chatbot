import os
import io
import boto3
import openai
import pandas as pd
import PyPDF2
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sentence_transformers import SentenceTransformer, util
from starlette.middleware.cors import CORSMiddleware

# --- AWS S3 & OpenAI Configuration ---
AWS_ACCESS_KEY_ID = "PASTE-HERE"
AWS_SECRET_ACCESS_KEY = "PASTE-HERE"
S3_BUCKET_NAME = "botchat-bucket-1"
FOLDER_NAME = "chatbot/"  # Folder inside bucket containing PDF and Excel

openai.api_key = "PASTE-HERE"

# --- Initialize App, S3, Templates ---
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

model = SentenceTransformer('all-MiniLM-L6-v2')
documents = []

# --- Load All PDF and Excel Files into Memory Once ---
def load_documents():
    global documents
    documents = []
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=FOLDER_NAME)
    for obj in response.get("Contents", []):
        key = obj["Key"]
        if key.endswith(".pdf"):
            file_obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=key)
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_obj['Body'].read()))
            for i, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text:
                    documents.append({"content": text, "source": f"{key} - Page {i+1}"})
        elif key.endswith(".xlsx") or key.endswith(".xls"):
            file_obj = s3.get_object(Bucket=S3_BUCKET_NAME, Key=key)
            df = pd.read_excel(io.BytesIO(file_obj['Body'].read()))
            for _, row in df.iterrows():
                text = " | ".join([f"{col}: {str(val)}" for col, val in row.items()])
                documents.append({"content": text, "source": key})

load_documents()
doc_texts = [doc["content"] for doc in documents]
doc_embeddings = model.encode(doc_texts, convert_to_tensor=True)

# --- Smart Answer Logic ---
def get_relevant_chunks(query):
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, doc_embeddings, top_k=5)[0]
    return [documents[hit['corpus_id']] for hit in hits]

def ask_openai(context, question):
    prompt = f"Answer the following based only on the provided context:\n\nContext:\n{context}\n\nQuestion: {question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

@app.get("/", response_class=HTMLResponse)
def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask(request: Request, question: str = Form(...)):
    relevant_chunks = get_relevant_chunks(question)
    context = "\n\n".join([f"From {c['source']}:\n{c['content']}" for c in relevant_chunks])
    answer = ask_openai(context, question)
    return templates.TemplateResponse("index.html", {"request": request, "question": question, "answer": answer})
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("aibot:app", host="0.0.0.0", port=5000, reload=True)
