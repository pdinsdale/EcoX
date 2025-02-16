import React, { useCallback, useEffect, useState } from "react";
import axios from "axios";
import "./../App.css";
import styles from './Camera.module.css'

function Camera() {
  const [images, setImages] = useState([]);
  const [cameraOn, setCameraOn] = useState(false);

  // const handleToggleWebcam = useCallback(() => {
  //   setCameraOn((prev) => !prev);
  // }, []);

  // Function to fetch saved images from Flask
  // const fetchImages = () => {
  //   axios.get("http://127.0.0.1:8080/detections")
  //     .then(response => {
  //       setImages(response.data.images);
  //     })
  //     .catch(error => {
  //       console.error("Error fetching images:", error);
  //     });
  // };

  // Fetch images initially and every 2 seconds
  // useEffect(() => {
  //   fetchImages();
  //   const interval = setInterval(fetchImages, 2000);
  //   return () => clearInterval(interval);
  // }, []);

  // Start Camera
  // const startCamera = () => {
  //   axios.get("http://127.0.0.1:8080/start_camera")
  //     .then(() => {
  //       setCameraOn(true);
  //     })
  //     .catch(error => {
  //       console.error("Error starting camera:", error);
  //     });
  // };

  // // Stop Camera
  // const stopCamera = () => {
  //   axios.get("http://127.0.0.1:8080/stop_camera")
  //     .then(() => {
  //       setCameraOn(false);
  //     })
  //     .catch(error => {
  //       console.error("Error stopping camera:", error);
  //     });
  // };

  const toggleCamera = () => {
    const action = cameraOn ? "stop_camera" : "start_camera";
    axios.get(`http://127.0.0.1:8080/${action}`)
      .then(() => {
        setCameraOn(!cameraOn);
      })
      .catch(error => {
        console.error(`Error toggling camera:`, error);
      });
  };

  return (
    <div className={styles.CameraWrapper}>
      {cameraOn && (
        <img className={styles.Camera}
          src="http://127.0.0.1:8080/video_feed"
          alt="Live Stream"
        />
      )}
      {!cameraOn && (
        <div className={styles.Camera}></div>
      )}

      <button className={styles.toggleCamera} onClick={toggleCamera}>{cameraOn ? "Stop Camera" : "Start Camera"}</button>
    </div>
  );
}

export default Camera;