const enhanceApi = (path, options = {}) => fetch(`${window.PANINI_API_URL || "http://127.0.0.1:8000"}${path}`, { headers: { "Content-Type": "application/json" }, ...options }).then((response) => { if (!response.ok) throw new Error("Request failed"); return response.json(); });
const enhance = (selector) => document.querySelector(selector);

async function renderAtlasDetails() {
  const renderGraph = async () => {
    const graph = await enhanceApi("/graph");
    enhance("#graph").innerHTML = graph.nodes.map((node) => `<div class="graph-node">${node.sutra}<small>${node.name}</small></div>`).join("");
    enhance("#graph-edges").innerHTML = graph.edges.map((edge) => `<div class="edge"><span>${edge.source}</span><b>${edge.relation.replace("_", " ")}</b><span>${edge.target}</span></div>`).join("");
  };
  const renderInteractions = async () => {
    const interactions = await enhanceApi("/interactions");
    enhance("#interactions").innerHTML = interactions.interactions.map((item) => `<div class="interaction"><span>${item.source}</span><b>${item.relation.replace("_", " ")}</b><span>${item.target}</span></div>`).join("") || "<div class='empty-state'>No observed interactions.</div>";
  };
  const renderImpact = async () => {
    const impact = await enhanceApi("/impact", { method: "POST", body: JSON.stringify({ input_surfaces: ["अइ", "इअ", "अए", "तश", "मक"] }) });
    enhance("#impact").innerHTML = impact.rules.map((item) => `<div class="impact-row"><b>#${item.impact_rank}</b><span>${item.sutra}<div class="impact-bar"><i style="width:${item.output_change_rate * 100}%"></i></div></span><b>${Math.round(item.output_change_rate * 100)}%</b></div>`).join("");
  };
  const tasks = [[renderGraph, "#graph"], [renderInteractions, "#interactions"], [renderImpact, "#impact"]];
  await Promise.all(tasks.map(async ([task, target]) => {
    try {
      await task();
    } catch (error) {
      const element = enhance(target);
      if (element) element.innerHTML = `<div class="empty-state">${error.message}. Check that the API is running.</div>`;
    }
  }));
}

async function renderExperimentDetails() {
  const disabled = [...document.querySelectorAll('input[name="experiment-rule"]:not(:checked)')].map((input) => input.value);
  if (!disabled.length) return;
  try {
    const data = await enhanceApi("/experiment", { method: "POST", body: JSON.stringify({ input_surface: enhance("#surface").value.trim() || "अइ", disabled_rules: disabled }) });
    const trace = (steps, label) => `<div class="trace-mini"><span>${label}</span>${steps.map((step) => `<b>${step.rule_id}<i>${step.after_surface}</i></b>`).join("") || "<small>no rules fired</small>"}</div>`;
    enhance("#comparison-content").insertAdjacentHTML("beforeend", `${trace(data.baseline_trace, "BASELINE")}${trace(data.counterfactual_trace, "COUNTERFACTUAL")}`);
  } catch (_) { /* The primary experiment handler already reports the error. */ }
}

document.querySelector('[data-view="atlas"]').addEventListener("click", renderAtlasDetails, true);
document.querySelector("#experiment-btn").addEventListener("click", renderExperimentDetails);