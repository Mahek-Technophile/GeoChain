// frontend/script.js

async function sendQuery() {
  const query = document.getElementById("query").value;

  const response = await fetch("http://localhost:8000/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  const data = await response.json();

  // Show logs
  document.getElementById("log").textContent = data.log;

  // Show steps
  const stepList = document.getElementById("steps");
  stepList.innerHTML = "";
  data.workflow_steps.forEach((s, i) => {
    const item = document.createElement("li");
    item.textContent = `Step ${i+1}: ${s.step} (${s.tool})`;
    stepList.appendChild(item);
  });

  // Show map
  document.getElementById("map").innerHTML = ""; // Clear previous map
  const map = L.map("map").setView([19.0760, 72.8777], 10); // Mumbai
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
  L.marker([19.0760, 72.8777]).addTo(map).bindPopup("Flood Risk Area (Example)").openPopup();
}
