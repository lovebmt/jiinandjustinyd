const assert = require("assert");
const fs = require("fs");
const vm = require("vm");

const html = fs.readFileSync("index.html", "utf8");
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
assert(scriptMatch, "index.html must include an inline script");

const script = scriptMatch[1];
const start = script.indexOf("function escapeHtml");
const end = script.indexOf("async function loadMarkdown");
assert(start >= 0, "renderer helpers must be present");
assert(end > start, "loadMarkdown must appear after renderer helpers");

const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(script.slice(start, end), sandbox);

const markdown = [
  "| STT | Tên hình | Vị trí |",
  "|---|---|---|",
  "| 1 | Hình 1.1 | Chương 1 |",
  "| 2 | Biểu đồ 2.1 | Chương 2 |",
].join("\n");

const rendered = sandbox.renderMarkdown(markdown);

assert(
  rendered.includes("<table>"),
  `expected markdown table to render as <table>, got:\n${rendered}`
);
assert(rendered.includes("<thead>"), "expected rendered table to include <thead>");
assert(rendered.includes("<tbody>"), "expected rendered table to include <tbody>");
assert(rendered.includes("<th>STT</th>"), "expected header cells to render");
assert(rendered.includes("<td>Hình 1.1</td>"), "expected body cells to render");
