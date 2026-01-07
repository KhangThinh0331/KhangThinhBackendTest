from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import re


def extract_url(text: str):
    match = re.search(r"Article URL:\s*(https?://\S+)", text)
    return match.group(1) if match else None

loader = DirectoryLoader(
    "../data/articles",
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

docs = []

for doc in documents:
    url = extract_url(doc.page_content)
    if not url:
        continue

    chunks = splitter.split_text(doc.page_content)
    clean_url = url.split("#")[0]
    for chunk in chunks:
        docs.append(
            Document(
                page_content=chunk,
                metadata={"url": clean_url}
            )
        )

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_documents(docs, embeddings)
db.save_local("faiss_index")

print(f"Files loaded: {len(documents)}")
print(f"Chunks created: {len(docs)}")