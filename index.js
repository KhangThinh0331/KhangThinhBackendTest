const { pullArticles } = require("./src/zendesk");
const { cleanHtml } = require("./src/cleanHtml");
const { htmlToMarkdown } = require("./src/toMarkdown");
const { saveMarkdown } = require("./src/saveFile");
const { detectDelta, saveState } = require("./src/delta");
const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

async function run() {
  fs.mkdirSync("data/articles", { recursive: true });
  fs.mkdirSync("state", { recursive: true });

  const articles = await pullArticles(400);
  const { added, updated, skipped, state } = detectDelta(articles);

  for (const a of [...added, ...updated]) {
    const cleaned = cleanHtml(a.body);
    const md = htmlToMarkdown(cleaned);
    saveMarkdown(a.title, a.html_url, md);
  }

  saveState(state);

  const pythonFolder = path.join(__dirname, "python");
  fs.readdirSync(pythonFolder)
    .filter(f => f.endsWith(".py") && f !== "query.py")
    .forEach(file => {
      console.log(`Running ${file}...`);
      execSync(`python3 ${file}`, { stdio: "inherit", cwd: pythonFolder });
    });

  const summary = {
    run_at: new Date().toISOString(),
    fetched: articles.length,
    added: added.length,
    updated: updated.length,
    skipped: skipped.length
  };

  fs.mkdirSync("logs", { recursive: true });
  fs.writeFileSync("logs/last_run.json", JSON.stringify(summary, null, 2));

  console.log("Run:", summary);
}

run();