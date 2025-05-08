// Define base API URLs for search and playlist suggestion endpoints
const API_BASE = "http://localhost:5000";
const API_SEARCH = `${API_BASE}/search`;
const API_SUGGEST = `${API_BASE}/suggest_playlists`;

// Grab DOM elements for UI updates
const spinner = document.getElementById("spinner");
const resultsContainer = document.getElementById("results");
const notFoundContainer = document.getElementById("not-found");
const errorMessageContainer = document.getElementById("error-message");
const suggestionsContainer = document.getElementById("playlistSuggestions");

/**
 * Show or hide the loading spinner
 * @param {boolean} show - Whether to display the spinner
 */
function toggleSpinner(show) {
  spinner.classList.toggle("hidden", !show);
}

/**
 * Display error message to user for a limited time
 * @param {string} message - Error message to display
 */
function displayError(message) {
  errorMessageContainer.textContent = message;
  errorMessageContainer.style.display = "block";
  setTimeout(() => (errorMessageContainer.style.display = "none"), 5000);
}

/**
 * Clear previous search results, errors and playlist suggestions from the DOM
 */
function clearContainers() {
  resultsContainer.innerHTML = "";
  notFoundContainer.innerHTML = "";
  notFoundContainer.style.display = "none";
  errorMessageContainer.style.display = "none";
  suggestionsContainer.innerHTML = "";
}

document.getElementById("searchForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const query = document.getElementById("searchInput").value.trim();
  if (!query) return displayError("Please enter a search query.");

  toggleSpinner(true);
  clearContainers();

  try {
    const res = await fetch(API_SEARCH, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
  } catch (err) {
    console.error(err);
  }
});

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

// Display songs that were not found
function displayNotFound(notFound) {
  // Display songs that were not found
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

// Event listener for getting playlist suggestions based on user vibe input
document
  .getElementById("suggestPlaylistButton")
  .addEventListener("click", function () {
    const vibe = document.getElementById("vibeInput").value.trim();
    if (!vibe) {
      displayErrorMessage("Please enter a vibe.");
      return;
    }

    fetch(
      `http://localhost:5000/suggest_playlists?vibe=${encodeURIComponent(vibe)}`
    )
      .then((response) => response.json())
      .then((data) => {
        const suggestionsContainer = document.getElementById(
          "playlistSuggestions"
        );
        suggestionsContainer.innerHTML = ""; // Clear previous suggestions
        if (data.playlists && data.playlists.length > 0) {
          data.playlists.forEach((playlist) => {
            const playlistElement = document.createElement("div");
            playlistElement.innerHTML = playlist.name;
            suggestionsContainer.appendChild(playlistElement);
          });
        } else {
          suggestionsContainer.innerHTML = "<p>No playlists found.</p>";
        }
      })
      .catch((error) => {
        console.error("Error fetching playlist suggestions:", error);
        displayErrorMessage("Failed to fetch playlist suggestions.");
      });
  });
