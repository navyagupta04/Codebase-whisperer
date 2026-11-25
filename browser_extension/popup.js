const repoNode = document.getElementById("repo");
const statusNode = document.getElementById("status");
const analyseButton = document.getElementById("analyse");
let repositoryUrl = null;

function publicRepoFromUrl(url) {
  try {
    const parsed = new URL(url);
    if (parsed.hostname !== "github.com") return null;
    const parts = parsed.pathname.split("/").filter(Boolean);
    if (parts.length < 2) return null;
    return `https://github.com/${parts[0]}/${parts[1].replace(/\.git$/, "")}`;
  } catch {
    return null;
  }
}

chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  repositoryUrl = publicRepoFromUrl(tabs[0]?.url ?? "");
  if (!repositoryUrl) {
    repoNode.textContent = "Open a public GitHub repository to get started.";
    return;
  }
  repoNode.textContent = repositoryUrl.replace("https://github.com/", "");
  analyseButton.disabled = false;
});

analyseButton.addEventListener("click", async () => {
  if (!repositoryUrl) return;
  analyseButton.disabled = true;
  statusNode.textContent = "Sending repository to the local workspace…";
  try {
    const response = await fetch("http://localhost:8000/repositories/analyse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: repositoryUrl }),
    });
    const result = await response.json();
    statusNode.textContent = result.message ?? `Repository status: ${result.status}`;
  } catch {
    statusNode.textContent = "Could not reach the API. Start the local FastAPI server and try again.";
  } finally {
    analyseButton.disabled = false;
  }
});
