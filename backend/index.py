import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

DATA_PATH = "../knowledge_base"
FAISS_PATH = "../faiss_index"

print("Loading documents...")

txt_loader = DirectoryLoader(
    DATA_PATH,
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)

pdf_loader = DirectoryLoader(
    DATA_PATH,
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)

txt_docs = txt_loader.load()
pdf_docs = pdf_loader.load()

docs = txt_docs + pdf_docs

print(f"Loaded {len(docs)} documents")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

docs = splitter.split_documents(docs)

print("Creating embeddings...")

# Changed: multilingual model that supports Arabic + English
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

db = FAISS.from_documents(docs, embeddings)

db.save_local(FAISS_PATH)

print("FAISS index created successfully!")