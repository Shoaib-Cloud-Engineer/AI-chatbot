🤖 AI.sist – Smart Q&A Bot from S3 PDF/Excel using FastAPI + OpenAI
<img width="978" height="840" alt="Screenshot" src="https://github.com/user-attachments/assets/7e85c21f-bd52-4481-93ef-2e92e4350eba" />
🧠 What is AI.sist?
AI.sist is a smart chatbot that extracts and answers queries from PDF and Excel files stored in AWS S3, using OpenAI embeddings and FastAPI. It semantically understands structured (Excel) and unstructured (PDF) data, providing accurate answers with keyword highlighting.

🛠️ Setup Instructions
1. Clone the Repo

bash
Copy
Edit
git clone https://github.com/your-username/AI-sist.git
cd AI-sist
2. Create and Activate Virtual Environment

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Or manually:

bash
Copy
Edit
pip install fastapi uvicorn boto3 openai pandas PyMuPDF openpyxl faiss-cpu python-multipart jinja2
4. Configure Keys in newbot.py (for development only)

python
Copy
Edit
os.environ["AWS_ACCESS_KEY_ID"] = "your_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "your_secret"
os.environ["OPENAI_API_KEY"] = "your_openai_key"
⚠️ Note: Never hardcode secrets in production. Use .env, IAM Roles, or Secrets Manager.

🧩 How It Works
Loads files from S3 into memory once

Uses OpenAI embeddings for semantic understanding

Answers queries from documents only

Highlights important keywords in responses

🎨 UI Design
Theme: Sky Blue

Title: AI.sist

Subtitle: Nice Global Customer Support Assistant

Tagline: Our efforts, AI supports.

Branded input/output with keyword highlights

🧱 Tech Stack
Backend: FastAPI

Frontend: Jinja2 Templates

Cloud: AWS EC2 + S3

AI: OpenAI Embeddings

Parsing: PyMuPDF, pandas

Search: FAISS

📉 Challenges Faced
OpenAI rate limits (solved via paid plan)

AWS S3 permission issues

Parsing large or nested documents

Compatibility with Python 3.12

✅ Outcome
Accurate answers from both Excel & PDF files

Blazing-fast responses via semantic search

Ready-to-use, professional chatbot UI

📬 Contact
Have questions or feedback?

📧 Email: shoaibkhalifahere@gmail.com

🔗 GitHub: @Shoaib-Cloud-Engineer

