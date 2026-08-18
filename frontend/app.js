const API_BASE_URL = "/api/v1";

const form = document.querySelector("#search-form");
const queryInput = document.querySelector("#query");
const emptyState = document.querySelector("#empty-state");
const status = document.querySelector("#status");
const resultsList = document.querySelector("#results-list");
const template = document.querySelector("#result-template");

function setStatus(message, isError = false) {
  status.hidden = !message;
  status.textContent = message;
  status.classList.toggle("error", isError);
}

function addTag(container, text) {
  if (!text) return;
  const tag = document.createElement("span");
  tag.className = "tag";
  tag.textContent = text;
  container.append(tag);
}

function renderResults(results) {
  resultsList.replaceChildren();
  if (!results.length) {
    setStatus("No matching passages found. Try different wording.");
    return;
  }

  setStatus(`${results.length} relevant passage${results.length === 1 ? "" : "s"} found.`);
  for (const result of results) {
    const card = template.content.cloneNode(true);
    const metadata = result.metadata || {};
    card.querySelector(".source").textContent = metadata.document_title || metadata.document_name || "Legal corpus";
    card.querySelector(".score").textContent = `${Math.round((result.score || 0) * 100)}% match`;
    card.querySelector(".result-title").textContent = metadata.title || result.chunk_type || "Relevant passage";
    card.querySelector(".result-text").textContent = result.text || "No passage text is available.";
    const tags = card.querySelector(".tags");
    addTag(tags, result.chunk_type);
    addTag(tags, metadata.article && `Article ${metadata.article}`);
    addTag(tags, metadata.section && `Section ${metadata.section}`);
    addTag(tags, metadata.jurisdiction);
    resultsList.append(card);
  }
}

async function search(query) {
  emptyState.hidden = true;
  resultsList.replaceChildren();
  setStatus("Searching the legal corpus…");
  try {
    const response = await fetch(`${API_BASE_URL}/search?${new URLSearchParams({ query, limit: "8" })}`);
    if (!response.ok) throw new Error(response.status === 503 ? "The search service is unavailable. Start Qdrant and index the corpus first." : "Search could not be completed.");
    renderResults(await response.json());
  } catch (error) {
    setStatus(error.message, true);
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  search(queryInput.value.trim());
});

document.querySelectorAll("[data-query]").forEach((button) => {
  button.addEventListener("click", () => {
    queryInput.value = button.dataset.query;
    search(queryInput.value);
  });
});
