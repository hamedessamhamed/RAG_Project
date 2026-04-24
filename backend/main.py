import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


# =========================
# Load env
# =========================
load_dotenv()

FAISS_PATH = "../faiss_index"


# =========================
# Embeddings
# =========================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

db = FAISS.load_local(
    FAISS_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_kwargs={"k": 3})


# =========================
# LLM - Local
# =========================
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0.5,
)


# =========================
# Prompt
# =========================
SYSTEM_PROMPT = """
You are a helpful assistant.
Use the context to answer in max 3 sentences.
If you don't know, say you don't know.
Answer in the same language as the question.

Context:
{context}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}")
])


# =========================
# RAG Chain
# =========================
qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)


# =========================
# FastAPI
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "RAG API running"}


@app.post("/query")
def query_rag(query: Query):
    response = rag_chain.invoke({"input": query.text})
    return {"answer": response["answer"]}