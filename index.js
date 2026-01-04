const fs = require("fs");
const { pullArticles } = require("./src/zendesk");
const { cleanHtml } = require("./src/cleanHTML");
const { htmlToMarkdown } = require("./src/toMarkdown");
const { saveMarkdown } = require("./src/saveFile");

fs.mkdirSync("data/articles", { recursive: true });

async function run() {
  const articles = await pullArticles(30);

  let count = 0;
  for (const article of articles) {
    const cleaned = cleanHtml(article.body);
    const md = htmlToMarkdown(cleaned);
    saveMarkdown(article.title, md);
    count++;
  }

  console.log(`Saved ${count} articles`);
}

run();