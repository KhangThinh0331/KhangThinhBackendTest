## Scrape ⇒ Markdown
- Pulls articles from support.optisigns.com via Zendesk Help Center API
- Retrieves at least 30 articles
- Removes navigation, footer, and non-article elements
- Converts HTML content into clean Markdown
- Saves each article as a separate `<slug>.md` file

**Tech Stack:**

- Node.js
- Axios (Zendesk API requests)
- JSDOM (HTML parsing & cleanup)
- Turndown (HTML → Markdown)
- Slugify (generate URL-safe filenames)

## Build Assistant & Programmatically Load Vector Store

**RAG Pipeline:**

1. Markdown articles are loaded and chunked
2. Text chunks are embedded using Sentence Transformers
3. Embeddings are stored in a FAISS vector database
4. User questions retrieve relevant chunks
5. A Groq-hosted LLM generates answers using retrieved context

**Chunking Strategy:**

- Documents are split into chunks of 500 characters
- Overlap of 100 characters is used to preserve context across chunks

**Tech Stack:**

- **Language:** Python 3.13.5
- **LLM:** Groq (Llama 3)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Database:** FAISS
- **Framework:** LangChain

**Sanity Check Result:**

The assistant correctly answered the test question using retrieved documentation.

![Playground Answer Screenshot](screenshots/playground_answer.png)

## Deploy Scraper as Daily Job

**Pull Docker Image:**

```bash
docker pull khangthinh/mynode-python-app
```

**Run Node.js ingestion (pull articles and build FAISS index):**

```bash
docker run -it -e GROQ_API_KEY="..." -v D:/faiss_index:/app/faiss_index khangthinh/mynode-python-app
```

**Run Chatbot:**

```bash
docker run -it -e GROQ_API_KEY="..." -v D:/faiss_index:/app/faiss_index khangthinh/mynode-python-app python3 python/query.py
```

**Daily Job:**

- Runs automatically once per day using GitHub Actions