# OptiBot Mini-Clone

## Overview
This project scrapes help articles from support.optisigns.com and converts them into clean Markdown files for use in an OpenAI Vector Store.

## Scrape ⇒ Markdown
- Pulls articles from support.optisigns.com via Zendesk Help Center API
- Retrieves at least 30 articles
- Removes navigation, footer, and non-article elements
- Converts HTML content into clean Markdown
- Saves each article as a separate `<slug>.md` file

## Tech Stack
- Node.js
- Axios (Zendesk API requests)
- JSDOM (HTML parsing & cleanup)
- Turndown (HTML → Markdown)
- Slugify (generate URL-safe filenames)

## How to Run Locally
```bash
npm install
node index.js
Markdown files will be generated in `data/articles/`