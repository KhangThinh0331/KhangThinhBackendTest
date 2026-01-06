from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from prompt import SYSTEM_PROMPT
from dotenv import load_dotenv
load_dotenv()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={"k": 3})

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    (
        "human",
        "Docs:\n{docs}\n\n"
        "Question: {question}"
    )
])

rag_chain = (
    {
        "docs": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
)

while True:
    question = input("\nAsk OptiBot (type 'exit' to quit): ")

    if question.lower() in ["exit", "quit"]:
        break

    response = rag_chain.invoke(question)

    docs = retriever.invoke(question)
    urls = {d.metadata["url"] for d in docs if "url" in d.metadata}

    print("\nAnswer:\n")
    print(response.content)