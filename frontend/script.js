function searchSongs() {
  const searchInput = document.getElementById("searchInput");

  if (!searchInput) {
    console.error("Search input field not found!");
    return;
  }

  const query = searchInput.value.trim();
  if (!query) {
    console.error("Query cannot be empty");
    return;
  }

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
      console.log("Search Results:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
