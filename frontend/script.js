// Define base API URLs for search and playlist suggestion endpoints
const API_BASE = "http://localhost:5000";
const API_SEARCH = `${API_BASE}/search`;
const API_SUGGEST = `${API_BASE}/suggest_playlists`;

// Grab DOM elements for UI updates
const spinner = document.getElementById("spinner");

function toggleSpinner(show) {
  spinner.classList.toggle("hidden", !show);
}

// Display error message in the UI
function displayErrorMessage(message) {
  // Display error message in the UI
  const errorMessageContainer = document.getElementById("error-message");
  errorMessageContainer.textContent = message;
  errorMessageContainer.style.display = "block";
  setTimeout(() => {
    errorMessageContainer.style.display = "none";
  }, 5000); // Clear message after 5 seconds
}

// Search for songs based on user input
function searchSongs() {
  // Search for songs based on user input
  const searchInput = document.getElementById("searchInput");
  const resultsContainer = document.getElementById("results");
  const notFoundContainer = document.getElementById("not-found");

  resultsContainer.innerHTML = "";
  notFoundContainer.style.display = "none";
  document.getElementById("error-message").style.display = "none";

  if (!searchInput) {
    console.error("Search input field not found!");
    return;
  }

  const query = searchInput.value.trim();

  if (!query) {
    displayErrorMessage("Please enter a search query.");
    return;
  }

  toggleSpinner(true);

  fetch(API_URL, {
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
      displayErrorMessage("Failed to fetch results. Please try again later.");
    })
    .finally(() => toggleSpinner(false));
}

// Display the search results in the UI
function displayResults(tracks) {
  // Display the search results in the UI
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
