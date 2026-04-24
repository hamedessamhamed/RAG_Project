# 🤖 RAG Document Chatbot

An intelligent chatbot that answers your questions by searching through your own documents. Built with Retrieval-Augmented Generation (RAG), it combines vector search with Large Language Models to provide accurate, context-aware answers from your PDF and TXT files.

Supports **Arabic** and **English** with both local (Ollama) and cloud (Gemini) LLM options.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Store-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal)

---

### ✨ Features

- 📄 Supports PDF and TXT documents
- 🌍 Multilingual — Arabic, English, and 50+ languages
- 🤖 Works with local Ollama or Google Gemini API
- 🔍 Fast vector search using FAISS
- 💬 Beautiful Streamlit chat interface
- ⚡ FastAPI backend
- 🔒 Your documents stay private on your machine

### 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM | Ollama (Qwen2.5) / Google Gemini |
| Embeddings | HuggingFace Multilingual MiniLM |
| Vector DB | FAISS |
| Framework | LangChain |
| Backend | FastAPI |
| Frontend | Streamlit |
---

## 🚀 How To Run

### Step 1: Clone

```bash
git clone https://github.com/GodaSaber/RAG_Project
cd rag-chatbot
```
### Step 2: Create Environment

```bash
conda create -n RAG python=3.10 -y
conda activate RAG
```

### Step 3: Install Dependencies

```bash
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### Step 4: Setup LLM

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:3b
```
### Step 5: Add Documents
Put your PDF and TXT files in knowledge_base/ folder.

### Step 6: Build Index
```bash
cd backend
python index.py
```
after run this folder faiss_index is created

### Step 7: Run Ollama

```bash
ollama serve
```

### Step 8: Run Backend

```bash
conda activate RAG
cd backend
uvicorn main:app --reload
```

### Step 9: Run Frontend

```bash
conda activate RAG
cd backend
streamlit run app.py
```
### Step 10: Open 
http://localhost:8501

## 📁 Project Structure

```
rag-chatbot/
├── knowledge_base/      # Your documents (PDF, TXT)
├── faiss_index/         # Auto-generated index
├── backend/
│   ├── index.py         # Build index
│   ├── main.py          # API server
│   └── app.py           # Chat UI
├── requirements.txt
└── README.md
```


