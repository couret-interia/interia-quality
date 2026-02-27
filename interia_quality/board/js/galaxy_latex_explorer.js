function colorForScore(score) {
  // Simple gradient: blue → pink → purple
  const r = Math.floor(150 + score * 105);
  const g = Math.floor(80 + score * 20);
  const b = Math.floor(255 - score * 155);
  return `rgb(${r},${g},${b})`;
}

async function main() {
  let galaxy, summary;

  try { galaxy = await loadJSON("latex_galaxy.json"); }
  catch { document.getElementById("summary").textContent = "❌ latex_galaxy.json not found. Run `latex-explorer` (or `latex-galaxy`) first."; return; }

  try { summary = await loadJSON("latex_galaxy_summary.json"); }
  catch { summary = null; }

  const files = galaxy.files;
  const totalFiles = Object.keys(files).length;

  document.getElementById("summary").textContent =
    `Files: ${totalFiles} · Global score: ${summary ? summary.galaxy_score : "?"}`;

  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");

  const hoverInfo = document.getElementById("hover-info");

  // Compute ranges
  let maxSections = 1, maxLabels = 1;
  for (const stats of Object.values(files)) {
    maxSections = Math.max(maxSections, stats.sections);
    maxLabels = Math.max(maxLabels, stats.labels);
  }

  // Draw points
  const points = [];

  for (const [fname, stats] of Object.entries(files)) {
    const x = (stats.sections / maxSections) * (canvas.width - 50) + 25;
    const y = canvas.height - ((stats.labels / maxLabels) * (canvas.height - 50) + 25);

    const score = stats.score;
    const macro = stats.macros_used_total;
    const radius = Math.max(5, 4 + macro * 1.4);

    ctx.fillStyle = colorForScore(score);
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();

    points.push({ fname, x, y, radius, stats });
  }

  // Hover detection
  canvas.addEventListener("mousemove", e => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    for (const p of points) {
      const dx = mx - p.x;
      const dy = my - p.y;
      if (dx*dx + dy*dy <= p.radius * p.radius) {
        hoverInfo.innerHTML = `
          <b>${p.fname}</b><br>
          score=${p.stats.score}<br>
          sections=${p.stats.sections}, labels=${p.stats.labels}<br>
          macros used=${p.stats.macros_used_total}<br>
          citations=${p.stats.citations_total}
        `;
        return;
      }
    }

    hoverInfo.textContent = "Hover a file…";
  });
}
