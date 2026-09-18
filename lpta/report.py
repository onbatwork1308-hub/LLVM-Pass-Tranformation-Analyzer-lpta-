import json
import webbrowser
from pathlib import Path

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>LPTA — Transformation Report</title>
<style>
body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; background: #0f1115; color: #e6e6e6; margin: 0; padding: 2rem; }
header { margin-bottom: 1.5rem; }
h1 { margin: 0; font-size: 1.6rem; }
.subtitle { color: #9aa0a6; margin: 0.3rem 0 0; }
#page { max-width: 900px; margin: 0 auto; }

.summary-bar { display: flex; gap: 0.8rem; margin-bottom: 1.2rem; flex-wrap: wrap; }
.stat { flex: 1; min-width: 140px; background: #171a21; border: 1px solid #2a2d34; border-radius: 8px; padding: 0.8rem 1rem; }
.stat-value { font-size: 1.4rem; font-weight: 700; }
.stat-value.positive { color: #ff7b72; }
.stat-value.negative { color: #7ee787; }
.stat-label { color: #9aa0a6; font-size: 0.78rem; margin-top: 0.2rem; }

.chart-box { background: #171a21; border: 1px solid #2a2d34; border-radius: 8px; padding: 1rem; margin-bottom: 1.2rem; }
.chart-title { font-size: 0.85rem; color: #9aa0a6; margin-bottom: 0.6rem; }
.chart-line { fill: none; stroke: #79c0ff; stroke-width: 2; }
.chart-point { fill: #79c0ff; }
.chart-axis { stroke: #2a2d34; stroke-width: 1; }

.pass-card { border: 1px solid #2a2d34; border-radius: 8px; margin-bottom: 0.8rem; overflow: hidden; background: #171a21; }
.pass-header { display: flex; justify-content: space-between; align-items: center; padding: 0.9rem 1.1rem; cursor: pointer; }
.pass-header:hover { background: #1d212a; }
.pass-name { font-weight: 600; font-size: 1rem; }
.pass-function { color: #9aa0a6; font-size: 0.85rem; margin-left: 0.5rem; }
.pass-arrow { color: #9aa0a6; transition: transform 0.15s ease; }
.pass-card.open .pass-arrow { transform: rotate(90deg); }
.pass-details { display: none; padding: 0 1.1rem 1.1rem; border-top: 1px solid #2a2d34; }
.pass-card.open .pass-details { display: block; }
.description { color: #c7c9cc; margin: 0.8rem 0; }
.metrics-table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; font-size: 0.85rem; }
.metrics-table th, .metrics-table td { text-align: left; padding: 0.35rem 0.6rem; border-bottom: 1px solid #2a2d34; }
.metrics-table .changed { color: #f2b84b; font-weight: 600; }
.diff-box { background: #0b0d11; border: 1px solid #2a2d34; border-radius: 6px; padding: 0.6rem 0.8rem; overflow-x: auto; font-family: "Courier New", monospace; font-size: 0.82rem; line-height: 1.4; }
.diff-line { white-space: pre; }
.diff-added { color: #7ee787; }
.diff-removed { color: #ff7b72; }
.diff-hunk { color: #79c0ff; }
.diff-context { color: #9aa0a6; }
</style>
</head>
<body>
<div id="page">
<header>
  <h1>LPTA Transformation Timeline</h1>
  <p class="subtitle">Click a pass to see its metrics and code diff</p>
</header>
<div id="summary"></div>
<div id="chart"></div>
<main id="timeline"></main>
</div>

<script>
const HISTORY = __HISTORY_JSON__;

function renderReport(history) {
  document.getElementById("summary").appendChild(buildSummaryBar(history));
  if (history.length > 0) {
    document.getElementById("chart").appendChild(buildTrendChart(history));
  }
  renderTimeline(history);
}

// history: full pass list. returns: a row of stat boxes summarizing the whole pipeline.
function buildSummaryBar(history) {
  const bar = document.createElement("div");
  bar.className = "summary-bar";

  if (history.length === 0) {
    bar.appendChild(makeStat(0, "Passes Analyzed"));
    return bar;
  }

  const firstInstr = history[0].metrics_before.instructions;
  const lastInstr = history[history.length - 1].metrics_after.instructions;
  const netChange = lastInstr - firstInstr;
  const increased = history.filter(e => e.metrics_after.instructions > e.metrics_before.instructions).length;
  const decreased = history.filter(e => e.metrics_after.instructions < e.metrics_before.instructions).length;

  bar.appendChild(makeStat(history.length, "Passes Analyzed"));
  bar.appendChild(makeStat(firstInstr + " \u2192 " + lastInstr, "Instructions (start \u2192 end)"));
  bar.appendChild(makeStat((netChange > 0 ? "+" : "") + netChange, "Net Instruction Change", netChange));
  bar.appendChild(makeStat(increased + " up / " + decreased + " down", "Passes That Changed Size"));
  return bar;
}

// value: text or number to show big. label: caption below it. changeValue: optional number to color it by sign.
function makeStat(value, label, changeValue) {
  const box = document.createElement("div");
  box.className = "stat";
  const valueClass = changeValue > 0 ? "positive" : changeValue < 0 ? "negative" : "";
  box.innerHTML = `
    <div class="stat-value ${valueClass}">${value}</div>
    <div class="stat-label">${label}</div>
  `;
  return box;
}

// history: full pass list. returns: an SVG line chart of instruction count across the pipeline.
function buildTrendChart(history) {
  const box = document.createElement("div");
  box.className = "chart-box";

  const points = [history[0].metrics_before.instructions, ...history.map(e => e.metrics_after.instructions)];
  const width = 840, height = 140, padding = 20;
  const minVal = Math.min(...points), maxVal = Math.max(...points);
  const range = maxVal - minVal || 1;

  const coords = points.map((val, i) => {
    const x = padding + (i / (points.length - 1)) * (width - 2 * padding);
    const y = height - padding - ((val - minVal) / range) * (height - 2 * padding);
    return [x, y];
  });

  const pathData = coords.map(([x, y], i) => (i === 0 ? "M" : "L") + x + "," + y).join(" ");
  const circles = coords.map(([x, y], i) => {
    const label = i === 0 ? "Start: " + points[i] : history[i - 1].pass_name + ": " + points[i];
    return `<circle class="chart-point" cx="${x}" cy="${y}" r="3"><title>${label}</title></circle>`;
  }).join("");

  box.innerHTML = `
    <div class="chart-title">Instruction count across the pipeline</div>
    <svg viewBox="0 0 ${width} ${height}" width="100%">
      <line class="chart-axis" x1="${padding}" y1="${height - padding}" x2="${width - padding}" y2="${height - padding}" />
      <path class="chart-line" d="${pathData}" />
      ${circles}
    </svg>
  `;
  return box;
}

function renderTimeline(history) {
  const container = document.getElementById("timeline");
  if (history.length === 0) {
    container.innerHTML = "<p>No passes recorded.</p>";
    return;
  }
  history.forEach((entry) => container.appendChild(buildPassCard(entry)));
}

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

function buildDescription(text) {
  const p = document.createElement("p");
  p.className = "description";
  p.textContent = text;
  return p;
}

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

function classifyDiffLine(line) {
  if (line.startsWith("+")) return "diff-added";
  if (line.startsWith("-")) return "diff-removed";
  if (line.startsWith("@")) return "diff-hunk";
  return "diff-context";
}

renderReport(HISTORY);
</script>
</body>
</html>
"""


def render_report(history: list[dict]) -> str:
    """history: list of pass dicts. returns: complete HTML report as one string, data embedded inline."""
    return TEMPLATE.replace("__HISTORY_JSON__", json.dumps(history))


def save_report(html: str, output_path: Path = Path("output/report.html")) -> Path:
    """html: report content. output_path: where to save. returns: the path written to."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
    return output_path


def open_report(path: Path) -> None:
    """path: report file to open. opens it in the system's default browser."""
    webbrowser.open(f"file://{path.resolve()}")
