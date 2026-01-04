const TurndownService = require("turndown");

const turndown = new TurndownService({
  codeBlockStyle: "fenced",
  headingStyle: "atx"
});

function htmlToMarkdown(html) {
  return turndown.turndown(html);
}

module.exports = { htmlToMarkdown };