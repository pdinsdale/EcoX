import React, { useEffect, useState } from "react";
import axios from "axios";
import "./../App.css";
import styles from './Camera.module.css'

function Camera() {
  const [images, setImages] = useState([]);
  const [cameraOn, setCameraOn] = useState(false); // Track camera state

  // Function to fetch saved images from Flask
  const fetchImages = () => {
    axios.get("http://127.0.0.1:8080/detections")
      .then(response => {
        setImages(response.data.images);
      })
      .catch(error => {
        console.error("Error fetching images:", error);
      });
  };

  // Fetch images initially and every 2 seconds
  useEffect(() => {
    fetchImages();
    const interval = setInterval(fetchImages, 2000);
    return () => clearInterval(interval);
  }, []);

  // Start Camera
  const startCamera = () => {
    axios.get("http://127.0.0.1:8080/start_camera")
      .then(() => {
        setCameraOn(true);
      })
      .catch(error => {
        console.error("Error starting camera:", error);
      });
  };

  // Stop Camera
  const stopCamera = () => {
    axios.get("http://127.0.0.1:8080/stop_camera")
      .then(() => {
        setCameraOn(false);
      })
      .catch(error => {
        console.error("Error stopping camera:", error);
      });
  };

  return (
    <div className="App" style={{ display: "flex", height: "100vh" }}>
      {/* Left Side - Live Camera */}
      <div className={styles.Camera}>
        <h1>Live Object Detection</h1>
        <button onClick={startCamera} disabled={cameraOn} style={{ margin: "10px", padding: "10px" }}>
          Start Camera
        </button>
        <button onClick={stopCamera} disabled={!cameraOn} style={{ margin: "10px", padding: "10px" }}>
          Stop Camera
        </button>
        {cameraOn && (
          <img
            src="http://127.0.0.1:8080/video_feed"
            alt="Live Stream"
            width="640"
            height="480"
          />
        )}
      </div>

      {/* Right Side - Saved Images */}
      <div>
        <h2>Saved Detections</h2>
        {images.length === 0 ? (
          <p>No images detected yet.</p>
        ) : (
          <div style={{ display: "flex", flexWrap: "wrap", gap: "10px" }}>
            {images.map((image, index) => (
              <img
                key={index}
                src={`http://127.0.0.1:8080/detections/${image}`}
                alt="Detected object"
                width="150"
                height="150"
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Camera;