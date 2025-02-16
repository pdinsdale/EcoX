import React from 'react';
import "./App.css";

import Home from './components/Home';
import Camera from './components/Camera';

import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/camera" element={<Camera />} />
    </Routes>
  );
}

export default App;