const fs = require("fs");

const STATE_FILE = "state.json";

function loadState() {
  if (!fs.existsSync(STATE_FILE)) return {};
  return JSON.parse(fs.readFileSync(STATE_FILE));
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function detectDelta(articles) {
  const oldState = loadState();
  const newState = {};

  const added = [];
  const updated = [];
  const skipped = [];

  for (const a of articles) {
    const id = String(a.id);
    newState[id] = a.updated_at;

    if (!oldState[id]) added.push(a);
    else if (oldState[id] !== a.updated_at) updated.push(a);
    else skipped.push(a);
  }

  return { added, updated, skipped, state: newState };
}

module.exports = { detectDelta, saveState };