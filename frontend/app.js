const HISTORY_PATH = "../output/history.json";

// Loads history.json and kicks off rendering, or shows an error message.
async function loadHistory() {
  const status = document.getElementById("status");
  try {
    const response = await fetch(HISTORY_PATH);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const history = await response.json();
    status.remove();
    renderTimeline(history);
  } catch (err) {
    status.textContent = `Could not load ${HISTORY_PATH}: ${err.message}`;
  }
}

// history: list of pass dicts from history_builder.py. Renders one card per pass.
function renderTimeline(history) {
  const container = document.getElementById("timeline");
  if (history.length === 0) {
    container.innerHTML = "<p>No passes recorded.</p>";
    return;
  }
  history.forEach((entry) => container.appendChild(buildPassCard(entry)));
}

// entry: one pass dict. Returns a clickable card element for the timeline.
function buildPassCard(entry) {
  const card = document.createElement("div");
  card.className = "pass-card";

  const header = document.createElement("div");
  header.className = "pass-header";
  header.innerHTML = `
    <div>
      <span class="pass-name">${entry.pass_name}</span>
      <span class="pass-function">on ${entry.function}</span>
    </div>
    <span class="pass-arrow">&#9654;</span>
  `;
  header.addEventListener("click", () => card.classList.toggle("open"));

  const details = document.createElement("div");
  details.className = "pass-details";
  details.appendChild(buildDescription(entry.description));
  details.appendChild(buildMetricsTable(entry.metrics_before, entry.metrics_after));
  details.appendChild(buildDiffBox(entry.diff));

  card.appendChild(header);
  card.appendChild(details);
  return card;
}

// text: plain-English pass description. Returns a paragraph element.
function buildDescription(text) {
  const p = document.createElement("p");
  p.className = "description";
  p.textContent = text;
  return p;
}

// before, after: metric count dicts. Returns a table comparing each metric.
function buildMetricsTable(before, after) {
  const table = document.createElement("table");
  table.className = "metrics-table";
  table.innerHTML = "<tr><th>Metric</th><th>Before</th><th>After</th></tr>";

  Object.keys(before).forEach((key) => {
    const changed = before[key] !== after[key];
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${key}</td>
      <td class="${changed ? "changed" : ""}">${before[key]}</td>
      <td class="${changed ? "changed" : ""}">${after[key]}</td>
    `;
    table.appendChild(row);
  });
  return table;
}

// diffLines: list of unified-diff text lines. Returns a color-coded diff box.
function buildDiffBox(diffLines) {
  const box = document.createElement("div");
  box.className = "diff-box";

  if (diffLines.length === 0) {
    box.textContent = "No line-level diff available.";
    return box;
  }

  diffLines.forEach((line) => {
    const div = document.createElement("div");
    div.className = "diff-line " + classifyDiffLine(line);
    div.textContent = line;
    box.appendChild(div);
  });
  return box;
}

// line: one diff line. Returns the CSS class matching its diff symbol.
function classifyDiffLine(line) {
  if (line.startsWith("+")) return "diff-added";
  if (line.startsWith("-")) return "diff-removed";
  if (line.startsWith("@")) return "diff-hunk";
  return "diff-context";
}

loadHistory();