function toggleSpinner(show) {
  // Toggle the visibility of loading spinner based on parameter
  document.getElementById("spinner").classList.toggle("hidden", !show);
}

function searchSongs() {
  const searchInput = document.getElementById("searchInput");

  // Ensure search input field exists before proceeding to prevent errors if the element is missing
  if (!searchInput) {
    console.error("Search input field not found!");
    return;
  }

  const query = searchInput.value.trim();

  toggleSpinner(true);

  fetch("http://localhost:5000/search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  })
    .then((response) => {
      // Check if the API response is successful
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      console.log("API Response:", data);
      displayResults(data.tracks_found || []);
      displayNotFound(data.tracks_not_found || []);
    })
    .catch((error) => {
      console.error("Error:", error);
      // Display error message in the results container if fetching fails
      document.getElementById(
        "results"
      ).innerHTML = `<p class="error">Failed to fetch results.</p>`;
    })
    .finally(() => toggleSpinner(false));
}

function displayResults(tracks) {
  const resultsContainer = document.getElementById("results");
  resultsContainer.innerHTML = "";

  // If no tracks are found, display appropriate message
  if (!Array.isArray(tracks) || tracks.length === 0) {
    resultsContainer.innerHTML = `<p class="no-results">No results found.</p>`;
    return;
  }

  tracks.forEach((track) => {
    const trackElement = document.createElement("div");
    trackElement.className = "track";

    // Construct track card with image, name, artist and Spotify link
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
          }" target="_blank" class="spotify-link" aria-label="Listen to ${
      track.name
    } on Spotify">Listen on Spotify</a>
        </div>
      </div>
    `;

    resultsContainer.appendChild(trackElement);
  });
}

function displayNotFound(notFound) {
  const notFoundContainer = document.getElementById("not-found");

  // Ensure section is hidden when empty
  if (!Array.isArray(notFound) || notFound.length === 0) {
    notFoundContainer.style.display = "none";
    return;
  }

  notFoundContainer.style.display = "block";

  notFoundContainer.innerHTML = `<p>The following songs were not found on Spotify:</p>`;

  const list = document.createElement("ul");
  notFound.forEach((song) => {
    const songItem = document.createElement("li");
    songItem.textContent = `🎵 ${song}`;
    list.appendChild(songItem);
  });

  notFoundContainer.appendChild(list);
}
