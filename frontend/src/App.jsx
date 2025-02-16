import React from 'react';
import "./App.css";

import Home from './components/Home';
import Camera from './components/Camera';
import Scan from './components/Scan'

import { Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/scan" element={<Scan />}/>
    </Routes>
  );
}

export default App;