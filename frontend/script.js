function toggleSpinner(show) {
  document.getElementById("spinner").classList.toggle("hidden", !show);
}

function searchSongs() {
  const searchInput = document.getElementById("searchInput");

  if (!searchInput) {
    console.error("Search input field not found!");
    return;
  }

  const query = searchInput.value.trim();

  if (!query) {
    alert("Please enter a search term.");
    return;
  }

  toggleSpinner(true);

  fetch("http://localhost:5000/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: query }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      console.log("API Response:", data); // Debugging API response
      displayResults(data.tracks || []);
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById(
        "results"
      ).innerHTML = `<p class="error">Failed to fetch results.</p>`;
    })
    .finally(() => toggleSpinner(false));
}

function displayResults(tracks) {
  const resultsContainer = document.getElementById("results");
  resultsContainer.innerHTML = ""; // Clear previous results

  if (!Array.isArray(tracks) || tracks.length === 0) {
    resultsContainer.innerHTML = `<p>No results found.</p>`;
    return;
  }

  tracks.forEach((track) => {
    const trackElement = document.createElement("div");
    trackElement.className = "track";

    trackElement.innerHTML = `
      <div class="track-card">
        <img src="${track.album?.images[0]?.url || ""}" alt="${
      track.name
    }" class="track-image">
        <div class="track-details">
          <h3>${track.name}</h3>
          <p><strong>Artist:</strong> ${track.artists
            .map((artist) => artist.name)
            .join(", ")}</p>
          <a href="${
            track.external_urls?.spotify || "#"
          }" target="_blank" class="spotify-link">Listen on Spotify</a>
        </div>
      </div>
    `;

    resultsContainer.appendChild(trackElement);
  });
}

function displayNotFound(notFound) {
  const notFoundContainer = document.getElementById("not-found");

  if (!Array.isArray(notFound) || notFound.length === 0) {
    notFoundContainer.style.display = "none"; // Hide if no songs are missing
    return;
  }
}
