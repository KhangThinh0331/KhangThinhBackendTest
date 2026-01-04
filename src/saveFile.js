const fs = require("fs");
const slugify = require("slugify");

function saveMarkdown(title, content) {
  const slug = slugify(title, { lower: true, strict: true });
  const path = `data/articles/${slug}.md`;

  fs.writeFileSync(path, content, "utf8");
  return slug;
}
module.exports = { saveMarkdown };