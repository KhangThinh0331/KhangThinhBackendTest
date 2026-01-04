const axios = require("axios");

const BASE_URL =
  "https://support.optisigns.com/api/v2/help_center/en-us/articles.json";

async function pullArticles(limit = 30) {
  const articles = [];
  let page = 1;

  while (articles.length < limit) {
    const res = await axios.get(BASE_URL, {
      params: { page, per_page: 100 }
    });

    articles.push(...res.data.articles);
    if (!res.data.next_page) break;
    page++;
  }

  return articles.slice(0, limit);
}

module.exports = { pullArticles };