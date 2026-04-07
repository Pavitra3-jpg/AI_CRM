const API_BASE = "http://127.0.0.1:8000";

// -------------------------
// Mode Toggle
// -------------------------
const chatModeBtn = document.getElementById("chatModeBtn");
const formModeBtn = document.getElementById("formModeBtn");
const chatSection = document.getElementById("chatSection");
const formSection = document.getElementById("formSection");

chatModeBtn.addEventListener("click", () => {
  chatSection.classList.remove("hidden");
  formSection.classList.add("hidden");
  chatModeBtn.classList.add("active");
  formModeBtn.classList.remove("active");
});

formModeBtn.addEventListener("click", () => {
  formSection.classList.remove("hidden");
  chatSection.classList.add("hidden");
  formModeBtn.classList.add("active");
  chatModeBtn.classList.remove("active");
});

// -------------------------
// Extract with AI
// -------------------------
document.getElementById("extractBtn").addEventListener("click", async () => {
  const chatInput = document.getElementById("chatInput").value.trim();

  if (!chatInput) {
    alert("Please enter interaction details.");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: chatInput })
    });

    const data = await response.json();

    document.getElementById("chatResult").classList.remove("hidden");
    document.getElementById("aiOutput").textContent = JSON.stringify(data.structured_data, null, 2);

    // Autofill form fields
    fillForm(data.structured_data);

    // Switch to form mode automatically
    formSection.classList.remove("hidden");
    chatSection.classList.add("hidden");
    formModeBtn.classList.add("active");
    chatModeBtn.classList.remove("active");

    if (data.missing_fields && data.missing_fields.length > 0) {
      alert("Missing fields: " + data.missing_fields.join(", "));
    }

  } catch (error) {
    console.error(error);
    alert("Error while extracting data.");
  }
});

// -------------------------
// Fill Form
// -------------------------
function fillForm(data) {
  document.getElementById("hcp_name").value = data.hcp_name || "";
  document.getElementById("interaction_type").value = data.interaction_type || "";
  document.getElementById("product").value = data.product || "";
  document.getElementById("notes").value = data.notes || "";
  document.getElementById("sentiment").value = data.sentiment || "";
  document.getElementById("concerns").value = data.concerns || "";
  document.getElementById("follow_up").value = data.follow_up || "";
}

// -------------------------
// Save Interaction
// -------------------------
document.getElementById("saveBtn").addEventListener("click", async () => {
  const payload = {
    hcp_name: document.getElementById("hcp_name").value,
    interaction_type: document.getElementById("interaction_type").value,
    product: document.getElementById("product").value,
    notes: document.getElementById("notes").value,
    sentiment: document.getElementById("sentiment").value,
    concerns: document.getElementById("concerns").value,
    follow_up: document.getElementById("follow_up").value
  };

  if (!payload.hcp_name || !payload.interaction_type) {
    alert("HCP Name and Interaction Type are required.");
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/log-interaction`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    alert(data.message);

    clearForm();
    loadLogs();

  } catch (error) {
    console.error(error);
    alert("Error while saving interaction.");
  }
});

// -------------------------
// Clear Form
// -------------------------
function clearForm() {
  document.getElementById("hcp_name").value = "";
  document.getElementById("interaction_type").value = "";
  document.getElementById("product").value = "";
  document.getElementById("notes").value = "";
  document.getElementById("sentiment").value = "";
  document.getElementById("concerns").value = "";
  document.getElementById("follow_up").value = "";
  document.getElementById("chatInput").value = "";
}

// -------------------------
// Load Logs
// -------------------------
document.getElementById("loadLogsBtn").addEventListener("click", loadLogs);

async function loadLogs() {
  try {
    const response = await fetch(`${API_BASE}/interactions`);
    const data = await response.json();

    const container = document.getElementById("logsContainer");
    container.innerHTML = "";

    if (data.length === 0) {
      container.innerHTML = "<p>No interactions found.</p>";
      return;
    }

    data.forEach(item => {
      const div = document.createElement("div");
      div.className = "log-card";
      div.innerHTML = `
        <h4>${item.hcp_name} (${item.interaction_type})</h4>
        <p><strong>Product:</strong> ${item.product || "-"}</p>
        <p><strong>Sentiment:</strong> ${item.sentiment || "-"}</p>
        <p><strong>Notes:</strong> ${item.notes || "-"}</p>
        <p><strong>Concerns:</strong> ${item.concerns || "-"}</p>
        <p><strong>Follow-up:</strong> ${item.follow_up || "-"}</p>
      `;
      container.appendChild(div);
    });

  } catch (error) {
    console.error(error);
    alert("Error loading interactions.");
  }
}