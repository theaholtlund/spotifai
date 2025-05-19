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

// Handle search form submission
document.getElementById("searchForm").addEventListener("submit", async (e) => {
  e.preventDefault(); // Prevent page reload on form submit
  const query = document.getElementById("searchInput").value.trim(); // Get user input
  if (!query) return displayError("Please enter a search query.");

  toggleSpinner(true); // Show loading spinner
  clearContainers(); // Clear previous results

  try {
    // Send POST request to search endpoint with the query
    const res = await fetch(API_SEARCH, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    if (!res.ok) throw new Error(`HTTP error: ${res.status}`);

    // Parse the JSON response
    const data = await res.json();
    renderResults(data.tracks_found); // Display found tracks
    renderNotFound(data.tracks_not_found); // Display not found tracks
  } catch (err) {
    console.error(err);
    displayError("Failed to fetch results. Try again later.");
  } finally {
    toggleSpinner(false); // Hide spinner regardless of success/failure
  }
});

/**
 * Render the list of found tracks to the results container
 * @param {Array} tracks - Array of track objects found from the search
 */
function renderResults(tracks = []) {
  if (!tracks.length) {
    resultsContainer.innerHTML = '<p class="no-results">No results found.</p>';
    return;
  }

  tracks.forEach((track) => {
    const el = document.createElement("div");
    el.className = "track-card";

    // Create a card with album image, name, artist(s) and Spotify link
    el.innerHTML = `
      <img src="${track.album?.images[0]?.url || ""}" alt="${
      track.name
    }" class="track-image">
      </div>
    `;
    resultsContainer.appendChild(el); // Add track card to DOM
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
  notFoundContainer.innerHTML =
    "<p>The following songs were not found on Spotify:</p>";

  const list = document.createElement("ul");
  notFound.forEach((song) => {
    const item = document.createElement("li");
    item.textContent = ` ${song}`;
    list.appendChild(item);
  });
  notFoundContainer.appendChild(list); // Add the list to the DOM
}

// Handle click event for playlist suggestion button
document
  .getElementById("suggestPlaylistButton")
  .addEventListener("click", function () {
    const vibe = document.getElementById("vibeInput").value.trim();

    const res = await fetch(`${API_SUGGEST}?vibe=${encodeURIComponent(vibe)}`);
    const data = await res.json();

    data.playlists.forEach((p) => {
      const el = document.createElement("div");
      el.className = "playlist-suggestion-item";
      el.innerHTML = `<a href="${p.external_urls.spotify}" target="_blank">${p.name}</a>`;
      suggestionsContainer.appendChild(el);
    });
  });
