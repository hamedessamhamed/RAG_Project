# 🤖 RAG Document Chatbot

A chatbot that answers questions from your PDF and TXT documents using RAG (Retrieval-Augmented Generation).

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
#Put your PDF and TXT files in knowledge_base/ folder.

### Step 6: Build Index
```bash
cd backend
python index.py
```



