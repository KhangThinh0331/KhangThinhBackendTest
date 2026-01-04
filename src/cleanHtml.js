const { JSDOM } = require("jsdom");

function cleanHtml(html) {
  const dom = new JSDOM(html);
  const document = dom.window.document;

  document.querySelectorAll(
    "nav, header, footer, .breadcrumbs, .article-sidebar"
  ).forEach(e => e.remove());

  return document.body.innerHTML;
}

module.exports = { cleanHtml };