function generatePlaylist() {
  const prompt = document.getElementById("prompt").value;
  console.log("Sending prompt:", prompt);
  fetch("http://localhost:5000/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Response data:", data);
      document.getElementById(
        "output"
      ).innerText = `Playlist Created: ${data.description}`;
    })
    .catch((error) => {
      console.error("Error:", error);
      document.getElementById("output").innerText =
        "Failed to create playlist.";
    });
}
