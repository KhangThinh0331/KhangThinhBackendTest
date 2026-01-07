from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from prompt import SYSTEM_PROMPT
from dotenv import load_dotenv
load_dotenv()

def format_docs_with_sources(docs):
    docs_text = []
    urls = []

    for i, d in enumerate(docs, 1):
        docs_text.append(f"[Doc {i}]\n{d.page_content}")
        if "url" in d.metadata:
            urls.append(d.metadata["url"])

    return "\n\n".join(docs_text), list(set(urls))

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={"k": 8})

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    (
        "human",
        "Docs:\n{docs}\n\n"
        "URL:\n{urls}\n\n"
        "Question: {question}"
    )
])

while True:
    question = input("\nAsk OptiBot (type 'exit' to quit): ")

    if question.lower() in ["exit", "quit"]:
        break

    retrieved_docs = retriever.invoke(question)
    retrieved_docs = sorted(
        retrieved_docs,
        key=lambda d: d.metadata.get("chunk_index", 0)
    )
    docs_text, urls = format_docs_with_sources(retrieved_docs)

    response = llm.invoke(
        prompt.format(
            docs=docs_text,
            urls="\n".join(f"- {u}" for u in urls),
            question=question
        )
    )

    print("\nAnswer:\n")
    print(response.content)