const fs = require("fs");
const slugify = require("slugify");

function saveMarkdown(title, url, content) {
  const slug = slugify(title, { lower: true, strict: true });
  const path = `data/articles/${slug}.md`;

  const finalContent =
    `Article URL: ${url}\n\n` +
    content;

  fs.writeFileSync(path, finalContent, "utf8");
  return slug;
}
module.exports = { saveMarkdown };