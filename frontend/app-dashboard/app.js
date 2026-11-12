const BACKEND_URL = "https://artemis-earth-detective.onrender.com";

const nasaVariables = {
  atmosphere: [
    "Air Temperature (Aqua/Aura)",
    "Surface Temperature",
    "Humidity",
    "Atmospheric Pressure",
    "Wind Speed",
    "Wind Direction",
    "Cloud Cover",
    "Cloud Height",
    "Aerosols",
    "Ozone",
    "Greenhouse Gases"
  ],
  precipitations: ["Rainfall (GPM)", "Precipitation Rate", "Snowfall", "Storm Frequency"],
  hydrologie: ["Soil Moisture", "Groundwater", "River Discharge", "Lake Extent", "Flood Extent", "Drought Index"],
  vegetation: ["NDVI", "EVI", "Biomass (GEDI)", "Forest Cover", "Vegetation Health", "Deforestation", "Carbon Storage", "Leaf Area Index"],
  landuse: ["Land Cover", "Land Use", "Urban Expansion", "Agriculture", "Bare Soil"],
  cryosphere: ["Snow Cover", "Ice Thickness", "Glacier Extent", "Sea Ice Extent", "Ice Elevation (ICESat-2)"],
  oceans: ["Sea Surface Temperature", "Sea Level (Jason-3)", "Ocean Color", "Chlorophyll", "Salinity", "Currents"],
  geodesie: ["Ground Deformation", "Vertical Displacement", "Land Subsidence", "Topography", "Elevation"]
};

let currentChatFile = null;

document.addEventListener("DOMContentLoaded", () => {
  initCategorySwitch();
  initAppEventListeners();
  initUploadButton();
});

function initCategorySwitch() {
  const categorySelect = document.getElementById("category-select");
  const variableSelect = document.getElementById("variable-select");

  if (!categorySelect || !variableSelect) {
    return;
  }

  const updateVariables = (category) => {
    variableSelect.innerHTML = "";

    (nasaVariables[category] || []).forEach((value) => {
      const option = document.createElement("option");
      option.value = value
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "_")
        .replace(/^_|_$/g, "");
      option.textContent = value;
      variableSelect.appendChild(option);
    });
  };

  categorySelect.addEventListener("change", (event) => {
    updateVariables(event.target.value);
  });

  updateVariables(categorySelect.value);
}

function appendLog(message, type = "info") {
  const logsTerminal = document.getElementById("console-logs");
  if (!logsTerminal) {
    return;
  }

  const row = document.createElement("p");
  row.className = `log-${type}`;
  row.textContent = message;
  logsTerminal.appendChild(row);
  logsTerminal.scrollTop = logsTerminal.scrollHeight;
}

function appendMessage(role, text) {
  const chatMessages = document.getElementById("chat-messages");
  if (!chatMessages) {
    return;
  }

  const message = document.createElement("div");
  message.className = `message ${role}`;
  message.innerHTML = text;
  chatMessages.appendChild(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function setMapState(mode, text) {
  const mapViewport = document.getElementById("map-viewport");
  if (!mapViewport) {
    return;
  }

  if (mode === "loading") {
    mapViewport.innerHTML = `
      <div class="map-placeholder">
        <div class="map-icon">◌</div>
        <p>${text}</p>
      </div>
    `;
    return;
  }

  if (mode === "success") {
    mapViewport.innerHTML = `
      <div class="map-placeholder">
        <div class="map-icon" style="color: var(--accent-green);">✓</div>
        <p>${text}</p>
      </div>
    `;
    return;
  }

  mapViewport.innerHTML = `
    <div class="map-placeholder">
      <div class="map-icon">◎</div>
      <p>${text}</p>
    </div>
  `;
}

function initUploadButton() {
  const uploadBtn = document.getElementById("chat-upload-btn");
  const fileInput = document.getElementById("chat-file-input");

  if (!uploadBtn || !fileInput) {
    return;
  }

  uploadBtn.addEventListener("click", () => {
    fileInput.click();
  });

  fileInput.addEventListener("change", async (e) => {
    if (e.target.files.length > 0) {
      currentChatFile = e.target.files;
      const filename = currentChatFile.name;
      appendLog(`> Fichier selectionne pour le chat : ${filename}`, "info");
      appendMessage("user", `<strong>Systeme :</strong> Fichier joint : ${filename}`);

      const formData = new FormData();
      formData.append("file", currentChatFile);

      try {
        const uploadResp = await fetch(`${BACKEND_URL}/chat/upload`, {
          method: "POST",
          body: formData
        });
        if (uploadResp.ok) {
          const uploadData = await uploadResp.json();
          appendMessage("assistant", `<strong>Artemis :</strong> ${uploadData.message}`);
          appendLog(`> [IA] Fichier ${filename} indexe en memoire.`, "success");
        }
      } catch (err) {
        console.error(err);
        appendLog("[Error] Echec de l'envoi du fichier au moteur IA.", "error");
      }
    }
  });
}

function initAppEventListeners() {
  const runBtn = document.getElementById("run-analysis-btn");
  if (runBtn) {
    runBtn.addEventListener("click", async () => {
      const categorySelect = document.getElementById("category-select");
      const variableSelect = document.getElementById("variable-select");
      const fileInput = document.getElementById("geo-file");
      const selectedVar = variableSelect?.options[variableSelect.selectedIndex]?.textContent || "Variable cible";
      const file = fileInput?.files?.[0];
      const filename = file ? file.name.toLowerCase() : "nasa_dataset_global.nc";
      const isMapData = /\.(tiff?|geojson|json|shp|nc)$/i.test(filename);

      appendLog(`> Ingestion de la variable : ${selectedVar}...`, "info");

      if (isMapData) {
        setMapState("loading", "Traitement de la matrice geographique...");
      } else {
        setMapState("default", "Donnees non cartographiques detectees.");
        appendLog("> [Pipeline] Format non-cartographique. Activation directe des modules graphiques et statistiques.", "info");
      }

      try {
        const response = await fetch(`${BACKEND_URL}/api/analyze`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            variable: selectedVar,
            category: categorySelect?.value || "atmosphere",
            is_map: isMapData,
            filename
          })
        });

        if (!response.ok) {
          throw new Error(`Erreur API : ${response.status}`);
        }

        const data = await response.json();

        document.getElementById("metric-output").innerHTML = `
          <p>Moyenne observee : <strong>${data.stats?.mean ?? "N/A"}</strong></p>
          <p>Variance / Ecart : <strong>${data.stats?.variance ?? "N/A"}</strong></p>
          <p class="status-inline">Statut : <strong>Donnees indexees</strong></p>
        `;

        document.getElementById("chart-output").innerHTML = `
          <p>${data.ai_expert_report || "Modelisation temporelle generee."}</p>
        `;

        if (isMapData) {
          setMapState("success", "Matrice spatiale injectee sur la carte.");
        }

        appendLog("> [IA] Analyse terminee.", "success");
        appendMessage(
          "assistant",
          `<strong>Artemis :</strong> Analyse terminee pour <em>${selectedVar}</em>. Posez-moi vos questions sur ces resultats.`
        );
      } catch (error) {
        console.error(error);
        appendLog("[Error] Probleme lors du traitement de la donnee par l'API.", "error");
        setMapState("default", "Le traitement a echoue, veuillez reessayer.");
      }
    });
  }

  const chatInput = document.getElementById("chat-input");
  const chatSendBtn = document.getElementById("chat-send-btn");

  if (!chatInput || !chatSendBtn) {
    return;
  }

  const submitChatMessage = async () => {
    const message = chatInput.value.trim();
    if (!message) {
      return;
    }

    appendMessage("user", `<strong>Vous :</strong> ${message}`);
    chatInput.value = "";

    try {
      const response = await fetch(`${BACKEND_URL}/chat/send_message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      if (!response.ok) {
        throw new Error(`Erreur chat : ${response.status}`);
      }

      const data = await response.json();
      const replyText = data.reply || data.analysis_result || data.response || "Je n'ai pas pu generer de reponse.";
      appendMessage("assistant", `<strong>Artemis :</strong> ${replyText}`);
    } catch (error) {
      console.error(error);
      appendMessage("assistant", "<strong>Artemis :</strong> Une erreur est survenue lors de la communication avec le serveur.");
    }
  };

  chatSendBtn.addEventListener("click", submitChatMessage);
  chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      submitChatMessage();
    }
  });
}