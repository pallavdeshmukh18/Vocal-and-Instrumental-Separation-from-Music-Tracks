import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [tracks, setTracks] = useState(null);

  const handleUpload = async () => {
    if (!file) return alert("Please choose a song!");
    setStatus("Processing... please wait 🎧");
    setTracks(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/separate", formData);
      setTracks(res.data.files);
      setStatus(res.data.message);
    } catch (err) {
      console.error(err);
      setStatus("❌ Error separating audio.");
    }
  };

  return (
    <div className="app-container">
      <h1>🎧 Vocal & Music Separator</h1>
      <p>Upload a song to extract vocals, drums, bass, and others using Demucs</p>

      <input
        type="file"
        accept="audio/*"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <br />
      <button onClick={handleUpload}>Start Separation</button>

      <p className="status-text">{status}</p>

      {tracks && (
        <div className="tracks-container">
          <div className="track-card">
            <h3>🎤 Vocals</h3>
            <audio controls src={tracks.vocals} />
          </div>

          <div className="track-card">
            <h3>🥁 Drums</h3>
            <audio controls src={tracks.drums} />
          </div>

          <div className="track-card">
            <h3>🎸 Bass</h3>
            <audio controls src={tracks.bass} />
          </div>

          <div className="track-card">
            <h3>🎶 Other</h3>
            <audio controls src={tracks.other} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
