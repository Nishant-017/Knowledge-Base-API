# 📚 Knowledge Base Semantic Search API

A backend service built using **FastAPI** and **Qdrant vector** database that enables:

- **Document storage with embeddings**
- **Semantic search**
- **Filtered semantic search**
- **Pagination**
- **Statistics endpoint**
- **Automated tests**

This project demonstrates a complete vector-search backend system 

--- 

## 🚀 Features

- ✅ Add documents with embeddings
- ✅ Semantic similarity search
- ✅ Filtered search by category
- ✅ Paginated document listing
- ✅ Collection management using Qdrant
- ✅ Stats endpoint (counts + categories)
- ✅ Service & API test coverage

## 🧱 Tech Stack

- Python
- FastAPI – API framework
- Qdrant – Vector database (local persistent mode)
- FastEmbed – Text embeddings
- Pytest – Testing

---

## 📁 Project Structure

task_3/
│
├── src/
│   ├── main.py
│   ├── routers/
│   │   └── documents.py
│   ├── services/
│   │   ├── qdrant_service.py
│   │   └── embedding_service.py
│   └── models/
│       └── schemas.py
│
├── tests/
│   ├── test_qdrant_service.py
│   └── test_api.py
│
├── sample_documents.json
├── upload_samples.py
├── requirements.txt
└── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Create virtual environment

- python -m venv venv

**Activate:**

- Windows:
venv\Scripts\activate

- Mac/Linux:
source venv/bin/activate

### 2️⃣ Install dependencies
pip install -r requirements.txt

### 3️⃣ Run the API
uvicorn src.main:app --reload

- **API will be available at:**

- 👉 http://127.0.0.1:8000

- 👉 Swagger UI: http://127.0.0.1:8000/docs

### 📄 Load Sample Data

After creating sample_documents.json,

**run:**
python upload_samples.py

- This will upload all sample documents into Qdrant.

---

### 📌 API Endpoints

➕ Add Document
POST /documents


Body:

{
  "id": 1,
  "title": "FastAPI Overview",
  "content": "FastAPI is a Python web framework.",
  "category": "tech"
}

🔍 Semantic Search
POST /search

{
  "query": "python framework",
  "limit": 5
}

🎯 Filtered Semantic Search
POST /search/filter

{
  "query": "anime adventure",
  "limit": 5,
  "category": "anime"
}

📃 Paginated Listing
GET /list_all?limit=5&offset=0

📄 Get Document by ID
GET /documents/{id}

📊 Stats
GET /stats


Example response:

{
  "collection": "kb_api",
  "total_documents": 30,
  "vector_dimension": 384,
  "categories": {
    "tech": 7,
    "anime": 6,
    "sports": 5
  }
}

### 🧪 Running Tests
▶️ API Tests (server must be running)
pytest tests/test_api.py

▶️ Service Tests (stop server first)
pytest tests/test_qdrant_service.py
(Local Qdrant allows only one process at a time)

---

### 🧠 How It Works

Documents are converted into embeddings using FastEmbed

Embeddings stored in Qdrant

Search queries converted to embeddings

Qdrant performs vector similarity search

Optional filters applied on payload metadata

***📈 Stats Endpoint Logic***

Counts total documents

Retrieves embedding vector size

Groups documents by category


### ✅ Key Concepts Demonstrated

- Vector databases

- Semantic search

- RESTful API design

- Pagination

- Metadata filtering

- Service layer architecture

- Automated testing

### 📌 Notes

Qdrant runs in local persistent mode (no Docker required)

Data stored in qdrant_data/ directory

Folder may remain even after collection deletion (expected behavior)


### 🎯 Future Improvements (Optional)

- Authentication
- Advanced filtering
- Sorting by score/date
- Frontend UI

